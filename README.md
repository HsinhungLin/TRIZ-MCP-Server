# 💡 TRIZ MCP Server (發明問題解決理論專家系統)

這是一個基於 [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) 標準開發的 TRIZ（Theory of Inventive Problem Solving）專家系統伺服器。

透過本專案，你可以讓 Claude 等支援 MCP 的大型語言模型 (LLM) 化身為頂尖的 TRIZ 專家。LLM 將不再依靠盲猜，而是能精準調用結構化的 TRIZ 分析工具、查詢 39 項工程參數、交叉比對矛盾矩陣，並提供包含具體案例的 40 項發明原理，最終為你的工程或技術問題產出一份完整的創新解決方案。

## ✨ 核心功能 (MCP Tools)

本伺服器提供了 9 個強大的 MCP 工具，涵蓋完整的 TRIZ 解題工作流：

1. **`triz_nine_windows` (九宮格分析)**：從時間（過去/現在/未來）與空間（超系統/系統/子系統）雙維度打破思維慣性。
2. **`triz_function_analysis` (功能分析)**：建立「組件-動作-對象」模型，標記有用、過度、不足與有害功能。
3. **`triz_ideality_analysis` (理想性分析)**：定義最終理想解 (IFR)，並盤點可用資源 (X-Factor)。
4. **`triz_physical_contradiction` (物理矛盾分析)**：應對單一組件的衝突狀態，提供空間、時間、條件、規模四大分離原則與對應的發明原理。
5. **`triz_contradiction_analysis` (技術矛盾分析)**：將現實困境轉化為標準的改善與惡化參數。
6. **`triz_query_matrix` (矛盾矩陣查詢)**：自動交叉比對阿奇舒勒矛盾矩陣，推薦突破性的發明原理。
7. **`triz_get_engineering_parameters` (39 工程參數查詢)**：支援關鍵字與編號檢索。
8. **`triz_get_inventive_principles` (40 發明原理查詢)**：支援關鍵字檢索，並內建具體應用案例。
9. **`triz_innovation_proposal` (創新方案總結)**：將前述分析收斂，自動生成結構化的創新提案報告。

除此之外，內建 `@mcp.prompt()` 提示詞模板，讓使用者能以類似 `/triz [你的問題]` 的快捷指令，一鍵啟動自動化專家顧問流程。

## 📂 專案結構

```text
triz-mcp-server/
├── triz_mcp_server.py    # MCP 伺服器主程式 (FastMCP)
├── principles.json       # 40 項發明原理與案例資料庫 (靜態資料)
├── matrix.json           # 39x39 矛盾矩陣資料庫 (靜態資料)
├── requirements.txt      # Python 依賴套件清單
└── README.md             # 專案說明檔
```
## 🚀 安裝與環境設定
複製專案到本地
```
Bash
git clone [https://github.com/你的帳號/triz-mcp-server.git](https://github.com/你的帳號/triz-mcp-server.git)
cd triz-mcp-server
```
建立並啟動虛擬環境 (強烈建議)

```
Bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```
安裝依賴套件
本專案使用 mcp 官方 SDK (包含 FastMCP 與 SSE 支援) 以及 pydantic。
```
Bash
pip install mcp[sse] pydantic uvicorn starlette sse-starlette
```
## 🔌 如何與 Claude Desktop 連線 (stdio 模式)
如果你想在官方的 Claude Desktop 軟體中直接使用 TRIZ 專家系統，請修改 Claude 的設定檔：

尋找設定檔 claude_desktop_config.json：

Windows: %APPDATA%\Claude\claude_desktop_config.json

macOS: ~/Library/Application Support/Claude/claude_desktop_config.json

在設定檔中加入以下內容（請替換為你電腦上的絕對路徑）：
```
JSON
{
  "mcpServers": {
    "triz-mcp": {
      "command": "C:/你的專案路徑/venv/Scripts/python.exe",
      "args": [
        "-X", 
        "utf8", 
        "C:/你的專案路徑/triz_mcp_server.py"
      ]
    }
  }
}
```
💡 提示：Windows 用戶強烈建議保留 -X utf8 參數，以避免 Python 在輸出 Emoji 或中文字元時發生 CP950 編碼錯誤。

重新啟動 Claude Desktop，點擊輸入框的「迴紋針 (Attach)」圖示，你就會看到 TRIZ 工具與 /triz 指令已經準備就緒！

## 🌐 啟動為 HTTP/SSE 網頁伺服器
如果你想將此 MCP 提供給 Web 應用程式、LangChain 或其他遠端 LLM 客戶端使用，請確保程式碼最下方使用的是 sse 傳輸模式：

```Python
if __name__ == "__main__":
    mcp.run(transport="sse", host="0.0.0.0", port=8000)
```
執行伺服器：

```Bash
python triz_mcp_server.py
```
## 伺服器將運行於 http://localhost:8000/sse
## 🧪 使用 MCP Inspector 測試工具
MCP 官方提供了視覺化的除錯介面 MCP Inspector，方便你在不消耗 LLM Token 的情況下單獨測試每一個工具的輸入與輸出。

如果是 stdio 模式：
```
Bash
npx @modelcontextprotocol/inspector python -X utf8 triz_mcp_server.py
```
如果是 SSE 模式 (需先啟動 Python 伺服器)：
```
Bash
npx @modelcontextprotocol/inspector sse http://localhost:8000/sse
```
執行後，開啟瀏覽器前往 http://localhost:5173 即可進行視覺化操作與測試。

## 📜 授權條款
本專案採用 MIT License 授權。歡迎自由使用、修改並貢獻更多 TRIZ 案例！
