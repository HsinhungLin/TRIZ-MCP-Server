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
