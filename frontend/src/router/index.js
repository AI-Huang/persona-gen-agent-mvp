import { createRouter, createWebHistory } from "vue-router";
import ChatApp from "../components/ChatApp.vue";
import ChatBotManager from "../components/ChatBotManager.vue";
import InputPanel from "../components/InputPanel.vue";
import LLMDebugPanel from "../components/LLMDebugPanel.vue";
import OutputPanel from "../components/OutputPanel.vue";
import SessionManager from "../components/SessionManager.vue";

// 创建路由配置
const routes = [
  {
    path: "/",
    redirect: "/persona",
  },
  {
    path: "/persona",
    name: "Persona",
    component: InputPanel,
    meta: {
      title: "人格提示词工具",
    },
  },
  {
    path: "/output",
    name: "Output",
    component: OutputPanel,
    meta: {
      title: "生成结果",
    },
  },
  {
    path: "/llm",
    name: "LLMDebug",
    component: LLMDebugPanel,
    meta: {
      title: "LLM 上手调试",
    },
  },
  {
    path: "/chatbot",
    name: "ChatBotManager",
    component: ChatBotManager,
    meta: {
      title: "ChatBot 管理",
    },
  },
  {
    path: "/session",
    name: "SessionManager",
    component: SessionManager,
    meta: {
      title: "会话管理",
    },
  },
  {
    path: "/apps",
    name: "ChatApp",
    component: ChatApp,
    meta: {
      title: "聊天应用",
    },
  },
];

// 创建路由器实例
const router = createRouter({
  history: createWebHistory(),
  routes,
});

// 导航守卫，设置页面标题
router.beforeEach((to, from, next) => {
  document.title = to.meta.title || "人格提示词与OpenAI参数生成工具";
  next();
});

export default router;
