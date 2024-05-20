# 使用 selenium 獲取 IG 追蹤者名單

替換內容：
1. 目標網頁，獲取單一帳號的追蹤者名單
2. 用來登入的 IG 帳號與密碼

程式碼區塊：
1. 登入 IG
2. 前往目標頁面
3. 等待 "Following" 按鈕出現並點擊
4. 模擬滾動到 following 列表最底部
5. 獲取 Instagram 追蹤者列表
6. 匯出成 CSV 文件

執行：
$ ```python3 main.py```
