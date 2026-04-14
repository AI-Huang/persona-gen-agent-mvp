# 使用 Node.js 20 作为基础镜像
FROM node:20-alpine

# 设置工作目录
WORKDIR /app

# 设置 npm 源为清华源
RUN npm config set registry https://registry.npmmirror.com

# 复制项目文件
COPY . .

# 安装依赖
RUN npm install

# 构建项目
RUN npm run build

# 使用 nginx 作为生产服务器
FROM nginx:alpine

# 设置 nginx 源为清华源
RUN sed -i 's|http://dl-cdn.alpinelinux.org|https://mirrors.tuna.tsinghua.edu.cn|g' /etc/apk/repositories

# 安装依赖
RUN apk update && apk add --no-cache nginx

# 复制构建结果到 nginx 静态目录
COPY --from=0 /app/dist /usr/share/nginx/html

# 暴露端口（使用环境变量）
EXPOSE ${PORT}

# 启动 nginx
CMD ["nginx", "-g", "daemon off;"]