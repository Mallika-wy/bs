class Config:
	"""
	通用配置
	"""
	# 本地数据库链接配置
	# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root123@db:3306/bs'
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:2004wangyang@localhost:3306/bs'
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	# 发送邮箱smtp设置
	MAIL_HOST = "smtp.163.com"  # 设置服务器
	MAIL_PORT = 465
	MAIL_USER = "18205098642@163.com"  # 用户名
	MAIL_PASS = "ZWqHSNX6XvtBiXXb"  # 口令

	FUZZ_THRESHOLD = 50
