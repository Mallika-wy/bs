FROM python:3.10.15-slim

# 设置工作目录
WORKDIR /app

# 复制 requirements.txt 文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件到工作目录
COPY . .

# 暴露 Flask 应用的端口
EXPOSE 5000

# 初始化数据库
# RUN flask db init
# RUN flask db migrate
# RUN flask db upgrade

# 使用 Flask 运行应用
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]