1. 初始进入登录界面，有另外的注册按钮

2. 登录成功后进入到搜索界面，有一个输入框以及一个确定按钮

3. 登录成功后，见进行京东和淘宝的模拟登录，获得京东和淘宝账号。登录成功后，保存cookie?如果登录不成功，就无法使用网站的所有功能。

4. 会有如下界面：

   - 搜索界面

     - 在搜索界面，点击一个商品，会进入到商品界面
     - 在商品界面，可以进行降价提醒功能，因为是定时查询价格，所以需要设置时间

   - 商品库界面

     因为一次爬虫代价很大，每次爬取的结果都需要保存下来，变成一个商品库

所需要的界面：

1. login
2. register
3. logintj
4. search
5. item
6. user
7. history

表：

- user
  - id
  - name
  - password
  - email
  - sex
  - address
  - phone
- product
  - id
  - carwler_id
  - name
  - image
  - category
- crawler
  - id
  - user_id
  - 
- account