from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import os
import hashlib
from typing import Dict

from src.models.database import get_db
from src.models.db_models import PDFFile
from src.core.config import settings

router = APIRouter(prefix="/api", tags=["files"])


def _ensure_pdf_dir_exists(directory_path: str) -> None:
    if not os.path.exists(directory_path):
        os.makedirs(directory_path, exist_ok=True)


def _compute_md5_for_bytes(data: bytes) -> str:
    md5 = hashlib.md5()
    md5.update(data)
    return md5.hexdigest()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)) -> Dict[str, str]:
    # 校验类型
    if file.content_type not in settings.ALLOWED_FILE_TYPES:
        raise HTTPException(status_code=400, detail="只允许上传 PDF 文件")

    # 读取内容
    content: bytes = await file.read()

    # 大小限制
    if len(content) > settings.MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="文件大小超出限制")

    # 哈希去重
    file_hash = _compute_md5_for_bytes(content)
    existing = db.query(PDFFile).filter(PDFFile.file_hash == file_hash).first()
    if existing:
        return {"message": "文件已存在", "file_id": existing.file_id, "filename": existing.filename}

    # 保存到磁盘
    pdf_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../pdf"))
    _ensure_pdf_dir_exists(pdf_dir)

    sanitized_name = os.path.basename(file.filename)
    # 以哈希+原名避免重名
    stored_filename = f"{file_hash[:8]}_{sanitized_name}"
    file_path = os.path.join(pdf_dir, stored_filename)
    with open(file_path, "wb") as f:
        f.write(content)

    # 入库
    pdf_record = PDFFile(
        filename=stored_filename,
        original_filename=sanitized_name,
        file_path=file_path,
        file_size=len(content),
        file_hash=file_hash,
        processing_status="pending",
    )
    db.add(pdf_record)
    db.commit()
    db.refresh(pdf_record)

    return JSONResponse({
        "message": "上传成功",
        "file_id": pdf_record.file_id,
        "filename": pdf_record.filename
    })


