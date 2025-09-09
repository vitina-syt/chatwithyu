from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.models.database import Base
from datetime import datetime
from typing import Optional
import uuid

class PDFFile(Base):
    """
    PDF文件模型
    存储上传的PDF文件信息和处理状态
    """
    __tablename__ = "pdf_files"

    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(String(36), unique=True, index=True, default=lambda: str(uuid.uuid4()))
    filename = Column(String(255), nullable=False, index=True)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=False)
    file_hash = Column(String(64), unique=True, index=True)  # MD5 hash for duplicate detection
    
    # 处理状态
    processing_status = Column(String(50), default="pending")  # pending, processing, completed, failed
    chunks_count = Column(Integer, default=0)
    processing_error = Column(Text, nullable=True)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    processed_at = Column(DateTime(timezone=True), nullable=True)
    
    # 关联关系
    conversations = relationship("Conversation", back_populates="pdf_file", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<PDFFile(id={self.id}, filename='{self.filename}', status='{self.processing_status}')>"

class Conversation(Base):
    """
    对话模型
    存储用户与AI的问答记录
    """
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(String(36), unique=True, index=True, default=lambda: str(uuid.uuid4()))
    pdf_file_id = Column(Integer, nullable=False, index=True)
    
    # 对话内容
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    context_chunks = Column(Text, nullable=True)  # JSON string of relevant chunks
    
    # 元数据
    question_length = Column(Integer, default=0)
    answer_length = Column(Integer, default=0)
    processing_time = Column(Float, nullable=True)  # 处理时间（秒）
    
    # 评分和反馈
    user_rating = Column(Integer, nullable=True)  # 1-5 评分
    user_feedback = Column(Text, nullable=True)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关联关系
    pdf_file = relationship("PDFFile", back_populates="conversations")

    def __repr__(self):
        return f"<Conversation(id={self.id}, question='{self.question[:50]}...')>"

class DocumentChunk(Base):
    """
    文档块模型
    存储PDF文档分割后的文本块
    """
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True)
    pdf_file_id = Column(Integer, nullable=False, index=True)
    chunk_index = Column(Integer, nullable=False)  # 在文档中的顺序
    
    # 内容
    content = Column(Text, nullable=False)
    content_length = Column(Integer, nullable=False)
    
    # 元数据
    page_number = Column(Integer, nullable=True)
    chunk_type = Column(String(50), default="text")  # text, title, paragraph, etc.
    
    # 向量信息
    embedding_model = Column(String(100), nullable=True)
    vector_id = Column(String(100), nullable=True)  # ChromaDB中的向量ID
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 索引
    __table_args__ = (
        {"extend_existing": True}
    )

    def __repr__(self):
        return f"<DocumentChunk(id={self.id}, pdf_file_id={self.pdf_file_id}, chunk_index={self.chunk_index})>"

class SystemLog(Base):
    """
    系统日志模型
    记录系统运行状态和错误信息
    """
    __tablename__ = "system_logs"

    id = Column(Integer, primary_key=True, index=True)
    log_level = Column(String(20), nullable=False, index=True)  # INFO, WARNING, ERROR, DEBUG
    log_type = Column(String(50), nullable=False, index=True)  # upload, processing, query, system
    
    # 日志内容
    message = Column(Text, nullable=False)
    details = Column(Text, nullable=True)  # JSON string for additional details
    
    # 关联信息
    pdf_file_id = Column(Integer, nullable=True, index=True)
    conversation_id = Column(Integer, nullable=True, index=True)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<SystemLog(id={self.id}, level='{self.log_level}', type='{self.log_type}')>"

class UserSession(Base):
    """
    用户会话模型
    跟踪用户的使用情况
    """
    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(36), unique=True, index=True, default=lambda: str(uuid.uuid4()))
    
    # 会话信息
    ip_address = Column(String(45), nullable=True)  # IPv4/IPv6
    user_agent = Column(String(500), nullable=True)
    
    # 统计信息
    total_uploads = Column(Integer, default=0)
    total_questions = Column(Integer, default=0)
    total_answers = Column(Integer, default=0)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_activity = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<UserSession(id={self.id}, session_id='{self.session_id}')>"

# 创建索引
from sqlalchemy import Index

# 为常用查询创建复合索引
Index('idx_pdf_files_status_created', PDFFile.processing_status, PDFFile.created_at)
Index('idx_conversations_pdf_created', Conversation.pdf_file_id, Conversation.created_at)
Index('idx_chunks_pdf_index', DocumentChunk.pdf_file_id, DocumentChunk.chunk_index)
Index('idx_logs_level_type_created', SystemLog.log_level, SystemLog.log_type, SystemLog.created_at)
