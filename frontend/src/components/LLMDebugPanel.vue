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
    
    <!-- 发送按钮 -->
    <div class="button-group">
      <button @click="sendRequest" :disabled="!userInput.trim()">发送请求</button>
      <button @click="clearAll">清空对话</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const selectedModel = ref('gpt-3.5-turbo');
const systemPrompt = ref('');
const userInput = ref('');
const temperature = ref(0.7);
const topP = ref(0.9);
const maxTokens = ref(1000);
const frequencyPenalty = ref(0);
const presencePenalty = ref(0);
const stop = ref('');
const messages = ref([]);

const sendRequest = async () => {
  if (!userInput.value.trim()) return;
  
  // 添加用户消息到对话历史
  messages.value.push({
    role: 'user',
    content: userInput.value
  });
  
  // 清空用户输入
  const userMessage = userInput.value;
  userInput.value = '';
  
  // 模拟 LLM 响应
  setTimeout(() => {
    messages.value.push({
      role: 'assistant',
      content: `这是对"${userMessage}"的模拟响应。在实际实现中，这里会显示来自 OpenAI API 的真实响应。`
    });
  }, 1000);
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