FROM python:3.12-slim

WORKDIR /app

RUN rm -f /etc/apt/sources.list.d/debian.sources && \
    echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian bookworm main contrib non-free" > /etc/apt/sources.list && \
    echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian bookworm-updates main contrib non-free" >> /etc/apt/sources.list

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN python -m pip install --no-cache-dir uv -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . .

RUN uv sync \
    --index-url https://pypi.tuna.tsinghua.edu.cn/simple \
    --no-cache

RUN touch /.dockerenv

EXPOSE ${PORT}

CMD ["uv", "run", "python", "main.py"]