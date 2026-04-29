from flask import render_template, request, redirect, url_for, abort, flash
from . import task_bp
# 之後實作時會引入: from app.models.task import TaskModel

@task_bp.route('/')
def index():
    """
    顯示所有任務的列表頁面。
    支援透過 request.args 取得 'search' 與 'status' 參數進行過濾。
    渲染 templates/tasks/index.html
    """
    pass

@task_bp.route('/tasks/new', methods=['GET'])
def new_task():
    """
    顯示新增任務的表單頁面。
    渲染 templates/tasks/new.html
    """
    pass

@task_bp.route('/tasks', methods=['POST'])
def create_task():
    """
    接收新增任務的表單資料。
    驗證資料後呼叫 Model 存入資料庫，成功後重導向至首頁 (/)。
    """
    pass

@task_bp.route('/tasks/<int:id>/edit', methods=['GET'])
def edit_task(id):
    """
    顯示編輯特定任務的表單頁面。
    透過 ID 查詢任務，若不存在則回傳 404。
    渲染 templates/tasks/edit.html
    """
    pass

@task_bp.route('/tasks/<int:id>/update', methods=['POST'])
def update_task(id):
    """
    接收編輯任務的表單資料。
    透過 ID 更新該筆任務，成功後重導向至首頁 (/)。
    """
    pass

@task_bp.route('/tasks/<int:id>/delete', methods=['POST'])
def delete_task(id):
    """
    刪除特定任務。
    透過 ID 刪除該筆任務，成功後重導向至首頁 (/)。
    """
    pass

@task_bp.route('/tasks/<int:id>/toggle', methods=['POST'])
def toggle_task(id):
    """
    切換特定任務的完成狀態。
    透過 ID 變更其 is_completed 屬性，成功後重導向至首頁 (/)。
    """
    pass

@task_bp.route('/stats')
def stats():
    """
    顯示任務進度統計圖表。
    取得所有任務以計算完成比例等數據。
    渲染 templates/stats/index.html
    """
    pass
