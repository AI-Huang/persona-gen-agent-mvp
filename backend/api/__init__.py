from fastapi import APIRouter

api_router = APIRouter()

from backend.api import generate, templates
from backend.api.chatbot import chatbot, conversations

# 注册路由
api_router.include_router(templates.router)
api_router.include_router(generate.router)
api_router.include_router(chatbot.router, prefix="/chatbot")
api_router.include_router(conversations.router, prefix="/chatbot")
