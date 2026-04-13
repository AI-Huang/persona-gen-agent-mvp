<template>
  <div class="panel">
    <h2>LLM 上手调试</h2>
    
    <!-- LLM 选择 -->
    <div class="form-group">
      <label>选择 LLM 模型：</label>
      <select v-model="selectedModel">
        <option value="gpt-5">GPT-5</option>
        <option value="gpt-5.1">GPT-5.1</option>
        <option value="gpt-5.2">GPT-5.2</option>
        <option value="gpt-5.4">GPT-5.4</option>
      </select>
    </div>
    
    <!-- 系统提示词 -->
    <div class="form-group">
      <label>系统提示词：</label>
      <textarea v-model="systemPrompt" placeholder="输入系统提示词..."></textarea>
    </div>
    
    <!-- ChatBot ID 显示 -->
    <div v-if="chatbotId" class="form-group">
      <label>ChatBot ID：</label>
      <div class="chatbot-id">
        {{ chatbotId }}
        <button @click="copyChatbotId" class="copy-btn">复制</button>
      </div>
    </div>
    
    <!-- 对话历史 -->
    <div class="form-group">
      <label>对话历史：</label>
      <div class="chat-history">
        <div 
          v-for="(message, index) in messages" 
          :key="index"
          :class="['message', message.role]"
        >
          <div class="message-role">{{ message.role === 'user' ? '用户' : 'LLM' }}：</div>
          <div class="message-content">{{ message.content }}</div>
        </div>
      </div>
    </div>
    
    <!-- 用户输入 -->
    <div class="form-group">
      <label>用户输入：</label>
      <textarea v-model="userInput" placeholder="输入你的问题..."></textarea>
    </div>
    
    <!-- 参数设置 -->
    <div class="form-group">
      <label>参数设置：</label>
      <div class="params-container">
        <div class="param-item">
          <label>temperature: {{ temperature }}</label>
          <input type="range" v-model.number="temperature" min="0" max="2" step="0.1">
        </div>
        <div class="param-item">
          <label>top_p: {{ topP }}</label>
          <input type="range" v-model.number="topP" min="0" max="1" step="0.1">
        </div>
        <div class="param-item">
          <label>max_tokens: {{ maxTokens }}</label>
          <input type="number" v-model.number="maxTokens" min="1" max="4096" step="100">
        </div>
        <div class="param-item">
          <label>frequency_penalty: {{ frequencyPenalty }}</label>
          <input type="range" v-model.number="frequencyPenalty" min="-2" max="2" step="0.1">
        </div>
        <div class="param-item">
          <label>presence_penalty: {{ presencePenalty }}</label>
          <input type="range" v-model.number="presencePenalty" min="-2" max="2" step="0.1">
        </div>
        <div class="param-item">
          <label>stop: {{ stop }}</label>
          <input type="text" v-model="stop" placeholder="输入停止词，用逗号分隔">
        </div>
      </div>
    </div>
    
    <!-- 错误提示 -->
    <div v-if="error" class="error-message">
      {{ error }}
    </div>
    
    <!-- 发送按钮 -->
    <div class="button-group">
      <button @click="sendRequest" :disabled="!userInput.trim() || loading">
        {{ loading ? '发送中...' : '发送请求' }}
      </button>
      <button @click="clearAll" :disabled="loading">清空对话</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { request } from '../utils/request';

const selectedModel = ref('gpt-5');
const systemPrompt = ref('');
const userInput = ref('');
const temperature = ref(0.7);
const topP = ref(0.9);
const maxTokens = ref(1000);
const frequencyPenalty = ref(0);
const presencePenalty = ref(0);
const stop = ref('');
const messages = ref([]);
const loading = ref(false);
const error = ref('');
const chatbotId = ref('');

// 创建 ChatBot 实例
const createChatBot = async () => {
  try {
    loading.value = true;
    error.value = '';
    
    const response = await request('/api/chatbot/create', 'POST', {
      name: 'LLM 调试助手',
      system_prompt: systemPrompt.value || '你是一个 helpful 的助手',
      model: selectedModel.value
    });
    
    chatbotId.value = response.data.chatbot_id;
    console.log('ChatBot 创建成功:', chatbotId.value);
  } catch (err) {
    error.value = '创建 ChatBot 失败，请稍后重试';
    console.error('创建 ChatBot 失败:', err);
  } finally {
    loading.value = false;
  }
};

const sendRequest = async () => {
  if (!userInput.value.trim()) return;
  
  // 如果还没有创建 ChatBot 实例，先创建
  if (!chatbotId.value) {
    await createChatBot();
    if (!chatbotId.value) return; // 创建失败，直接返回
  }
  
  // 添加用户消息到对话历史
  messages.value.push({
    role: 'user',
    content: userInput.value
  });
  
  // 清空用户输入
  const userMessage = userInput.value;
  userInput.value = '';
  
  try {
    loading.value = true;
    error.value = '';
    
    // 调用后端 API 与 ChatBot 对话
    const response = await request('/api/chatbot/chat', 'POST', {
      chatbot_id: chatbotId.value,
      message: userMessage
    });
    
    // 添加 LLM 响应到对话历史
    messages.value.push({
      role: 'assistant',
      content: response.data.response
    });
  } catch (err) {
    error.value = '对话失败，请稍后重试';
    console.error('对话失败:', err);
    
    // 添加错误消息到对话历史
    messages.value.push({
      role: 'assistant',
      content: '抱歉，对话失败，请稍后重试'
    });
  } finally {
    loading.value = false;
  }
};

const copyChatbotId = () => {
  if (chatbotId.value) {
    navigator.clipboard.writeText(chatbotId.value)
      .then(() => {
        alert('ChatBot ID 已复制到剪贴板');
      })
      .catch(err => {
        console.error('复制失败:', err);
      });
  }
};

const clearAll = () => {
  systemPrompt.value = '';
  userInput.value = '';
  temperature.value = 0.7;
  topP.value = 0.9;
  maxTokens.value = 1000;
  frequencyPenalty.value = 0;
  presencePenalty.value = 0;
  stop.value = '';
  messages.value = [];
  chatbotId.value = '';
  error.value = '';
};
</script>

<style scoped>
.chat-history {
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 10px;
  min-height: 200px;
  max-height: 400px;
  overflow-y: auto;
  margin-bottom: 10px;
}

.message {
  margin-bottom: 10px;
  padding: 8px 12px;
  border-radius: 8px;
  max-width: 80%;
}

.message.user {
  background-color: #e3f2fd;
  align-self: flex-start;
  margin-left: auto;
  border-bottom-right-radius: 2px;
}

.message.assistant {
  background-color: #f1f1f1;
  align-self: flex-start;
  margin-right: auto;
  border-bottom-left-radius: 2px;
}

.message-role {
  font-weight: bold;
  margin-bottom: 4px;
  font-size: 12px;
  color: #666;
}

.message-content {
  font-size: 14px;
  line-height: 1.4;
}

.error-message {
  background-color: #ffebee;
  color: #c62828;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 15px;
  font-size: 14px;
}

.chatbot-id {
  display: flex;
  align-items: center;
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 8px 12px;
  font-family: monospace;
  font-size: 14px;
  word-break: break-all;
}

.copy-btn {
  margin-left: 10px;
  padding: 4px 8px;
  font-size: 12px;
  background-color: #e0e0e0;
  color: #333;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.copy-btn:hover {
  background-color: #d0d0d0;
}
</style>

<style scoped>
.params-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-top: 10px;
}

.param-item {
  flex: 1;
}

.param-item label {
  display: block;
  margin-bottom: 5px;
  font-weight: normal;
}

.param-item input[type="range"] {
  width: 100%;
}
</style>