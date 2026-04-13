<template>
  <div class="chat-app">
    <!-- 左侧 ChatBot 列表 -->
    <div class="chatbot-sidebar">
      <h3>ChatBots</h3>
      <div class="chatbot-list">
        <div 
          v-for="chatbot in chatbots" 
          :key="chatbot.id"
          class="chatbot-item"
          :class="{ active: selectedChatBotId === chatbot.id }"
          @click="selectChatBot(chatbot.id)"
        >
          <div class="chatbot-icon">{{ chatbot.name.charAt(0) }}</div>
          <div class="chatbot-info">
            <div class="chatbot-name">{{ chatbot.name }}</div>
            <div class="chatbot-model">{{ chatbot.model }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 右侧聊天区域 -->
    <div class="chat-area" v-if="selectedChatBotId">
      <!-- 聊天窗口头部 -->
      <div class="chat-header">
        <div class="chatbot-title">
          {{ getSelectedChatBot()?.name }}
        </div>
        <div class="session-control">
          <select v-model="selectedSessionId" @change="loadSessionConversations">
            <option value="">请选择会话</option>
            <option v-for="session in sessions" :key="session.id" :value="session.id">
              {{ session.name }}
            </option>
          </select>
          <button class="add-session-btn" @click="showCreateSessionModal = true">
            +
          </button>
        </div>
      </div>

      <!-- 聊天消息区域 -->
      <div class="chat-messages">
        <div v-if="conversations.length === 0" class="empty-state">
          暂无对话历史，请开始新的对话
        </div>
        <div v-else class="message-list">
          <div v-for="(conv, index) in conversations" :key="conv.id" class="message">
            <div class="user-message">
              <div class="message-header">
                <span class="sender">你</span>
                <span class="timestamp">{{ formatDate(conv.created_at) }}</span>
              </div>
              <div class="message-content">{{ conv.user_message }}</div>
            </div>
            <div class="model-message">
              <div class="message-header">
                <span class="sender">{{ getSelectedChatBot()?.name }}</span>
                <span class="timestamp">{{ formatDate(conv.created_at) }}</span>
              </div>
              <div class="message-content">{{ conv.model_response }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 输入区域 -->
      <div class="chat-input-area">
        <textarea 
          v-model="userInput" 
          placeholder="输入消息..." 
          @keydown.enter.exact="sendMessage"
          @keydown.enter.shift="$event.preventDefault()"
        ></textarea>
        <button class="send-btn" @click="sendMessage" :disabled="!userInput.trim()">
          发送
        </button>
      </div>
    </div>

    <!-- 未选择 ChatBot 提示 -->
    <div class="no-selection" v-else>
      <h3>请选择一个 ChatBot 开始对话</h3>
    </div>

    <!-- 创建会话模态框 -->
    <div v-if="showCreateSessionModal" class="modal">
      <div class="modal-content">
        <h3>创建新会话</h3>
        <form @submit.prevent="createSession">
          <div class="form-group">
            <label>会话名称：</label>
            <input type="text" v-model="newSessionName" placeholder="输入会话名称" required>
          </div>
          <div class="button-group">
            <button type="submit">创建</button>
            <button type="button" @click="showCreateSessionModal = false">取消</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { request } from '../utils/request';

// 状态
const chatbots = ref([]);
const sessions = ref([]);
const conversations = ref([]);
const selectedChatBotId = ref('');
const selectedSessionId = ref('');
const userInput = ref('');
const showCreateSessionModal = ref(false);
const newSessionName = ref('');

// 计算属性
const getSelectedChatBot = () => {
  return chatbots.value.find(chatbot => chatbot.id === selectedChatBotId.value);
};

// 加载 ChatBot 列表
const loadChatBots = async () => {
  try {
    const response = await request('/api/chatbot/list', 'GET');
    chatbots.value = response.data;
  } catch (error) {
    console.error('加载 ChatBot 列表失败:', error);
  }
};

// 选择 ChatBot
const selectChatBot = async (chatbotId) => {
  selectedChatBotId.value = chatbotId;
  selectedSessionId.value = '';
  conversations.value = [];
  await loadSessions();
};

// 加载会话列表
const loadSessions = async () => {
  if (!selectedChatBotId.value) return;
  
  try {
    const response = await request(`/api/chatbot/session/list/${selectedChatBotId.value}`, 'GET');
    sessions.value = response.data;
  } catch (error) {
    console.error('加载会话列表失败:', error);
  }
};

// 加载会话历史
const loadSessionConversations = async () => {
  if (!selectedChatBotId.value || !selectedSessionId.value) {
    conversations.value = [];
    return;
  }
  
  try {
    const response = await request(`/api/chatbot/session/${selectedSessionId.value}/conversations?chatbot_id=${selectedChatBotId.value}`, 'GET');
    conversations.value = response.data;
  } catch (error) {
    console.error('加载会话历史失败:', error);
  }
};

// 创建会话
const createSession = async () => {
  if (!selectedChatBotId.value || !newSessionName.value) return;
  
  try {
    const response = await request('/api/chatbot/session/create', 'POST', {
      chatbot_id: selectedChatBotId.value,
      name: newSessionName.value
    });
    
    // 重新加载会话列表
    await loadSessions();
    
    // 选择新创建的会话
    selectedSessionId.value = response.data.session_id;
    conversations.value = [];
    
    // 关闭模态框
    showCreateSessionModal.value = false;
    newSessionName.value = '';
  } catch (error) {
    console.error('创建会话失败:', error);
  }
};

// 发送消息
const sendMessage = async () => {
  if (!selectedChatBotId.value || !userInput.value.trim()) return;
  
  // 如果没有选择会话，创建一个新会话
  if (!selectedSessionId.value) {
    await createSession();
    if (!selectedSessionId.value) return;
  }
  
  try {
    const response = await request('/api/chatbot/chat', 'POST', {
      chatbot_id: selectedChatBotId.value,
      params: {
        model: getSelectedChatBot()?.model || 'gpt-5',
        messages: [{"role": "user", "content": userInput.value}]
      },
      session_id: selectedSessionId.value
    });
    
    // 重新加载会话历史
    await loadSessionConversations();
    
    // 清空输入
    userInput.value = '';
  } catch (error) {
    console.error('发送消息失败:', error);
  }
};

// 格式化日期
const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleString();
};

// 组件挂载时加载数据
onMounted(() => {
  loadChatBots();
});
</script>

<style scoped>
.chat-app {
  display: flex;
  height: calc(100vh - 120px); /* 减去导航栏和容器的 padding/margin */
  width: 100%;
  overflow: hidden;
}

/* 左侧 ChatBot 列表 */
.chatbot-sidebar {
  width: 250px;
  background-color: #f5f5f5;
  border-right: 1px solid #ddd;
  padding: 20px;
  overflow-y: auto;
  max-height: calc(100vh - 120px); /* 减去导航栏和容器的 padding/margin */
  box-sizing: border-box;
}

.chatbot-sidebar h3 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #333;
}

.chatbot-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.chatbot-item {
  display: flex;
  align-items: center;
  padding: 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.chatbot-item:hover {
  background-color: #e0e0e0;
}

.chatbot-item.active {
  background-color: #e3f2fd;
  border: 1px solid #2196F3;
}

.chatbot-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #2196F3;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  margin-right: 12px;
}

.chatbot-info {
  flex: 1;
}

.chatbot-name {
  font-weight: bold;
  margin-bottom: 4px;
  color: #333;
}

.chatbot-model {
  font-size: 12px;
  color: #666;
}

/* 右侧聊天区域 */
.chat-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: #f9f9f9;
  min-width: 0;
  max-height: calc(100vh - 120px); /* 减去导航栏和容器的 padding/margin */
  overflow: hidden;
}
/* 聊天窗口头部 */
.chat-header {
  background-color: white;
  padding: 15px 20px;
  border-bottom: 1px solid #ddd;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chatbot-title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.session-control {
  display: flex;
  align-items: center;
  gap: 10px;
}

.session-control select {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.add-session-btn {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-color: #4CAF50;
  color: white;
  border: none;
  font-size: 18px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.3s ease;
}

.add-session-btn:hover {
  background-color: #45a049;
}

/* 聊天消息区域 */
.chat-messages {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  max-height: calc(100vh - 260px); /* 减去导航栏、容器的 padding/margin 以及头部和输入区域的高度 */
  box-sizing: border-box;
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: #666;
}

.message-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.message {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.user-message {
  align-self: flex-end;
  max-width: 80%;
  background-color: #e3f2fd;
  border-radius: 12px 12px 0 12px;
  padding: 12px;
}

.model-message {
  align-self: flex-start;
  max-width: 80%;
  background-color: white;
  border-radius: 12px 12px 12px 0;
  padding: 12px;
  border: 1px solid #ddd;
}

.message-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 12px;
}

.sender {
  font-weight: bold;
  color: #333;
}

.timestamp {
  color: #999;
}

.message-content {
  line-height: 1.4;
  color: #333;
}

/* 输入区域 */
.chat-input-area {
  background-color: white;
  padding: 15px 20px;
  border-top: 1px solid #ddd;
  display: flex;
  gap: 10px;
  flex-shrink: 0;
}

.chat-input-area textarea {
  flex: 1;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  resize: none;
  min-height: 60px;
  font-size: 14px;
  max-height: 200px;
  overflow-y: auto;
  box-sizing: border-box;
}

.send-btn {
  padding: 0 20px;
  background-color: #2196F3;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  align-self: flex-end;
  margin-bottom: 10px;
  white-space: nowrap;
  min-width: 80px;
}

.send-btn:hover {
  background-color: #0b7dda;
}

.send-btn:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

/* 未选择 ChatBot 提示 */
.no-selection {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f9f9f9;
  color: #666;
}

/* 模态框 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 30px;
  border-radius: 8px;
  width: 90%;
  max-width: 400px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.modal-content h3 {
  margin-top: 0;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.button-group {
  display: flex;
  gap: 10px;
  margin-top: 20px;
  justify-content: flex-end;
}

.button-group button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.button-group button:first-child {
  background-color: #4CAF50;
  color: white;
}

.button-group button:first-child:hover {
  background-color: #45a049;
}

.button-group button:last-child {
  background-color: #999;
  color: white;
}

.button-group button:last-child:hover {
  background-color: #777;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .chat-app {
    flex-direction: column;
  }
  
  .chatbot-sidebar {
    width: 100%;
    height: 200px;
    border-right: none;
    border-bottom: 1px solid #ddd;
  }
  
  .chatbot-list {
    flex-direction: row;
    flex-wrap: wrap;
  }
  
  .chatbot-item {
    width: calc(50% - 5px);
  }
  
  .user-message,
  .model-message {
    max-width: 90%;
  }
}
</style>