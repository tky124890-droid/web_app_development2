# 任務管理系統 - 流程圖與路徑對照

這份文件展示了任務管理系統的使用者操作流程、核心功能的系統序列圖，以及功能與 URL 路由的對照表，藉此梳理前端與後端的互動關係。

## 1. 使用者流程圖（User Flow）

以下圖表描述了使用者進入網站後，可以進行的各種操作路徑，涵蓋任務的 CRUD、狀態標記與統計查看等功能。

```mermaid
flowchart LR
    Start([使用者開啟網頁]) --> Index[首頁 - 任務列表]
    
    Index --> Action{選擇操作？}
    
    Action -->|搜尋與過濾| Filter[輸入關鍵字 / 選擇標籤] --> Index
    
    Action -->|新增任務| Add[點擊新增按鈕]
    Add --> Form[填寫任務表單<br>優先級、截止日、標籤]
    Form --> SubmitAdd[送出表單] --> Index
    
    Action -->|編輯任務| Edit[點擊編輯按鈕]
    Edit --> EditForm[修改任務內容]
    EditForm --> SubmitEdit[送出更新] --> Index
    
    Action -->|刪除任務| Delete[點擊刪除按鈕]
    Delete --> ConfirmDelete[確認刪除] --> Index
    
    Action -->|標記狀態| Toggle[勾選完成 / 取消完成] --> Index
    
    Action -->|查看統計| Stats[點擊統計按鈕]
    Stats --> Chart[進度圖表頁面]
    Chart -->|返回| Index
```

## 2. 系統序列圖（Sequence Diagram）

此序列圖展示了「使用者新增任務」時，瀏覽器、Flask 應用程式與資料庫之間的完整互動流程。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask (Controller)
    participant Model as Task Model
    participant DB as SQLite
    
    User->>Browser: 點擊「新增」並填寫任務表單
    User->>Browser: 點擊「送出」
    Browser->>Flask: POST /task/add (包含表單資料)
    Flask->>Model: 呼叫建立任務邏輯
    Model->>DB: INSERT INTO tasks (標題, 優先級, 截止日, 標籤...)
    DB-->>Model: 寫入成功，回傳新任務 ID
    Model-->>Flask: 任務建立完成
    Flask-->>Browser: 重導向 (Redirect) 到首頁 /
    Browser->>Flask: GET /
    Flask->>Model: 查詢所有任務清單
    Model->>DB: SELECT * FROM tasks
    DB-->>Model: 回傳任務資料集
    Model-->>Flask: 回傳 Task 物件陣列
    Flask->>Browser: 渲染 index.html 並回傳
    Browser-->>User: 顯示包含新任務的列表頁面
```

## 3. 功能清單對照表

本表列出系統所有主要功能與對應的 HTTP 方法及 URL 路徑規劃。

| 功能名稱 | 說明 | HTTP 方法 | URL 路徑 |
| :--- | :--- | :--- | :--- |
| **首頁與任務列表** | 顯示所有任務，支援關鍵字搜尋與標籤過濾 | GET | `/` |
| **新增任務頁面** | 顯示填寫任務內容的表單 | GET | `/task/add` |
| **送出新增任務** | 接收表單資料，並存入資料庫 | POST | `/task/add` |
| **編輯任務頁面** | 顯示既有任務內容以供修改 | GET | `/task/<int:id>/edit` |
| **送出更新任務** | 接收修改後的資料，並更新資料庫 | POST | `/task/<int:id>/edit` |
| **刪除任務** | 將特定任務從資料庫移除 | POST | `/task/<int:id>/delete` |
| **切換完成狀態** | 將任務標記為完成或未完成 | POST | `/task/<int:id>/toggle` |
| **進度統計圖表** | 顯示任務完成進度等相關統計圖表 | GET | `/stats` |
