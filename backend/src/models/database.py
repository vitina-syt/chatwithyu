from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager
from typing import Generator
from src.core.config import settings
import logging

# 创建配置实例
settings = settings

logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL))

engine = create_engine(
    settings.DATABASE_URL, 
    pool_size=settings.DATABASE_POOL_SIZE, 
    poolclass=QueuePool,
    max_overflow=settings.DATABASE_MAX_OVERFLOW
)

SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """
    获取数据库会话的依赖注入函数
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@contextmanager
def get_db_context() -> Generator[Session, None, None]:
    """
    获取数据库会话的上下文管理器
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    finally:
        db.close()

def init_db() -> None:
    """
    初始化数据库
    """
    try:
        Base.metadata.create_all(bind=engine)
        logging.info("Database tables created successfully")
    except Exception as e:
        logging.error(f"Failed to create database tables: {e}")
        raise
