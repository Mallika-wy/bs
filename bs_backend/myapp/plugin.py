from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import queue


db = SQLAlchemy()
cors = CORS()
message_queue = queue.Queue()
