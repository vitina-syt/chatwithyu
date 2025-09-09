import os
import uuid
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import uvicorn

# 导入原有的功能
from pypdf_pdf_qa import load_pdf_split, creatt_chroma_vectorstore, setup_ollama_llm, create_qa_chain

app = FastAPI(title="PDF QA API", version="1.0.0")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # 前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局变量存储当前的处理链
current_qa_chain = None
current_pdf_path = None

class QuestionRequest(BaseModel):
    question: str

class QuestionResponse(BaseModel):
    answer: str
    success: bool
    message: Optional[str] = None

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """上传PDF文件"""
    global current_qa_chain, current_pdf_path
    
    try:
        # 检查文件类型
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="只能上传PDF文件")
        
        # 生成唯一文件名
        file_id = str(uuid.uuid4())
        filename = f"{file_id}.pdf"
        file_path = os.path.join("./pdf", filename)
        
        # 确保目录存在
        os.makedirs("./pdf", exist_ok=True)
        
        # 保存文件
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # 处理PDF文件
        print(f"开始处理PDF文件: {file_path}")
        
        # # 1. 加载并分割PDF
        # docs = load_pdf_split(file_path)
        
        # # 2. 创建向量存储
        # retriever = creatt_chroma_vectorstore(docs, "bge-m3")
        
        # # 3. 设置LLM
        # llm = setup_ollama_llm("llama3")
        
        # # 4. 创建问答链
        # current_qa_chain = create_qa_chain(llm, retriever)
        # current_pdf_path = file_path
        
        return JSONResponse({
            "success": True,
            "message": f"文件 {file.filename} 上传成功，已建立知识库",
            "file_id": file_id,
            # "chunks_count": len(docs)
        })
        
    except Exception as e:
        print(f"文件上传处理错误: {e}")
        raise HTTPException(status_code=500, detail=f"文件处理失败: {str(e)}")

@app.post("/api/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """提问接口"""
    global current_qa_chain
    
    if not current_qa_chain:
        return QuestionResponse(
            answer="",
            success=False,
            message="请先上传PDF文件"
        )
    
    try:
        print(f"收到问题: {request.question}")
        answer = current_qa_chain.invoke(request.question)
        
        return QuestionResponse(
            answer=answer,
            success=True,
            message="回答成功"
        )
        
    except Exception as e:
        print(f"问答处理错误: {e}")
        return QuestionResponse(
            answer="",
            success=False,
            message=f"处理问题失败: {str(e)}"
        )

@app.get("/api/status")
async def get_status():
    """获取服务状态"""
    return JSONResponse({
        "status": "running",
        "has_pdf": current_qa_chain is not None,
        "pdf_path": current_pdf_path
    })

@app.get("/")
async def root():
    return {"message": "PDF QA API 服务正在运行"}

if __name__ == "__main__":
    print("启动PDF QA API服务器...")
    print("前端地址: http://localhost:8080")
    print("API文档: http://localhost:8000/docs")
    
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
