from redis import StrictRedis
import logging

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
    # 配置flask_session 将session数据写入到服务器的redis数据库
    # 指定session 数据库储存在redis
    SESSION_TYPE = 'redis'
    # 告诉session 服务器redis的位置
    SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    # 是否将session签名后在存储
    SESSION_USE_SIGNER = True
    # 当SESSION_PERMANENT 为True 时 设置session 的有效期才可以成立  正好默认的就是true
    PERMANENT_SESSION_LIFETIME = 60*60*24  #自定义为一天的有效期


class DevelopmentConfig(Config):
    '''开发环境下的配置'''
    pass
    LEVEL_LOG = logging.DEBUG


class ProductionConfig(Config):
    '''生产环境下的配置'''
    # 关闭调试模式
    DEBUG = False
    # 指定生产环境下的数据库
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/information_pro_002'
    LEVEL_LOG = logging.ERROR

class UnittestConfig(Config):
    '''开发环境下'''
    # 开启测试模式
    TESTING = True
    # 指定测试用数据库
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/information_pro_002'
    LEVEL_LOG = logging.DEBUG

# 准备工厂方法的create_app（参数）的原材料
configs = {
    'dev': DevelopmentConfig,
    'pro': ProductionConfig,
    'unit': UnittestConfig
}
