import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# 加载.env环境变量
load_dotenv()

class Settings(BaseSettings):
    # 后端服务配置
    PORT: int = int(os.getenv("PORT", 8000))
    HOST: str = os.getenv("HOST", "0.0.0.0")
    RELOAD: bool = os.getenv("RELOAD", "True").lower() == "true"
    
    # OpenAI配置
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

# 实例化配置对象，供其他模块调用
settings = Settings()