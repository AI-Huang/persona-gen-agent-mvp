<template>
  <div class="container">
    <nav class="navbar">
      <div class="navbar-brand">人格提示词与OpenAI参数生成工具</div>
      <div class="navbar-buttons">
        <button 
          class="nav-button" 
          :class="{ active: activePanel === 'persona' }"
          @click="switchPanel('persona')"
        >
          人格提示词工具
        </button>
        <button 
          class="nav-button" 
          :class="{ active: activePanel === 'llm' }"
          @click="switchPanel('llm')"
        >
          LLM上手调试
        </button>
        <button 
          class="nav-button" 
          :class="{ active: activePanel === 'chatbot' }"
          @click="switchPanel('chatbot')"
        >
          ChatBot 管理
        </button>
      </div>
    </nav>
    
    <!-- 人格提示词工具面板 -->
    <div v-if="activePanel === 'persona'">
      <InputPanel @generate-result="handleGenerateResult" />
      <OutputPanel :result="result" />
    </div>
    
    <!-- LLM 上手调试面板 -->
    <div v-else-if="activePanel === 'llm'">
      <LLMDebugPanel />
    </div>
    
    <!-- ChatBot 管理面板 -->
    <div v-else-if="activePanel === 'chatbot'">
      <ChatBotManager />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import ChatBotManager from './components/ChatBotManager.vue';
import InputPanel from './components/InputPanel.vue';
import LLMDebugPanel from './components/LLMDebugPanel.vue';
import OutputPanel from './components/OutputPanel.vue';

const activePanel = ref('persona');
const result = ref(null);

const switchPanel = (panel) => {
  activePanel.value = panel;
};

const handleGenerateResult = (data) => {
  result.value = data;
};
</script>