import sqlite3
import os

# 預設資料庫路徑 (instance/database.db)
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')

class TaskModel:
    @staticmethod
    def get_connection():
        # 確保 instance 資料夾存在
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # 讓查詢結果能像 dict 一樣操作
        return conn

    @staticmethod
    def create_table():
        """建立 tasks 資料表"""
        with TaskModel.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    priority TEXT DEFAULT '中',
                    tags TEXT DEFAULT '',
                    due_date TEXT,
                    is_completed INTEGER NOT NULL DEFAULT 0,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    @staticmethod
    def create_task(title, priority='中', tags='', due_date=None):
        """新增任務"""
        with TaskModel.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO tasks (title, priority, tags, due_date)
                VALUES (?, ?, ?, ?)
            ''', (title, priority, tags, due_date))
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def get_all_tasks(search_query=None, status_filter=None):
        """取得所有任務，支援關鍵字與狀態過濾"""
        with TaskModel.get_connection() as conn:
            cursor = conn.cursor()
            query = 'SELECT * FROM tasks WHERE 1=1'
            params = []
            
            if search_query:
                query += ' AND (title LIKE ? OR tags LIKE ?)'
                params.extend([f'%{search_query}%', f'%{search_query}%'])
                
            if status_filter == 'completed':
                query += ' AND is_completed = 1'
            elif status_filter == 'active':
                query += ' AND is_completed = 0'
                
            query += ' ORDER BY is_completed ASC, due_date ASC, created_at DESC'
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def get_task_by_id(task_id):
        """依 ID 取得單一任務"""
        with TaskModel.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    @staticmethod
    def update_task(task_id, title, priority, tags, due_date):
        """更新任務內容"""
        with TaskModel.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE tasks
                SET title = ?, priority = ?, tags = ?, due_date = ?
                WHERE id = ?
            ''', (title, priority, tags, due_date, task_id))
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def toggle_complete(task_id):
        """切換任務完成狀態"""
        with TaskModel.get_connection() as conn:
            cursor = conn.cursor()
            # 先取得目前狀態
            cursor.execute('SELECT is_completed FROM tasks WHERE id = ?', (task_id,))
            row = cursor.fetchone()
            if row:
                new_status = 0 if row['is_completed'] else 1
                cursor.execute('UPDATE tasks SET is_completed = ? WHERE id = ?', (new_status, task_id))
                conn.commit()
                return True
            return False

    @staticmethod
    def delete_task(task_id):
        """刪除特定任務"""
        with TaskModel.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            conn.commit()
            return cursor.rowcount > 0
