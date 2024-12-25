docker打包涉及到三个部分：

1. 后端打包：
   1. 需要安装一系列包，支持drissionpage爬虫在docker中的正常运行
   2. 安装python包
   3. 运行flask
2. 前端打包：
   1. 安装node和nginx
   2. npm下载
   3. 运行vue项目
3. docker-compose
   1. 提供mysql
   2. 组合前端后端和数据库

需要的镜像：

1. node : 20
2. nginx : stable-perl
3. python : 3.10.15-slim
4. mysql : 5.7
