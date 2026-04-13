from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # 解决跨域问题

from backend.api import api_router
from backend.config.settings import settings
from backend.database.db import create_tables

# 初始化数据库表
create_tables()

# 初始化FastAPI应用
app = FastAPI(title="Persona Prompt & OpenAI Parameter Agent (MVP)", version="1.0.0")

# 解决跨域问题（前端对接后端必备）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发环境允许所有来源，生产环境可修改为指定域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册 API 路由
app.include_router(api_router, prefix="/api")

# 启动服务（关联配置文件中的端口、主机）
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app", host=settings.HOST, port=settings.PORT, reload=settings.RELOAD
    )
