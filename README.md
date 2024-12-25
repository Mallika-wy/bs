# docker 运行

```bash
$ docker-compose build
$ docker-compose up
```

我使用的爬虫是由python的drissionpage提供的，其很难部署到docker中，在无头浏览器上爬取京东和淘宝的数据很容易爬取不到信息。但是简单的注册和登录，信息编辑，md渲染等不涉及到爬虫的可以正常运行，京东淘宝登录也有2大概率可以成功。