# 注册和登录
from . import passport_blue
from flask import request,abort,current_app,make_response,jsonify
from info.utils.captcha.captcha import captcha
from info import redis_store, constants,response_code
import json,re,random
from info.libs.yuntongxun.sms import CCP


@passport_blue.route('/sms_code', methods=['POST'])
def sms_code():
    """发送短信验证码
    1.接受参数（手机号，图片验证码，图片验证码编号）
    2.校验参数（判断参数是否存在，手机号是否合法）
    3.查询服务器存储的图片验证码
    4.跟客户端传入的图片验证码对比
    5.如果对比成功，生成短信验证码数字
    6.调用CCP()单例类封装的发送短信的方法，发送短信
    7.将短信验证码存储到服务器(将来注册时要判断短信验证码是否正确)
    8.响应发送短信验证码的结果
    """
    # 1.接受参数（手机号，图片验证码，图片验证码编号）
    # '{'mobile':'17600992168','image_code':1234,'image_code_id':'uuid'}'
    # json_str = request.data
    # json_dict = json.loads(json_str)
    json_dict = request.json
    mobile = json_dict.get('mobile')
    image_code_clinet = json_dict.get('image_code')
    image_code_id = json_dict.get('image_code_id')

    # 2.校验参数（判断参数是否存在，手机号是否合法）
    if not all([mobile,image_code_clinet,image_code_id]):
        # '{'errno':'0', 'errmsg':'OK'}'
        return jsonify(errno=response_code.RET.PARAMERR, errmsg='缺少参数')
    if not re.match(r'^1[345678][0-9]{9}$', mobile):
        return jsonify(errno=response_code.RET.PARAMERR, errmsg='手机号格式错误')

    # 3.查询服务器存储的图片验证码
    try:
        image_code_server = redis_store.get('ImageCode:'+image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=response_code.RET.DBERR, errmsg='查询图片验证码失败')
    if not image_code_server:
        return jsonify(errno=response_code.RET.NODATA, errmsg='图片验证码不存在')

    # 4.跟客户端传入的图片验证码对比
    if image_code_server.lower() != image_code_clinet.lower():
        return jsonify(errno=response_code.RET.PARAMERR, errmsg='输入验证码有误')

    # 5.如果对比成功，生成短信验证码数字
    # '%06d' : 不够6位补0；比如，34--》000034
    sms_code = '%06d' % random.randint(0, 999999)

    # 6.调用CCP()单例类封装的发送短信的方法，发送短信
    result = CCP().send_template_sms(mobile, [sms_code, 5], 1)
    if result != 0:
        return jsonify(errno=response_code.RET.THIRDERR, errmsg='发送短信验证码失败')

    # 7.将短信验证码存储到服务器(将来注册时要判断短信验证码是否正确)
    try:
        redis_store.set('SMS:'+mobile, sms_code, constants.SMS_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=response_code.RET.DBERR, errmsg='存储短信验证码失败')

    #  8.响应发送短信验证码的结果
    return jsonify(errno=response_code.RET.OK, errmsg='发送短信验证码成功')


@passport_blue.route('/image_code')
def image_code():
    """提供图片验证码
    1.接受参数（图片验证码唯一标识uuid）
    2.校验参数（判断参数是否存在）
    3.生成图片验证码
    4.存储图片验证码
    5.将图片的类型指定为image/jpg
    6.响应图片验证码
    """
    # 1.接受参数（图片验证码唯一标识uuid）
    imageCodeId = request.args.get('imageCodeId')

    # 2.校验参数（判断参数是否存在）
    if not imageCodeId:
        abort(403)

    # 3.生成图片验证码:text写入到redis,image响应到浏览器
    name,text,image = captcha.generate_captcha()

    # 4.存储图片验证码
    try:
        redis_store.set('ImageCode:'+imageCodeId, text, constants.IMAGE_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        abort(500)

    # 5.将图片的类型指定为image/jpg
    response = make_response(image)
    # 设置响应头信息
    response.headers['Content-Type'] = 'image/jpg'

    # 6.响应图片验证码
    return response