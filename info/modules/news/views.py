# 新闻详情   收藏   评论
from . import news_blue
from flask import render_template, session, current_app, g
from info.models import User, News
from info import constants
from info.utils.comment import user_login_data



@news_blue.route('/detail/<int:news_id>')
@user_login_data
def news_detail(news_id):
    '''新闻详情
    1 获取登陆用户信息
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

    context = {
        'user': user,
        'news_clicks': news_clicks

    }
    # 渲染新闻详情页
    return render_template('news/detail.html', context=context)