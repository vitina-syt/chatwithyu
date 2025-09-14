from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # 应用配置
    PROJECT_NAME: str = "PDF QA System"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # 数据库配置
    # mysql+<driver>://<user>:<password>@<host>[:<port>]/<database_name>
    DATABASE_URL: str="mysql+pymysql://root:root123456d@localhost:3307/chat_with_yu_database"
    DATABASE_TEST_URL: Optional[str] = None
    
    # 安全配置
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # 文件配置
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    ALLOWED_FILE_TYPES: list = ["application/pdf"]
    
    # AI 配置
    OPENAI_API_KEY: Optional[str] = None
    EMBEDDING_MODEL: str = "text-embedding-ada-002"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
