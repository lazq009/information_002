
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from info import create_app, db, models #这里导入models仅仅是为了在迁徙时让manage知道models的存在

# from werkzeug.routing import BaseConverter

# 创建app
app = create_app('dev')
# 创建脚本管理器对象
manager = Manager(app)
# 让迁移和app 和 db 建立关联
Migrate(app, db)
# 将迁移的脚本命令 添加到manager
manager.add_command('mysql', MigrateCommand)





if __name__ == '__main__':
    manager.run()
