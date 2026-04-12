<template>
  <div class="container">
    <h1>人格提示词与OpenAI参数生成工具（MVP版）</h1>
    
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