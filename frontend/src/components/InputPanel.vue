<template>
  <div class="panel">
    <h2>请选择或描述人格需求</h2>
    
    <!-- 模板选择 -->
    <div class="form-group">
      <label>选择模板：</label>
      <select v-model="selectedTemplateId">
        <option value="">请选择</option>
        <option v-for="template in templates" :key="template.id" :value="template.id">
          {{ template.name }}
        </option>
      </select>
    </div>
    
    <!-- 自然语言输入 -->
    <div class="form-group">
      <label>或描述人格需求：</label>
      <textarea v-model="nlPrompt" placeholder="例如：专业药品助手、治愈陪伴、毒舌顾问"></textarea>
    </div>
    
    <!-- 场景选择 -->
    <div class="form-group">
      <label>使用场景：</label>
      <select v-model="scene">
        <option value="dify">Dify</option>
        <option value="api">OpenAI API</option>
      </select>
    </div>
    
    <!-- 生成按钮 -->
    <div class="button-group">
      <button @click="generateByTemplate" :disabled="!selectedTemplateId">按模板生成</button>
      <button @click="generateByNL" :disabled="!nlPrompt.trim()">按描述生成</button>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { request } from '../utils/request';

const router = useRouter();

const templates = ref([]);
const selectedTemplateId = ref('');
const nlPrompt = ref('');
const scene = ref('dify');

onMounted(async () => {
  const res = await request('/api/templates');
  if (res) {
    templates.value = res.data;
  }
});

const generateByTemplate = async () => {
  const res = await request('/api/generate-by-template', 'POST', {
    template_id: selectedTemplateId.value,
    scene: scene.value
  });
  if (res) {
    // 将结果存储在 sessionStorage 中，然后跳转到 output 页面
    sessionStorage.setItem('generationResult', JSON.stringify(res.data));
    router.push('/output');
  }
};

const generateByNL = async () => {
  const res = await request('/api/generate-by-nl', 'POST', {
    prompt: nlPrompt.value,
    scene: scene.value
  });
  if (res) {
    // 将结果存储在 sessionStorage 中，然后跳转到 output 页面
    sessionStorage.setItem('generationResult', JSON.stringify(res.data));
    router.push('/output');
  }
};
</script>