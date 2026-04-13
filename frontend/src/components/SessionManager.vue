<template>
  <div class="session-manager">
    <h2>会话管理</h2>
    
    <div class="control-panel">
      <!-- ChatBot 选择 -->
      <div class="control-group">
        <label for="chatbot-select">选择 ChatBot:</label>
        <select id="chatbot-select" v-model="selectedChatBotId" @change="loadSessions">
          <option value="">请选择 ChatBot</option>
          <option v-for="chatbot in chatbots" :key="chatbot.id" :value="chatbot.id">
            {{ chatbot.name }}
          </option>
        </select>
      </div>
      
      <!-- 会话选择 -->
      <div class="control-group">
        <label for="session-select">选择会话:</label>
        <select id="session-select" v-model="selectedSessionId" @change="loadSessionConversations">
          <option value="">请选择会话</option>
          <option v-for="session in sessions" :key="session.id" :value="session.id">
            {{ session.name }}
          </option>
        </select>
      </div>
      
      <!-- 创建新会话 -->
      <div class="control-group">
        <input type="text" v-model="newSessionName" placeholder="新会话名称">
        <button @click="createSession" :disabled="!selectedChatBotId || !newSessionName">
          创建会话
        </button>
      </div>
    </div>
    
    <!-- 会话历史 -->
    <div class="conversation-history" v-if="selectedSessionId">
      <h3>会话历史</h3>
      <div class="messages">
        <div v-for="(conv, index) in conversations" :key="conv.id" class="message">
          <div class="user-message">
            <strong>用户:</strong> {{ conv.user_message }}
          </div>
          <div class="model-response">
            <strong>模型:</strong> {{ conv.model_response }}
          </div>
          <div class="timestamp">{{ formatDate(conv.created_at) }}</div>
          <hr v-if="index < conversations.length - 1">
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { request } from '../utils/request';

const chatbots = ref([]);
const sessions = ref([]);
const conversations = ref([]);
const selectedChatBotId = ref('');
const selectedSessionId = ref('');
const newSessionName = ref('');

// 加载 ChatBot 列表
const loadChatBots = async () => {
  try {
    const response = await request('/api/chatbot/list', 'GET');
    chatbots.value = response.data;
  } catch (error) {
    console.error('加载 ChatBot 列表失败:', error);
  }
};

// 加载会话列表
const loadSessions = async () => {
  if (!selectedChatBotId.value) {
    sessions.value = [];
    selectedSessionId.value = '';
    conversations.value = [];
    return;
  }
  
  try {
    const response = await request(`/api/chatbot/session/list/${selectedChatBotId.value}`, 'GET');
    sessions.value = response.data;
    selectedSessionId.value = '';
    conversations.value = [];
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

// 创建新会话
const createSession = async () => {
  if (!selectedChatBotId.value || !newSessionName.value) {
    return;
  }
  
  try {
    const response = await request('/api/chatbot/session/create', 'POST', {
      chatbot_id: selectedChatBotId.value,
      name: newSessionName.value
    });
    
    // 重新加载会话列表
    await loadSessions();
    
    // 清空输入
    newSessionName.value = '';
  } catch (error) {
    console.error('创建会话失败:', error);
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
.session-manager {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

h2 {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
}

.control-panel {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 30px;
  padding: 20px;
  background-color: #f5f5f5;
  border-radius: 8px;
}

.control-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.control-group label {
  font-weight: bold;
  min-width: 100px;
}

.control-group select,
.control-group input {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  flex: 1;
  min-width: 200px;
}

.control-group button {
  padding: 8px 16px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.control-group button:hover {
  background-color: #45a049;
}

.control-group button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.conversation-history {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  border: 1px solid #ddd;
}

.conversation-history h3 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #333;
}

.messages {
  max-height: 400px;
  overflow-y: auto;
}

.message {
  margin-bottom: 15px;
}

.user-message {
  background-color: #e3f2fd;
  padding: 10px;
  border-radius: 8px;
  margin-bottom: 5px;
}

.model-response {
  background-color: #f3e5f5;
  padding: 10px;
  border-radius: 8px;
  margin-bottom: 5px;
}

.timestamp {
  font-size: 12px;
  color: #666;
  text-align: right;
}

hr {
  margin: 15px 0;
  border: 1px solid #eee;
}

@media (max-width: 768px) {
  .control-panel {
    flex-direction: column;
    align-items: stretch;
  }
  
  .control-group {
    flex-direction: column;
    align-items: stretch;
  }
  
  .control-group label {
    min-width: auto;
    margin-bottom: 5px;
  }
  
  .control-group select,
  .control-group input {
    min-width: auto;
  }
}
</style>