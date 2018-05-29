# 主页的逻辑

from . import index_blue
from info import redis_store
from flask import render_template, current_app, session
from info.models import User, News
from info import constants

@index_blue.route('/')
def index():
    """主页
        1.浏览器右上角用户信息：如果未登录主页右上角显示'登录、注册'；反之，显示'用户名 退出'
        2 主页点击排行
        """
    # 1.浏览器右上角用户信息
    # 1.1 判断用户是否登录，直接从session中取出user_id
    user_id = session.get('user_id', None)
    user = None
    if user_id:
        # 如果有user_id，说明登录中，就取出User模型对象信息
        try:
            user = User.query.get(user_id)
        except Exception as e:
            current_app.logger.error(e)

    # 2 主页点击排行  查询新闻数据  根据clikes 点击量属性实现倒叙
    # new_clicks = [News, News, News, News, News, News,]
    news_clicks = []
    try:
        news_clicks = News.query.order_by(News.clicks.desc()).limit(constants.CLICK_RANK_MAX_NEWS)
    except Exception as e:
        current_app.logger.error(e)



    # 构造模板上下文
    context = {
        'user': user,
        'news_clicks': news_clicks
    }

    return render_template('news/index.html', context=context)


@index_blue.route('/favicon.ico', methods=['GET'])
def favicon():
    '''渲染title 左侧的图标'''
    return current_app.send_static_file('news/favicon.ico')