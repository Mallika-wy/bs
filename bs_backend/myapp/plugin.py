from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_siwadoc import SiwaDoc
import queue


db = SQLAlchemy()
cors = CORS()
message_queue = queue.Queue()
siwa = SiwaDoc()
