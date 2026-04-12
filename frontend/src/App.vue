<template>
  <div class="container">
    <nav class="navbar">
      <div class="navbar-brand">人格提示词与OpenAI参数生成工具</div>
      <div class="navbar-buttons">
        <button class="nav-button active">人格提示词工具</button>
        <button class="nav-button">LLM上手调试</button>
      </div>
    </nav>
    
    <InputPanel @generate-result="handleGenerateResult" />
    <OutputPanel :result="result" />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import InputPanel from './components/InputPanel.vue';
import OutputPanel from './components/OutputPanel.vue';

const result = ref(null);

const handleGenerateResult = (data) => {
  result.value = data;
};
</script>