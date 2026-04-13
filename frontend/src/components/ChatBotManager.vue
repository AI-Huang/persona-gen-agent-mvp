<template>
  <div class="panel">
    <h2>ChatBot 管理</h2>
    
    <!-- 创建 ChatBot 表单 -->
    <div class="form-section">
      <h3>创建新的 ChatBot</h3>
      <form @submit.prevent="createChatBot">
        <div class="form-group">
          <label>名称：</label>
          <input type="text" v-model="newChatBot.name" placeholder="输入 ChatBot 名称" required>
        </div>
        <div class="form-group">
          <label>系统提示词：</label>
          <textarea v-model="newChatBot.systemPrompt" placeholder="输入系统提示词" required></textarea>
        </div>
        <div class="form-group">
          <label>模型：</label>
          <select v-model="newChatBot.model">
            <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
            <option value="gpt-4">GPT-4</option>
            <option value="gpt-4o">GPT-4o</option>
          </select>
        </div>
        <button type="submit">创建</button>
      </form>
    </div>
    
    <!-- ChatBot 列表 -->
    <div class="list-section">
      <h3>ChatBot 列表</h3>
      <div v-if="chatbots.length === 0" class="empty-state">
        暂无 ChatBot，请创建一个新的 ChatBot
      </div>
      <div v-else class="chatbot-list">
        <div 
          v-for="chatbot in chatbots" 
          :key="chatbot.id"
          class="chatbot-item"
        >
          <div class="chatbot-info">
            <h4>{{ chatbot.name }}</h4>
            <p>{{ chatbot.systemPrompt }}</p>
            <p class="model-info">模型：{{ chatbot.model }}</p>
          </div>
          <div class="chatbot-actions">
            <button @click="editChatBot(chatbot)" class="edit-btn">编辑</button>
            <button @click="deleteChatBot(chatbot.id)" class="delete-btn">删除</button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 编辑 ChatBot 对话框 -->
    <div v-if="editingChatBot" class="modal">
      <div class="modal-content">
        <h3>编辑 ChatBot</h3>
        <form @submit.prevent="updateChatBot">
          <div class="form-group">
            <label>名称：</label>
            <input type="text" v-model="editingChatBot.name" placeholder="输入 ChatBot 名称" required>
          </div>
          <div class="form-group">
            <label>系统提示词：</label>
            <textarea v-model="editingChatBot.systemPrompt" placeholder="输入系统提示词" required></textarea>
          </div>
          <div class="form-group">
            <label>模型：</label>
            <select v-model="editingChatBot.model">
              <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
              <option value="gpt-4">GPT-4</option>
              <option value="gpt-4o">GPT-4o</option>
            </select>
          </div>
          <div class="button-group">
            <button type="submit">保存</button>
            <button type="button" @click="editingChatBot = null">取消</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';

const chatbots = ref([]);
const newChatBot = ref({
  name: '',
  systemPrompt: '',
  model: 'gpt-3.5-turbo'
});
const editingChatBot = ref(null);

// 加载 ChatBot 列表
const loadChatBots = async () => {
  try {
    // 这里需要实现与后端的交互，获取 ChatBot 列表
    // 暂时模拟数据
    chatbots.value = [
      {
        id: '1',
        name: '测试机器人',
        systemPrompt: '你是一个 helpful 的助手',
        model: 'gpt-3.5-turbo'
      },
      {
        id: '2',
        name: '客服机器人',
        systemPrompt: '你是一个专业的客服代表，负责回答用户的问题',
        model: 'gpt-4'
      }
    ];
  } catch (error) {
    console.error('加载 ChatBot 列表失败:', error);
  }
};

// 创建 ChatBot
const createChatBot = async () => {
  try {
    // 这里需要实现与后端的交互，创建 ChatBot
    // 暂时模拟创建
    const newId = Date.now().toString();
    chatbots.value.push({
      id: newId,
      name: newChatBot.value.name,
      systemPrompt: newChatBot.value.systemPrompt,
      model: newChatBot.value.model
    });
    
    // 清空表单
    newChatBot.value = {
      name: '',
      systemPrompt: '',
      model: 'gpt-3.5-turbo'
    };
  } catch (error) {
    console.error('创建 ChatBot 失败:', error);
  }
};

// 编辑 ChatBot
const editChatBot = (chatbot) => {
  editingChatBot.value = { ...chatbot };
};

// 更新 ChatBot
const updateChatBot = async () => {
  try {
    // 这里需要实现与后端的交互，更新 ChatBot
    // 暂时模拟更新
    const index = chatbots.value.findIndex(cb => cb.id === editingChatBot.value.id);
    if (index !== -1) {
      chatbots.value[index] = { ...editingChatBot.value };
    }
    editingChatBot.value = null;
  } catch (error) {
    console.error('更新 ChatBot 失败:', error);
  }
};

// 删除 ChatBot
const deleteChatBot = async (id) => {
  if (confirm('确定要删除这个 ChatBot 吗？')) {
    try {
      // 这里需要实现与后端的交互，删除 ChatBot
      // 暂时模拟删除
      chatbots.value = chatbots.value.filter(cb => cb.id !== id);
    } catch (error) {
      console.error('删除 ChatBot 失败:', error);
    }
  }
};

// 组件挂载时加载数据
onMounted(() => {
  loadChatBots();
});
</script>

<style scoped>
.form-section {
  margin-bottom: 30px;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.form-group textarea {
  min-height: 100px;
  resize: vertical;
}

button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  background-color: #4CAF50;
  color: white;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #45a049;
}

.list-section {
  margin-top: 30px;
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: #666;
  background-color: #f9f9f9;
  border-radius: 8px;
}

.chatbot-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.chatbot-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.chatbot-info {
  flex: 1;
  margin-right: 20px;
}

.chatbot-info h4 {
  margin: 0 0 10px 0;
  color: #333;
}

.chatbot-info p {
  margin: 0 0 10px 0;
  color: #666;
  line-height: 1.4;
}

.model-info {
  font-size: 12px;
  color: #999;
  margin-top: 5px;
}

.chatbot-actions {
  display: flex;
  gap: 10px;
}

.edit-btn {
  background-color: #2196F3;
}

.edit-btn:hover {
  background-color: #0b7dda;
}

.delete-btn {
  background-color: #f44336;
}

.delete-btn:hover {
  background-color: #da190b;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 30px;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.modal-content h3 {
  margin-top: 0;
  margin-bottom: 20px;
}

.button-group {
  display: flex;
  gap: 10px;
  margin-top: 20px;
  justify-content: flex-end;
}

.button-group button:nth-child(2) {
  background-color: #999;
}

.button-group button:nth-child(2):hover {
  background-color: #777;
}
</style>