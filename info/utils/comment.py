# 公共的工具类

from flask import session, current_app, g
from info.models import User


def do_rank(index):
    '''根据传入的索引 返回first  second third'''
    if index == 1:
        return 'first'
    elif index == '2':
        return 'second'
    elif index == '3':
        return 'third'
    else:
        return ''


def user_login_data(view_func):
    '''自定义装饰器获取登陆用户的信息'''
    def wrapper(*args, **kwargs):
        # 具体获取user_id,使用user_id查询user信息
        user_id = session.get('user_id', None)
        user = None
        if user_id:
            # 如果有user_id，说明登录中，就取出User模型对象信息
            try:
                user = User.query.get(user_id)
            except Exception as e:
                current_app.logger.error(e)

        # 是哟灵g变量，将查询到的用户user信息存储，在视图函数中可以再次使用g变量读取
        g.user = user

        # 调用被装饰器的函数
        return view_func(*args, **kwargs)

    return wrapper

# def user_login_data():
#     user_id = session.get('user_id', None)
#     user = None
#     if user_id:
#         # 如果有user_id，说明登录中，就取出User模型对象信息
#         try:
#             user = User.query.get(user_id)
#         except Exception as e:
#             current_app.logger.error(e)
#
#     return user
