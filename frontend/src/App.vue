<template>
  <div class="container">
    <nav class="navbar">
      <div class="navbar-brand">人格提示词与OpenAI参数生成工具</div>
      <div class="navbar-buttons">
        <router-link to="/persona" class="nav-link" active-class="active">
          人格提示词工具
        </router-link>
        <router-link to="/llm" class="nav-link" active-class="active">
          LLM上手调试
        </router-link>
        <router-link to="/chatbot" class="nav-link" active-class="active">
          ChatBot 管理
        </router-link>
        <router-link to="/session" class="nav-link" active-class="active">
          会话管理
        </router-link>
        <router-link to="/apps" class="nav-link" active-class="active">
          聊天应用
        </router-link>
      </div>
    </nav>
    
    <!-- 主内容区域 -->
    <div class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const result = ref(null);

const handleGenerateResult = (data) => {
  result.value = data;
};
</script>