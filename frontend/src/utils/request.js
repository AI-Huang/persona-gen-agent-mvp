// 简化请求工具，MVP够用，处理请求异常，适配前端对接
export const request = async (url, method = "GET", data = {}) => {
  const options = {
    method,
    headers: {
      "Content-Type": "application/json",
    },
  };
  // POST请求添加请求体
  if (method === "POST") {
    options.body = JSON.stringify(data);
  }
  try {
    const response = await fetch(url, options);
    const res = await response.json();
    // 处理后端返回的错误
    if (res.code !== 200) {
      alert(`请求失败：${res.message || "未知错误"}`);
      return null;
    }
    return res;
  } catch (error) {
    console.error("请求失败：", error);
    alert("请求失败，请检查后端服务是否启动");
    return null;
  }
};
