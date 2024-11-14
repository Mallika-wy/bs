from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_siwadoc import SiwaDoc
import queue
import logging


db = SQLAlchemy()
cors = CORS()
message_queue = queue.Queue()
siwa = SiwaDoc()


# 配置日志级别和格式
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 创建一个文件处理器，并设置级别和格式
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

# 创建一个控制台处理器，并设置级别和格式
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)

# 获取一个日志记录器
logger = logging.getLogger(__name__)
logger.addHandler(file_handler)
logger.addHandler(console_handler)
