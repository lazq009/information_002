from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from config import Config, DevelopmentConfig, ProductionConfig, UnittestConfig
from config import configs

# 创建SQLALchemy 对象
db = SQLAlchemy()

def create_app(config_name):
    '''根据外界传入的配置环境参数 创建app'''
    app = Flask(__name__)
    # 配置必须放前面
    app.config.from_object(configs[config_name])
    # 创建链接到数据库的对象
    # db = SQLAlchemy(app)
    db.init_app(app)
    # 创建redis数据库的对象
    redis_store = StrictRedis(host=configs[config_name].REDIS_HOST, port=configs[config_name].REDIS_PORT)
    # 开启csrf 保护
    CSRFProtect(app)
    # 配置flask_session 将session 数据写入到redis数据库
    Session(app)
    return app
