from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.agent.chatbot_agent import ChatBot
from backend.database.db import ChatBot as ChatBotModel
from backend.database.db import get_db

router = APIRouter()

from .api import chatbot_instances


class SessionCreateInput(BaseModel):
    chatbot_id: str
    name: str


@router.post(
    "/session/create",
    summary="创建会话",
    description="为指定的 ChatBot 创建一个新的会话",
)
async def create_session(input: SessionCreateInput):
    try:
        # 获取或创建 ChatBot 实例
        if input.chatbot_id not in chatbot_instances:
            # 从数据库加载 ChatBot
            db_generator = get_db()
            db = next(db_generator)
            chatbot_model = (
                db.query(ChatBotModel)
                .filter(ChatBotModel.id == input.chatbot_id)
                .first()
            )
            if not chatbot_model:
                raise HTTPException(
                    status_code=404, detail=f"ChatBot {input.chatbot_id} 不存在"
                )
            # 创建 ChatBot 实例
            chatbot = ChatBot(
                name=chatbot_model.name,
                system_prompt=chatbot_model.system_prompt,
                model=chatbot_model.model,
            )
            chatbot_instances[input.chatbot_id] = chatbot
        else:
            chatbot = chatbot_instances[input.chatbot_id]

        # 创建会话
        session_id = chatbot.create_session(input.name)

        return {
            "code": 200,
            "message": "会话创建成功",
            "data": {"session_id": session_id, "name": input.name},
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建会话失败: {str(e)}")


@router.get(
    "/session/list/{chatbot_id}",
    summary="获取会话列表",
    description="获取指定 ChatBot 的所有会话",
)
async def get_sessions(chatbot_id: str):
    try:
        # 获取或创建 ChatBot 实例
        if chatbot_id not in chatbot_instances:
            # 从数据库加载 ChatBot
            db_generator = get_db()
            db = next(db_generator)
            chatbot_model = (
                db.query(ChatBotModel).filter(ChatBotModel.id == chatbot_id).first()
            )
            if not chatbot_model:
                raise HTTPException(
                    status_code=404, detail=f"ChatBot {chatbot_id} 不存在"
                )
            # 创建 ChatBot 实例
            chatbot = ChatBot(
                name=chatbot_model.name,
                system_prompt=chatbot_model.system_prompt,
                model=chatbot_model.model,
            )
            chatbot_instances[chatbot_id] = chatbot
        else:
            chatbot = chatbot_instances[chatbot_id]

        # 获取会话列表
        sessions = chatbot.get_sessions()

        return {"code": 200, "message": "获取会话列表成功", "data": sessions}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取会话列表失败: {str(e)}")


@router.get(
    "/session/{session_id}/conversations",
    summary="获取会话历史",
    description="获取指定会话的对话历史",
)
async def get_session_conversations(session_id: str, chatbot_id: str):
    try:
        # 获取或创建 ChatBot 实例
        if chatbot_id not in chatbot_instances:
            # 从数据库加载 ChatBot
            db_generator = get_db()
            db = next(db_generator)
            chatbot_model = (
                db.query(ChatBotModel).filter(ChatBotModel.id == chatbot_id).first()
            )
            if not chatbot_model:
                raise HTTPException(
                    status_code=404, detail=f"ChatBot {chatbot_id} 不存在"
                )
            # 创建 ChatBot 实例
            chatbot = ChatBot(
                name=chatbot_model.name,
                system_prompt=chatbot_model.system_prompt,
                model=chatbot_model.model,
            )
            chatbot_instances[chatbot_id] = chatbot
        else:
            chatbot = chatbot_instances[chatbot_id]

        # 获取会话历史
        conversations = chatbot.get_session_conversations(session_id)

        return {"code": 200, "message": "获取会话历史成功", "data": conversations}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取会话历史失败: {str(e)}")
