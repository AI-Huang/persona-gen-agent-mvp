import os
import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# 获取数据库连接URL
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/persona_agent"
)

# 创建数据库引擎
engine = create_engine(DATABASE_URL)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基类
Base = declarative_base()


# ChatBot 表 - 存储 ChatBot 自身属性
class ChatBot(Base):
    __tablename__ = "chatbots"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    system_prompt = Column(Text, nullable=False)
    model = Column(String, nullable=False, default="gpt-3.5-turbo")
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    conversations = relationship("Conversation", back_populates="chatbot")


# 会话表 - 存储用户请求和模型响应
class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    chatbot_id = Column(String, ForeignKey("chatbots.id"), nullable=False)
    user_message = Column(Text, nullable=False)
    model_response = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    chatbot = relationship("ChatBot", back_populates="conversations")


# 创建表
def create_tables():
    Base.metadata.create_all(bind=engine)


# 获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
