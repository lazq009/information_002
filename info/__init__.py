
from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from config import Config, DevelopmentConfig, ProductionConfig, UnittestConfig
from config import configs
import logging
from logging.handlers import RotatingFileHandler
from flask_wtf import csrf
from info.utils.comment import do_rank



def setup_log(level):
    # 设置⽇志的记录等级
    # logging.basicConfig(level=logging.DEBUG) # 调试debug级
    logging.basicConfig(level=level)
    # 创建⽇志记录器，指明⽇志保存的路径、每个⽇志⽂件的最⼤⼤⼩、保存的⽇志⽂件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024*1024*100, backupCount=10)
    # 创建⽇志记录的格式 ⽇志等级 输⼊⽇志信息的⽂件名 ⾏数 ⽇志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的⽇志记录器设置⽇志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的⽇志⼯具对象（flask app使⽤的）添加⽇志记录器
    logging.getLogger().addHandler(file_log_handler)

# 创建SQLALchemy 对象
db = SQLAlchemy()
redis_store = None


def create_app(config_name):
    '''根据外界传入的配置环境参数 创建app'''

    # 集成日志  根据不同的配置环境  加载不同的日志等级
    setup_log(configs[config_name].LEVEL_LOG)

    app = Flask(__name__)
    # 配置必须放前面
    app.config.from_object(configs[config_name])
    # 创建链接到数据库的对象
    # db = SQLAlchemy(app)
    db.init_app(app)
    # 创建redis数据库的对象
    global redis_store
    redis_store = StrictRedis(host=configs[config_name].REDIS_HOST, port=configs[config_name].REDIS_PORT, decode_responses=True)
    # 开启csrf 保护
    CSRFProtect(app)

    # 业务一开始 就准备请求钩子  在每次的请求结束后向浏览器写入cookie
    @app.after_request
    def after_request(response):
        # 1 生成csrf_token
        csrf_token = csrf.generate_csrf()
        # 2 将csrf_token 写入浏览器
        response.set_cookie('csrf_token', csrf_token)
        return response

    # 将自定义的过滤器 函数  转换模板可以直接使用的过滤器
    app.add_template_filter(do_rank, 'rank')

    # 配置flask_session 将session 数据写入到redis数据库
    Session(app)
    # 将蓝图注册到app
    # 注意点   蓝图在哪里注册就哪里导入   避免在导入蓝图时某些变量还没加出来
    from info.modules.index import index_blue
    app.register_blueprint(index_blue)
    from info.modules.passport import passport_blue
    app.register_blueprint(passport_blue)

    return app
