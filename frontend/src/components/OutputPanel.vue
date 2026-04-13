<template>
  <div class="panel">
    <h2>生成结果（可直接复制使用）</h2>
    
    <div v-if="result">
      <!-- 匹配的模板提示 -->
      <div class="matched-template">
        匹配人格模板：{{ result.matched_template }}
      </div>
      
      <!-- 提示词输出 -->
      <div class="output-section">
        <h3>提示词：</h3>
        <div class="output-content">{{ result.prompt }}</div>
        <button class="copy-button" @click="copyToClipboard(result.prompt)">一键复制</button>
      </div>
      
      <!-- 参数输出 -->
      <div class="output-section">
        <h3>OpenAI参数：</h3>
        <div class="output-content">{{ JSON.stringify(result.params, null, 2) }}</div>
        <button class="copy-button" @click="copyToClipboard(JSON.stringify(result.params, null, 2))">一键复制</button>
      </div>
      
      <!-- API调用示例（仅API场景显示） -->
      <div v-if="result.api_example" class="output-section">
        <h3>API调用示例：</h3>
        <div class="api-example">{{ result.api_example }}</div>
        <button class="copy-button" @click="copyToClipboard(result.api_example)">一键复制</button>
      </div>
      
      <div class="button-group">
        <router-link to="/persona" class="nav-link">返回人格提示词工具</router-link>
      </div>
    </div>
    
    <div v-else class="output-section">
      <p>请选择模板或输入人格描述，点击生成按钮获取结果</p>
      <div class="button-group">
        <router-link to="/persona" class="nav-link">返回人格提示词工具</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const result = ref(null);

onMounted(() => {
  // 从 sessionStorage 中获取结果数据
  const storedResult = sessionStorage.getItem('generationResult');
  if (storedResult) {
    result.value = JSON.parse(storedResult);
  }
});

const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text);
    alert('复制成功！');
  } catch (err) {
    console.error('复制失败:', err);
    alert('复制失败，请手动复制');
  }
};
</script>

<style scoped>
.panel {
  height: calc(100vh - 120px); /* 减去导航栏和容器的 padding/margin */
  width: 100%;
  overflow: auto;
  padding: 15px;
  box-sizing: border-box;
}
</style>