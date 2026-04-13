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
            <option value="gpt-5">GPT-5</option>
            <option value="gpt-5.1">GPT-5.1</option>
            <option value="gpt-5.2">GPT-5.2</option>
            <option value="gpt-5.4">GPT-5.4</option>
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
      <div v-else class="chatbot-table">
        <table>
          <thead>
            <tr>
              <th>完整ID</th>
              <th>短ID</th>
              <th>名称</th>
              <th>系统提示词</th>
              <th>模型</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="chatbot in chatbots" :key="chatbot.id">
              <td class="id-column">{{ chatbot.id }}</td>
              <td class="short-id-column">{{ chatbot.id.substring(0, 8) }}</td>
              <td class="name-column">{{ chatbot.name }}</td>
              <td class="system-prompt-column">{{ chatbot.systemPrompt }}</td>
              <td class="model-column">{{ chatbot.model }}</td>
              <td class="actions-column">
                <button @click="editChatBot(chatbot)" class="edit-btn">编辑</button>
                <button @click="deleteChatBot(chatbot.id)" class="delete-btn">删除</button>
              </td>
            </tr>
          </tbody>
        </table>
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
            <option value="gpt-5">GPT-5</option>
            <option value="gpt-5.1">GPT-5.1</option>
            <option value="gpt-5.2">GPT-5.2</option>
            <option value="gpt-5.4">GPT-5.4</option>
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
import { request } from '../utils/request';

const chatbots = ref([]);
const newChatBot = ref({
  name: '',
  systemPrompt: '',
  model: 'gpt-5'
});
const editingChatBot = ref(null);

// 加载 ChatBot 列表
const loadChatBots = async () => {
  try {
    const response = await request('/api/chatbot/list', 'GET');
    chatbots.value = response.data;
  } catch (error) {
    console.error('加载 ChatBot 列表失败:', error);
  }
};

// 创建 ChatBot
const createChatBot = async () => {
  try {
    const response = await request('/api/chatbot/create', 'POST', {
      name: newChatBot.value.name,
      system_prompt: newChatBot.value.systemPrompt,
      model: newChatBot.value.model
    });
    
    // 重新加载 ChatBot 列表
    await loadChatBots();
    
    // 清空表单
    newChatBot.value = {
      name: '',
      systemPrompt: '',
      model: 'gpt-5'
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
    await request(`/api/chatbot/update/${editingChatBot.value.id}`, 'PUT', {
      name: editingChatBot.value.name,
      system_prompt: editingChatBot.value.systemPrompt,
      model: editingChatBot.value.model
    });
    
    // 重新加载 ChatBot 列表
    await loadChatBots();
    
    editingChatBot.value = null;
  } catch (error) {
    console.error('更新 ChatBot 失败:', error);
  }
};

// 删除 ChatBot
const deleteChatBot = async (id) => {
  if (confirm('确定要删除这个 ChatBot 吗？')) {
    try {
      await request(`/api/chatbot/delete/${id}`, 'DELETE');
      
      // 重新加载 ChatBot 列表
      await loadChatBots();
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

.chatbot-table {
  overflow-x: auto;
}

.chatbot-table table {
  width: 100%;
  border-collapse: collapse;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.chatbot-table th,
.chatbot-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.chatbot-table th {
  background-color: #f2f2f2;
  font-weight: bold;
  color: #333;
}

.chatbot-table tr:hover {
  background-color: #f5f5f5;
}

.chatbot-table .id-column {
  width: 20%;
  font-family: monospace;
  font-size: 12px;
  word-break: break-all;
}

.chatbot-table .short-id-column {
  width: 10%;
  font-family: monospace;
  font-size: 12px;
}

.chatbot-table .name-column {
  width: 15%;
}

.chatbot-table .system-prompt-column {
  width: 30%;
  word-break: break-word;
}

.chatbot-table .model-column {
  width: 10%;
}

.chatbot-table .actions-column {
  width: 15%;
  white-space: nowrap;
}

.chatbot-table .actions-column button {
  margin-right: 5px;
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