from flask import Blueprint

# 註冊路由藍圖 (Blueprints)
task_bp = Blueprint('tasks', __name__)

from . import task_routes
