from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from core.config import settings
from api.endpoints import files, qa, auth

app = FastAPI(
    title="PDF QA API",
     version="1.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(files.router)
# app.include_router(qa.router)
# app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "PDF QA System API", "version": "1.0.0"}

if __name__ == "__main__":
    uvicorn.run(
        "PDF QA System.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
