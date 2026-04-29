# 任務管理系統 - 路由設計與頁面規劃

這份文件說明 Flask 應用程式的路由設計 (Routes)，包含 URL 路徑規劃、對應的處理邏輯與 Jinja2 模板，做為前後端實作的依據。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **首頁/任務列表** | GET | `/` | `tasks/index.html` | 顯示所有任務，支援查詢字串過濾 (`?search=`, `?status=`) |
| **新增任務頁面** | GET | `/tasks/new` | `tasks/new.html` | 顯示新增任務的表單 |
| **建立任務** | POST | `/tasks` | — | 接收表單，存入資料庫，成功後重導向至 `/` |
| **編輯任務頁面** | GET | `/tasks/<int:id>/edit` | `tasks/edit.html` | 顯示特定任務的編輯表單 |
| **更新任務** | POST | `/tasks/<int:id>/update`| — | 接收表單，更新資料庫，成功後重導向至 `/` |
| **刪除任務** | POST | `/tasks/<int:id>/delete`| — | 刪除特定任務，成功後重導向至 `/` |
| **切換狀態** | POST | `/tasks/<int:id>/toggle`| — | 切換特定任務的完成狀態，重導向回當前列表 |
| **進度統計圖表** | GET | `/stats` | `stats/index.html` | 顯示各類任務進度的統計圖表 |

## 2. 每個路由的詳細說明

### `GET /` (任務列表)
- **輸入**：URL 參數 `search` (字串), `status` ('active', 'completed', 'all')
- **處理邏輯**：呼叫 `TaskModel.get_all_tasks(search_query, status_filter)` 取得任務清單。
- **輸出**：渲染 `tasks/index.html`，並將任務清單 (`tasks`) 傳入模板。
- **錯誤處理**：無特定錯誤，若無任務則顯示空狀態。

### `GET /tasks/new` (新增任務表單)
- **輸入**：無
- **處理邏輯**：無特殊處理。
- **輸出**：渲染 `tasks/new.html` 顯示空白表單。

### `POST /tasks` (建立任務)
- **輸入**：表單欄位 `title`, `priority`, `tags`, `due_date`
- **處理邏輯**：驗證 `title` 是否存在，呼叫 `TaskModel.create_task(...)`。
- **輸出**：重新導向 (Redirect) 到 `/`。
- **錯誤處理**：若 `title` 驗證失敗，可閃現錯誤訊息 (flash) 並重新渲染表單。

### `GET /tasks/<int:id>/edit` (編輯任務表單)
- **輸入**：URL 變數 `id`
- **處理邏輯**：呼叫 `TaskModel.get_task_by_id(id)` 取得該任務資料。
- **輸出**：若任務存在，渲染 `tasks/edit.html` 並帶入資料。
- **錯誤處理**：若找不到任務，回傳 HTTP 404 錯誤畫面。

### `POST /tasks/<int:id>/update` (更新任務)
- **輸入**：URL 變數 `id`，表單欄位 `title`, `priority`, `tags`, `due_date`
- **處理邏輯**：呼叫 `TaskModel.update_task(...)` 更新該任務。
- **輸出**：重新導向 (Redirect) 到 `/`。
- **錯誤處理**：若找不到任務，回傳 404。

### `POST /tasks/<int:id>/delete` (刪除任務)
- **輸入**：URL 變數 `id`
- **處理邏輯**：呼叫 `TaskModel.delete_task(id)`。
- **輸出**：重新導向 (Redirect) 到 `/`。
- **錯誤處理**：若找不到任務，回傳 404。

### `POST /tasks/<int:id>/toggle` (切換狀態)
- **輸入**：URL 變數 `id`
- **處理邏輯**：呼叫 `TaskModel.toggle_complete(id)`。
- **輸出**：重新導向 (Redirect) 到 `/` 或使用者原本的瀏覽位置。

### `GET /stats` (統計圖表)
- **輸入**：無
- **處理邏輯**：呼叫 `TaskModel.get_all_tasks()` 取得所有任務，計算已完成與未完成的數量。
- **輸出**：渲染 `stats/index.html` 並帶入統計數據。

## 3. Jinja2 模板清單

所有的模板將放置於 `app/templates/` 目錄中，並將繼承自一個基礎佈局模板。

- `base.html`：包含 HTML 的 `<head>`、Navbar、引入 CSS 與 Chart.js，以及 `{% block content %}`。
- `tasks/index.html`：繼承 `base.html`，任務列表清單，包含過濾器與搜尋框。
- `tasks/new.html`：繼承 `base.html`，新增任務的表單頁面。
- `tasks/edit.html`：繼承 `base.html`，編輯任務的表單頁面。
- `stats/index.html`：繼承 `base.html`，顯示統計圖表。
- `404.html` (Optional)：繼承 `base.html`，顯示找不到頁面的錯誤訊息。
