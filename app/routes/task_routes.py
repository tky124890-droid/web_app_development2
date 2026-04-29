from flask import render_template, request, redirect, url_for, abort, flash
from . import task_bp
from app.models.task import TaskModel

@task_bp.route('/')
def index():
    """
    顯示所有任務的列表頁面。
    支援透過 request.args 取得 'search' 與 'status' 參數進行過濾。
    渲染 templates/tasks/index.html
    """
    search_query = request.args.get('search', '')
    status_filter = request.args.get('status', 'all')
    tasks = TaskModel.get_all_tasks(search_query=search_query, status_filter=status_filter if status_filter != 'all' else None)
    return render_template('tasks/index.html', tasks=tasks, search=search_query, status=status_filter)

@task_bp.route('/tasks/new', methods=['GET'])
def new_task():
    """
    顯示新增任務的表單頁面。
    渲染 templates/tasks/new.html
    """
    return render_template('tasks/new.html')

@task_bp.route('/tasks', methods=['POST'])
def create_task():
    """
    接收新增任務的表單資料。
    驗證資料後呼叫 Model 存入資料庫，成功後重導向至首頁 (/)。
    """
    title = request.form.get('title', '').strip()
    priority = request.form.get('priority', '中')
    tags = request.form.get('tags', '').strip()
    due_date = request.form.get('due_date', '').strip()

    if not title:
        flash('任務標題為必填欄位', 'danger')
        return redirect(url_for('tasks.new_task'))

    TaskModel.create_task(title=title, priority=priority, tags=tags, due_date=due_date)
    flash('任務建立成功', 'success')
    return redirect(url_for('tasks.index'))

@task_bp.route('/tasks/<int:id>/edit', methods=['GET'])
def edit_task(id):
    """
    顯示編輯特定任務的表單頁面。
    透過 ID 查詢任務，若不存在則回傳 404。
    渲染 templates/tasks/edit.html
    """
    task = TaskModel.get_task_by_id(id)
    if not task:
        abort(404)
    return render_template('tasks/edit.html', task=task)

@task_bp.route('/tasks/<int:id>/update', methods=['POST'])
def update_task(id):
    """
    接收編輯任務的表單資料。
    透過 ID 更新該筆任務，成功後重導向至首頁 (/)。
    """
    title = request.form.get('title', '').strip()
    priority = request.form.get('priority', '中')
    tags = request.form.get('tags', '').strip()
    due_date = request.form.get('due_date', '').strip()

    if not title:
        flash('任務標題為必填欄位', 'danger')
        return redirect(url_for('tasks.edit_task', id=id))

    success = TaskModel.update_task(task_id=id, title=title, priority=priority, tags=tags, due_date=due_date)
    if success:
        flash('任務更新成功', 'success')
    else:
        flash('任務更新失敗或找不到任務', 'danger')
        
    return redirect(url_for('tasks.index'))

@task_bp.route('/tasks/<int:id>/delete', methods=['POST'])
def delete_task(id):
    """
    刪除特定任務。
    透過 ID 刪除該筆任務，成功後重導向至首頁 (/)。
    """
    success = TaskModel.delete_task(id)
    if success:
        flash('任務已刪除', 'success')
    else:
        flash('任務刪除失敗', 'danger')
    return redirect(url_for('tasks.index'))

@task_bp.route('/tasks/<int:id>/toggle', methods=['POST'])
def toggle_task(id):
    """
    切換特定任務的完成狀態。
    透過 ID 變更其 is_completed 屬性，成功後重導向至首頁 (/)。
    """
    success = TaskModel.toggle_complete(id)
    if success:
        flash('狀態更新成功', 'success')
    else:
        flash('狀態更新失敗', 'danger')
    return redirect(url_for('tasks.index'))

@task_bp.route('/stats')
def stats():
    """
    顯示任務進度統計圖表。
    取得所有任務以計算完成比例等數據。
    渲染 templates/stats/index.html
    """
    pass
