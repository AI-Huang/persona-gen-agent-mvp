<template>
  <div class="panel">
    <h2>LLM 上手调试</h2>
    
    <!-- LLM 选择 -->
    <div class="form-group">
      <label>选择 LLM 模型：</label>
      <select v-model="selectedModel">
        <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
        <option value="gpt-4">GPT-4</option>
        <option value="gpt-4o">GPT-4o</option>
      </select>
    </div>
    
    <!-- 系统提示词 -->
    <div class="form-group">
      <label>系统提示词：</label>
      <textarea v-model="systemPrompt" placeholder="输入系统提示词..."></textarea>
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
          <input type="range" v-model.number="temperature" min="0" max="1" step="0.1">
        </div>
        <div class="param-item">
          <label>top_p: {{ topP }}</label>
          <input type="range" v-model.number="topP" min="0" max="1" step="0.1">
        </div>
      </div>
    </div>
    
    <!-- 发送按钮 -->
    <div class="button-group">
      <button @click="sendRequest" :disabled="!userInput.trim()">发送请求</button>
      <button @click="clearAll">清空</button>
    </div>
    
    <!-- 响应结果 -->
    <div v-if="response" class="output-section">
      <h3>LLM 响应：</h3>
      <div class="output-content">{{ response }}</div>
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
const response = ref('');

const sendRequest = async () => {
  // 这里需要实现与后端的交互，发送请求到 OpenAI API
  // 暂时模拟响应
  response.value = "这是 LLM 的模拟响应。在实际实现中，这里会显示来自 OpenAI API 的真实响应。";
};

const clearAll = () => {
  systemPrompt.value = '';
  userInput.value = '';
  response.value = '';
};
</script>

<style scoped>
.params-container {
  display: flex;
  gap: 20px;
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