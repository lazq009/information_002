# 新闻详情   收藏   评论
from . import news_blue
from flask import render_template, session, current_app, g, abort, jsonify, request
from info.models import User, News, Comment, CommentLike
from info import constants, db, response_code
from info.utils.comment import user_login_data

@news_blue.route('/comment_like', methods=['POST'])
@user_login_data
def comment_like():
    '''评论和点赞'''
    # 1 获取登录的信息
    user = g.user
    if not user:
        return jsonify(errno=response_code.RET.SESSIONERR, errmsg='用户未登录')

    # 2 获取参数
    comment_id = request.json.get('comment_id')
    action = request.json.get('action')

    # 3 校验参数
    if not all([comment_id, action]):
        return jsonify(errno=response_code.RET.PARAMERR, errmsg='缺少参数')

    if action not in ['add','remove']:
        return jsonify(errno=response_code.RET.PARAMERR, errmsg='参数错误')

    # 4 查询要点赞的评论是否存在
    try:
        comment = Comment.query.get(comment_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=response_code.RET.PARAMERR, errmsg='参数错误')
    if not comment:
        return jsonify(errno=response_code.RET.NODATA, errmsg='评论不存在')

    # 5 点赞和取消点赞
    # 查询要点赞的记录是否存在
    comment_like_model = CommentLike.query.filter(CommentLike.comment_id==comment_id, CommentLike.user_id==user.id).first()
    if action == 'add':
        # 点赞
        if not comment_like_model:
            comment_like_model = CommentLike()
            comment_like_model.comment_id = comment_id
            comment_like_model.user_id = user.id
            # 提交新闻记录
            db.session.add(comment_like_model)

            # 累计点赞量
            comment.like_count += 1
    else:
        # 取消点赞
        if comment_like_model:
            # 删除该记录
            db.session.delete(comment_like_model)
            # 减少点赞量
            comment.like_count -= 1

    # 将点赞和取消点赞的数据同步到数据库
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)

    # 6 响应点赞和取消点赞的结果
    return jsonify(errno=response_code.RET.OK, errmsg='Ok')


@news_blue.route('/news_comment', methods=['POST'])
@user_login_data
def news_comment():
    '''新闻的评论和回复
    '''
    # 1 只要用户在登陆的状态下才能评论
    # 2 哪个用户平轮的是哪个新闻  新闻是否存在
    # 3 评论的内容提交数据库 并返给客户端
    # 4 评论的评论是评论的哪个评论

    # 1 获取用户登录的信息
    user = g.user
    if not user:
        return jsonify(errno=response_code.RET.SESSIONERR, errmsg='用户未登录')

    # 2 获取参数
    news_id = request.json.get('news_id')
    comment_content = request.json.get('comment')
    parent_id = request.json.get('parent_id')

    # 3 校验参数
    if not all([news_id, comment_content]):
        return jsonify(errno=response_code.RET.PARAMERR, errmsg='缺少参数')
    try:
        news_id = int(news_id)
        if parent_id:
            parent_id = int(parent_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=response_code.RET.PARAMERR, errmsg='参数错误')

    # 4 查询当前要评论的新闻是否存在
    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(response_code.RET.DBERR, errmsg='查询的新闻数据失败')
    if not news:
        return jsonify(errno=response_code.RET.NODATA, errmsg='新闻不存在')

    # 5 实现评论新闻和回复评论
    comment = Comment()
    comment.user_id = user.id
    comment.news_id = news_id
    comment.content = comment_content
    # 评论回复
    if parent_id:
        comment.parent_id = parent_id
    # 同步新闻评论和评论回复到数据库
    try:
        db.session.add(comment)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=response_code.RET.DBERR, errmsg='评论失败')
    # 为了将评论可以展示到界面上 需要将内容响应给用户
    data = {
        'comment': comment.to_dict()
    }

    # 6 响应评论新闻和回复评论结果
    return jsonify(errno=response_code.RET.OK, errmsg='评论成功', data=comment.to_dict())


@news_blue.route('/news_collect', methods=['POST'])
@user_login_data
def news_collect():
    """新闻收藏
    1.获取登录用户信息，因为收藏和取消收藏都是需要在登录状态下执行的
    2.接受参数
    3.检验参数
    4.查询当前要收藏或取消收藏的新闻是否存在
    5.实现收藏和取消收藏
    6.响应收藏和取消收藏的结果
    """
    # 一 只有用户在登陆的状太下才能收藏和取消收藏
    # 二 确定是哪个用户收藏了哪个新闻
    # 三 对于当前用户判断是否对当前新闻已收藏
    # 1 判断用户是否存在
    # 2 接受参数（用户  新闻 ）
    # 3 判断参数的合法性（要收藏 还是取消收藏）
    # 4 是收藏就是把收藏数存储到数据库
    # 5 取消旧数据库删除收藏数
    # 四 响应结果
    # 1 获取用户登陆信息
    user = g.user
    if not user:
        return jsonify(errno=response_code.RET.SESSIONERR, errmsg='用户未登陆')

    # 2 接受参数
    news_id = request.json.get('news_id')
    action = request.json.get('action')

    # 3 校验参数
    if not all([news_id, action]):
        return jsonify(errno=response_code.RET.PARAMERR, errmsg='缺少参数')
    if action not in ['collect', 'cancel_collect']:
        return jsonify(errno=response_code.RET.PARAMERR, errmsg='参数错误')

    # 4 查询当前要收藏或取消收藏的新闻是否存在
    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=response_code.RET.DBERR, errmsg='查询数据失败')
    if not news:
        return jsonify(errno=response_code.RET.NODATA, errmsg='新闻不存在')

    # 5 实现新闻的收藏和取消
    if action == 'collect':
        if news not in user.collection_news:
            user.collection_news.append(news)
    else:
        if news in user.collection_news:
            user.collection_news.remove(news)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=response_code.RET.DBERR, errmsg='操作失败')

    # 6 响应收藏和取消收藏的结果
    return jsonify(errno=response_code.RET.OK, errmsg='操作成功')


@news_blue.route('/detail/<int:news_id>')
@user_login_data
def news_detail(news_id):
    '''新闻详情
    1 获取登陆用户信息
    2.点击排行
    3.查询和展示新闻详情数据
    4.更新点击量
    5.判断是否收藏
    6 展示新闻评论和评论回复
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

    # 4.更新点击量
    news.clicks += 1
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()

    # 5.判断是否收藏:默认就是未收藏

    is_collected = False
    if user:
        if news in user.collection_news:
            is_collected = True

    # 6 展示新闻评论和评论回复
    comments = []
    try:
        comments = Comment.query.filter(Comment.news_id==news_id).order_by(Comment.create_time.desc()).all()
    except Exception as e:
        current_app.logger.error(e)

    # 查询该登录用户给该新闻的哪些评论点了赞
    comment_like_ids = []
    if user:
        try:
            # 查询用户点赞了哪些评论  comment_like = [模型对象]
            comment_likes = CommentLike.query.filter(CommentLike.user_id==user.id).all()
            # 取出所有被用户点赞的评论id  comment_like_ids == 【】
            comment_like_ids = [comment_like.comment_id for comment_like in comment_likes]
        except Exception as e:
            current_app.logger.error(e)

    # 为了读取模型类中的to_dict 封装后的结果  我选择遍历出每个模型类对象 转字典
    comment_dict_list = []
    for comment in comments:
        comment_dict = comment.to_dict()
        # 为了判断出每条评论中当前登录用户是否点赞了 给comment_dict 追加一个key(is-like), 默认未False
        comment_dict['is_like'] = False
        # if 当钱登录用户给这个评论点赞了就把is——like 设置为Ture
        #     comment_dict['is_like'] = True

        if comment.id in comment_like_ids:
            comment_dict['is_like'] = True

        comment_dict_list.append(comment_dict)

    context = {
        'user': user,
        'news_clicks': news_clicks,
        'news': news.to_dict(),
        'is_collected': is_collected,
        'comments': comment_dict_list


    }
    # 渲染新闻详情页
    return render_template('news/detail.html', context=context)