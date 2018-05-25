
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
# from info import app, db
from info import create_app

# from werkzeug.routing import BaseConverter

# class Config(object):
#     ''' 配置文件的加载'''
#     # 设置秘钥
#     SECRET_KEY = 'UsJI6EtahFAkzf+BXqK9/Xn1qaisKAf2w4YIx1ZJIcrP3/Ue1BjyQeeA6bTfH6q0'
#     # 开启debug 调试模式
#     DEBUG = True
#     # 配置mysql 数据库  实际开发时写真实的ip
#     SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/information_002'
#     # 开启是否追踪模式
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#
#     # 配置redis 数据库 redis 模块不是flask的扩展 是python的一个包而已
#     # 这里写的格式和SQLALchemy 的配置一样  但是  app 不会自动的读取  需要自己来读
#     REDIS_HOST = '127.0.0.1'
#     REDIS_PORT = 6379
#     # 配置flask_session 将session数据写入到服务器的redis数据库
#     # 指定session 数据库储存在redis
#     SESSION_TYPE = 'redis'
#     # 告诉session 服务器redis的位置
#     SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
#     # 是否将session签名后在存储
#     SESSION_USE_SIGNER = True
#     # 当SESSION_PERMANENT 为True 时 设置session 的有效期才可以成立  正好默认的就是true
#     PERMANENT_SESSION_LIFETIME = 60*60*24  #自定义为一天的有效期


# app = Flask(__name__)
# # 配置必须放前面
# app.config.from_object(Config)
# # 创建链接到数据库的对象
# db = SQLAlchemy(app)
# # 创建redis数据库的对象
# redis_store = StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)
# # 开启csrf 保护
# CSRFProtect(app)
# # 配置flask_session 将session 数据写入到redis数据库
# Session(app)

# 创建app
app = create_app('dev')
# 创建脚本管理器对象
manager = Manager(app)
# 让迁移和app 和 db 建立关联
# Migrate(app, db)
# 将迁移的脚本命令 添加到manager
# manager.add_command('mysql', MigrateCommand)


@app.route('/')
def index():
    # 测试下 redis
    # redis_store.set('name', 'xjzx')

    # 测试session
    from flask import session
    # 会将session 数据 写入到 浏览器的cookie
    session['name'] = 'xxx'
    return 'hello world'


if __name__ == '__main__':
    manager.run()
