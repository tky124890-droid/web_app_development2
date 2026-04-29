import os
from flask import Flask
from .routes import task_bp
from .models.task import TaskModel

def create_app(test_config=None):
    # 建立 Flask 應用程式
    app = Flask(__name__, instance_relative_config=True)
    
    # 載入預設設定
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        DATABASE=os.path.join(app.instance_path, 'database.db'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # 確保 instance 資料夾存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 註冊 Blueprints
    app.register_blueprint(task_bp)

    # 初始化資料庫
    with app.app_context():
        TaskModel.create_table()

    return app
