# 新闻详情   收藏   评论
from . import news_blue
from flask import render_template, session, current_app, g, abort
from info.models import User, News
from info import constants
from info.utils.comment import user_login_data


@news_blue.route('/news_collect')
@user_login_data
def news_collect():
    """新闻收藏"""
    pass


@news_blue.route('/detail/<int:news_id>')
@user_login_data
def news_detail(news_id):
    '''新闻详情
    1 获取登陆用户信息
    2.点击排行
    3.查询和展示新闻详情数据
    :param news_id: 要查询和展示的新闻的id
    '''
    # 封装函数的形式获取user
    # from info.utils.comment import user_login_data
    # user = user_login_data()

    user = g.user
    # user_id = session.get('user_id', None)
    # user = None
    # if user_id:
    #     # 如果有user_id  说明登陆成功  取出User 模型类对象信息
    #     try:
    #         user = User.query.get(user_id)
    #     except Exception as e:
    #         current_app.logger.error(e)


    # 2 主页点击排行 查询新闻数据 根据clicks 点击量属性 实现倒叙
    news_clicks = []
    try:
        news_clicks = News.query.order_by(News.clicks.desc()).limit(constants.CLICK_RANK_MAX_NEWS)
    except Exception as e:
        current_app.logger.error(e)

    # 3.查询和展示新闻详情数据
    news = None
    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)
    if not news:
        # 将来会自定义一个友好的404页面
        abort(404)



    context = {
        'user': user,
        'news_clicks': news_clicks,
        'news': news.to_dict()

    }
    # 渲染新闻详情页
    return render_template('news/detail.html', context=context)