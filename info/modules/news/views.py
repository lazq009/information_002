# 新闻详情   收藏   评论
from . import news_blue
from flask import render_template


@news_blue.route('/detail/<int:news_id>')
def news_detail(news_id):
    '''新闻详情'''


    # 渲染新闻详情页
    return render_template('news/detail.html')