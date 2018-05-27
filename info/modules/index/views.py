# 主页的逻辑

from . import index_blue

@index_blue.route('/')
def index():
    return 'index'