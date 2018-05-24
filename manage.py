from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_wtf.csrf import CSRFProtect


class Config(object):
    ''' 配置文件的加载'''
    # 设置秘钥
    SECRET_KEY = 'UsJI6EtahFAkzf+BXqK9/Xn1qaisKAf2w4YIx1ZJIcrP3/Ue1BjyQeeA6bTfH6q0'
    # 开启debug 调试模式
    DEBUG = True
    # 配置mysql 数据库  实际开发时写真实的ip
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/information_002'
    # 开启是否追踪模式
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 配置redis 数据库 redis 模块不是flask的扩展 是python的一个包而已
    # 这里写的格式和SQLALchemy 的配置一样  但是  app 不会自动的读取  需要自己来读
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
app = Flask(__name__)
# 配置必须放前面
app.config.from_object(Config)
# 创建链接到数据库的对象
db = SQLAlchemy(app)
# 创建redis数据库的对象
redis_store = StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)
# 开启csrf 保护
CSRFProtect(app)

@app.route('/')
def index():
    # 测试下 redis
    redis_store.set('name', 'xjzx')

    return 'hello world'


if __name__ == '__main__':
    app.run()
