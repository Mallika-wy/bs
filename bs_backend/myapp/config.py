class Config:
	"""
	通用配置
	"""
	# 本地数据库链接配置
	SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:2004wangyang@localhost/bs"
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	# 发送邮箱smtp设置
	mail_host = "smtp.163.com"           # 设置服务器
	mail_post = 465
	mail_user = "18205098642@163.com"     # 用户名
	mail_pass = "ZWqHSNX6XvtBiXXb"      # 口令

	fazz_threshold = 80
