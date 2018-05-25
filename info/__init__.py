from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from config import Config, DevelopmentConfig, ProductionConfig, UnittestConfig


app = Flask(__name__)
# 配置必须放前面
app.config.from_object(DevelopmentConfig)
# 创建链接到数据库的对象
db = SQLAlchemy(app)
# 创建redis数据库的对象
redis_store = StrictRedis(host=DevelopmentConfig.REDIS_HOST, port=DevelopmentConfig.REDIS_PORT)
# 开启csrf 保护
CSRFProtect(app)
# 配置flask_session 将session 数据写入到redis数据库
Session(app)