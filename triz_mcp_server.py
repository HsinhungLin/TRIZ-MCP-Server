######################################
# TRIZ MCP Server
######################################

#npx @modelcontextprotocol/inspector
import json
import os
from fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import List, Optional


# 初始化 FastMCP 伺服器
mcp = FastMCP("TRIZ_MCP_Server")

# ==========================================
# 靜態資料區 - 從 JSON 動態載入
# ==========================================
PRINCIPLES_FILE = "principles.json"
MATRIX_FILE = "matrix.json"

INVENTIVE_PRINCIPLES = {}
CONTRADICTION_MATRIX = {}

# 1. 載入發明原理
if os.path.exists(PRINCIPLES_FILE):
    try:
        with open(PRINCIPLES_FILE, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
            INVENTIVE_PRINCIPLES = {int(k): v for k, v in raw_data.items()}
        print(f"✅ 成功載入 {len(INVENTIVE_PRINCIPLES)} 個 TRIZ 發明原理！")
    except Exception as e:
        print(f"❌ 讀取 {PRINCIPLES_FILE} 失敗: {e}")
else:
    print(f"⚠️ 警告：找不到 {PRINCIPLES_FILE}。")

# 2. 載入矛盾矩陣
if os.path.exists(MATRIX_FILE):
    try:
        with open(MATRIX_FILE, "r", encoding="utf-8") as f:
            raw_matrix = json.load(f)
            for key_str, principles_list in raw_matrix.items():
                # 將 "1,2" 拆解為 1 和 2，並存成 tuple 作為 dict 的 key
                improving_id, worsening_id = key_str.split(',')
                CONTRADICTION_MATRIX[(int(improving_id), int(worsening_id))] = principles_list
        print(f"✅ 成功載入 {len(CONTRADICTION_MATRIX)} 組矛盾矩陣規則！")
    except Exception as e:
        print(f"❌ 讀取 {MATRIX_FILE} 失敗: {e}")
else:
    print(f"⚠️ 警告：找不到 {MATRIX_FILE}。")

# 3. 39 工程參數 (若未來也想轉成 parameters.json，可比照辦理)
ENGINEERING_PARAMETERS = {
   1: "移動物體的重量", 2: "靜止物體的重量", 3: "移動物體的長度", 4: "靜止物體的長度",
    5: "移動物體的面積", 6: "固定物體的面積", 7: "移動物體的體積", 8: "固定物體的體積",
    9: "速度", 10: "力量", 11: "張力/壓力", 12: "形狀", 
    13: "物體的穩定度", 14: "強度", 15: "移動物體的耐久性", 16: "固定物體的耐久性",
    17: "濕度", 18: "亮度", 19: "移動物體消耗的能量", 20: "固定物體消耗的能量",
    21: "功率", 22: "能量的浪費", 23: "物質的浪費", 24: "資訊的損失", 
    25: "時間的浪費", 26: "物質的數量", 27: "可靠度", 28: "量測的準確度", 
    29: "製造的準確度", 30: "物體外在有害因素", 31: "有害的副作用因素", 32: "易製造性",
    33: "易操作性", 34: "易維修性", 35: "適應性", 36: "設備的複雜性",
    37: "控制的複雜性", 38: "自動化的程度", 39: "生產力"
}

# ==========================================
# 物理矛盾：四大分離原則推薦的發明原理順序 (填入原理 ID)
# ==========================================
SEPARATION_PRINCIPLES_MAPPING = {
    "space": [1, 2, 3, 17, 13, 14, 7, 30, 4, 24, 26],       # 空間分離
    "time": [15, 10, 19, 11, 16, 21, 26, 18, 37, 34, 9, 20], # 時間分離
    "condition": [35, 32, 36, 31, 38, 39, 28, 29],    # 條件分離
    "scale": [1, 25, 40, 33, 12, 27, 5, 6, 23, 22, 13, 8]    # 規模/系統級別分離
}

# ==========================================
# 工具 1：九宮格分析工具
# ==========================================
@mcp.tool()
def triz_nine_windows(
    current_system: str,
    past_system: str = "",
    future_system: str = "",
    current_supersystem: str = "",
    past_supersystem: str = "",
    future_supersystem: str = "",
    current_subsystem: str = "",
    past_subsystem: str = "",
    future_subsystem: str = ""
) -> str:
    """
    進行九宮格（系統算盤）分析，從時間（過去/現在/未來）與空間（超系統/系統/子系統）維度全面檢視問題環境。
    """
    matrix = {
        "Supersystem (超系統)": {"Past": past_supersystem, "Present": current_supersystem, "Future": future_supersystem},
        "System (系統)": {"Past": past_system, "Present": current_system, "Future": future_system},
        "Subsystem (子系統)": {"Past": past_subsystem, "Present": current_subsystem, "Future": future_subsystem}
    }
    
    return f"九宮格分析建立成功：\n{matrix}"


# ==========================================
# 工具 2：功能分析工具
# ==========================================
class Interaction(BaseModel):
    source: str = Field(description="施加動作的組件（主體）")
    target: str = Field(description="接受動作的組件（客體）")
    action: str = Field(description="功能動作（動詞，例如：加熱、支撐）")
    function_type: str = Field(description="功能類型：useful_normal, useful_insufficient, useful_excessive, harmful")

@mcp.tool()
def triz_function_analysis(components: List[str], interactions: List[Interaction]) -> str:
    """
    對系統進行功能分析，定義組件間的作用關係並識別系統中的問題。
    """
    report = [f"系統組件 ({len(components)}): {', '.join(components)}", "\n交互作用分析:"]
    
    harmful_count = 0
    for idx, act in enumerate(interactions):
        report.append(f"{idx+1}. [{act.function_type}] {act.source} -> {act.action} -> {act.target}")
        if act.function_type == "harmful":
            harmful_count += 1
            
    report.append(f"\n分析總結：共發現 {harmful_count} 個有害功能待解決。")
    return "\n".join(report)

# ==========================================
# 工具 3：理想性分析 (最終理想解 IFR)
# ==========================================
@mcp.tool()
def triz_ideality_analysis(
    useful_purpose: str, 
    current_harms_and_costs: str, 
    available_resources: List[str]
) -> str:
    """
    進行理想性分析，定義系統的最終理想解（Ideal Final Result, IFR），並盤點可用資源以提升理想度。
    """
    # 建立 IFR 敘述式
    ifr_statement = (
        f"🌟 **最終理想解 (IFR) 定義**：\n"
        f"「該系統或物件『完全不存在』，但【{useful_purpose}】的功能卻被『自己』或『環境』完美地實現了，"
        f"同時完全消除了【{current_harms_and_costs}】的代價與副作用。」"
    )
    
    # 資源盤點與引導提示
    resources_str = "\n".join([f"- {res}" for res in available_resources])
    resource_prompt = (
        f"🛠️ **可用資源盤點 (X-Factor)**：\n{resources_str}\n\n"
        f"💡 **下一步思考引導**：\n"
        f"1. 上述清單中，哪個資源可以『免費』代為執行【{useful_purpose}】？\n"
        f"2. 我們能否利用上述資源，直接抵消或吸收【{current_harms_and_costs}】？\n"
        f"3. 理想度公式為：Ideality = Σ(有用功能) / [Σ(有害功能) + Σ(成本)]。請嘗試基於 IFR 提出 1~2 個顛覆傳統的構想。"
    )
    
    return f"【理想性分析報告】\n\n{ifr_statement}\n\n{resource_prompt}"


# ==========================================
# 工具 4：矛盾分析工具
# ==========================================
@mcp.tool()
def triz_contradiction_analysis(what_to_improve: str, what_worsens: str, problem_description: str = "") -> str:
    """
    分析系統的技術矛盾。輸入想改善的具體特徵與因此惡化的副作用。
    """
    return (
        f"矛盾模型建立完畢：\n"
        f"背景：{problem_description}\n"
        f"⬆️ 嘗試改善：{what_to_improve}\n"
        f"⬇️ 伴隨惡化：{what_worsens}\n\n"
        f"下一步建議：請呼叫 triz_get_engineering_parameters 查詢與這兩個描述最匹配的標準參數編號 (1-39)，然後使用 triz_query_matrix 尋找發明原理。"
    )


# ==========================================
# 工具 5：39工程參數查詢
# ==========================================
@mcp.tool()
def triz_get_engineering_parameters(parameter_id: Optional[int] = None, keyword: Optional[str] = None) -> dict:
    """
    查詢 TRIZ 39個標準工程參數。可獲取完整列表，或透過關鍵字、參數編號查詢。
    """
    if parameter_id and parameter_id in ENGINEERING_PARAMETERS:
        return {parameter_id: ENGINEERING_PARAMETERS[parameter_id]}
    
    if keyword:
        results = {k: v for k, v in ENGINEERING_PARAMETERS.items() if keyword.lower() in v.lower()}
        return results if results else {"message": f"找不到包含 '{keyword}' 的參數"}
        
    return ENGINEERING_PARAMETERS


# ==========================================
# 工具 6：40發明原理查詢 (維持上一版的案例支援邏輯)
# ==========================================
@mcp.tool()
def triz_get_inventive_principles(principle_id: Optional[int] = None, keyword: Optional[str] = None) -> dict:
    """
    查詢 TRIZ 40個發明原理。可依原理編號或關鍵字檢索其詳細含義與應用實例。
    """
    if not INVENTIVE_PRINCIPLES:
        return {"error": "系統尚未載入發明原理資料庫 (principles.json)。"}

    if principle_id and principle_id in INVENTIVE_PRINCIPLES:
        return {principle_id: INVENTIVE_PRINCIPLES[principle_id]}
        
    if keyword:
        keyword_lower = keyword.lower()
        results = {}
        for k, v in INVENTIVE_PRINCIPLES.items():
            match_name_desc = (keyword_lower in v["name"].lower() or keyword_lower in v["desc"].lower())
            match_examples = any(keyword_lower in ex.lower() for ex in v.get("examples", []))
            
            if match_name_desc or match_examples:
                results[k] = v
                
        return results if results else {"message": f"找不到包含 '{keyword}' 的發明原理或案例"}
        
    return INVENTIVE_PRINCIPLES


# ==========================================
# 工具 7：矛盾矩陣查詢 (提取 JSON 中的案例)
# ==========================================
@mcp.tool()
def triz_query_matrix(improving_parameter_id: int, worsening_parameter_id: int) -> dict:
    """
    根據阿奇舒勒矛盾矩陣，輸入「改善參數」與「惡化參數」的編號，交叉查詢推薦使用的發明原理。
    """
    if improving_parameter_id not in ENGINEERING_PARAMETERS or worsening_parameter_id not in ENGINEERING_PARAMETERS:
        return {"error": "請確認輸入的參數編號介於 1-39，且目前靜態資料庫中有該筆資料。"}
        
    principles_ids = CONTRADICTION_MATRIX.get((improving_parameter_id, worsening_parameter_id))
    
    if not principles_ids:
        return {
            "improving": ENGINEERING_PARAMETERS[improving_parameter_id],
            "worsening": ENGINEERING_PARAMETERS[worsening_parameter_id],
            "recommended_principles": [],
            "message": "此矛盾組合在標準矩陣中沒有推薦的發明原理，建議嘗試更換參數定義。"
        }
        
    recommended = []
    for pid in principles_ids:
        if pid in INVENTIVE_PRINCIPLES:
            principle = INVENTIVE_PRINCIPLES[pid]
            # 將案例用頓號串聯起來
            examples_str = "、".join(principle.get("examples", ["尚無案例"]))
            recommended.append(f"原理 {pid}: {principle['name']} - {principle['desc']} (案例：{examples_str})")
        else:
            recommended.append(f"原理 {pid} (待擴充至 principles.json)")
            
    return {
        "improving": ENGINEERING_PARAMETERS[improving_parameter_id],
        "worsening": ENGINEERING_PARAMETERS[worsening_parameter_id],
        "recommended_principles": recommended
    }

# ==========================================
# 工具 8：物理矛盾與四大分離原則分析 (整合發明原理推薦版)
# ==========================================
@mcp.tool()
def triz_physical_contradiction(
    component: str,
    state_1: str,
    reason_1: str,
    state_2: str,
    reason_2: str
) -> str:
    """
    進行物理矛盾分析。當同一個組件需要兩種相反狀態時，透過空間、時間、條件、規模等四大分離原則，並結合專屬的發明原理來尋找突破點。
    """
    # 建立一個小工具函數：把 ID 陣列轉換成帶有名稱的字串 (例如："1.分割、2.抽取")
    def get_recommended_principles(mapping_key):
        if not INVENTIVE_PRINCIPLES:
            return "（請先確認 principles.json 已正確載入）"
            
        p_ids = SEPARATION_PRINCIPLES_MAPPING.get(mapping_key, [])
        names = []
        for pid in p_ids:
            if pid in INVENTIVE_PRINCIPLES:
                # 只取括號前的中文名稱，讓版面更簡潔
                short_name = INVENTIVE_PRINCIPLES[pid]["name"].split(" ")[0]
                names.append(f"{pid}.{short_name}")
            else:
                names.append(f"{pid}.(待擴充)")
        return "、".join(names)

    report = [
        f"⚔️ **【物理矛盾模型已建立】**",
        f"核心組件：**{component}**",
        f"🔹 狀態 A：必須「{state_1}」，因為 {reason_1}",
        f"🔸 狀態 B：必須「{state_2}」，因為 {reason_2}\n",
        "💡 **【四大分離原則與對應發明原理求解引導】**",
        f"請 LLM 根據以下四個維度，並『優先使用』括號內推薦的發明原理，為「{component}」構思具體解法：",
        "",
        f"1. 🌌 **空間分離 (Separation in Space)**",
        f"   - 提問：我們能不能讓 {component} 的某個部位 {state_1}，而另一個部位 {state_2}？",
        f"   - 🎯 推薦發明原理：{get_recommended_principles('space')}",
        "",
        f"2. ⏱️ **時間分離 (Separation in Time)**",
        f"   - 提問：我們能不能讓 {component} 在某個時段 {state_1}，在另一個時段變成 {state_2}？",
        f"   - 🎯 推薦發明原理：{get_recommended_principles('time')}",
        "",
        f"3. 🎛️ **條件分離 (Separation upon Condition)**",
        f"   - 提問：當遇到什麼特定環境或物質條件時，能讓 {component} 自動從 {state_1} 切換成 {state_2}？",
        f"   - 🎯 推薦發明原理：{get_recommended_principles('condition')}",
        "",
        f"4. 🔬 **規模/系統級別分離 (Separation in Scale / Parts & Whole)**",
        f"   - 提問：如果 {component} 整體是 {state_1}，我們能不能讓組成它的微小結構（如分子、塗層）是 {state_2}？",
        f"   - 🎯 推薦發明原理：{get_recommended_principles('scale')}"
    ]
    
    return "\n".join(report)


# ==========================================
# 工具 9：創新方案總結與提案生成
# ==========================================
class SolutionProposal(BaseModel):
    solution_name: str = Field(description="方案名稱（簡短有力）")
    description: str = Field(description="方案的具體作法與執行細節")
    mechanism: str = Field(description="此方案如何運用了發明原理與環境資源來達成 IFR")

@mcp.tool()
def triz_innovation_proposal(
    original_problem: str,
    proposed_solutions: List[SolutionProposal],
    key_insights: str = "未提供",
    ideal_final_result: str = "未提供",
    applied_principles: List[str] = [],
    evaluation_and_next_steps: str = "未提供"
) -> str:
    """
    總結前面所有 TRIZ 分析工具的結果，將零散的洞見綜合成一份結構化、具體可行的創新方案建議書。
    """
    report = [
        "📑 **【TRIZ 創新方案建議書】**",
        "---",
        f"**📍 原始問題背景**\n{original_problem}\n",
        f"**🔍 核心分析洞見**\n{key_insights}\n",
        f"**🌟 最終理想解 (IFR) 與資源**\n{ideal_final_result}\n",
        f"**🛠️ 應用的發明原理**\n" + ", ".join(applied_principles) + "\n",
        "---",
        "**💡 具體解決方案**"
    ]
    
    for idx, sol in enumerate(proposed_solutions):
        report.append(f"### 方案 {idx+1}: {sol.solution_name}")
        report.append(f"**詳細作法**: {sol.description}")
        report.append(f"**運作機制**: {sol.mechanism}\n")
        
    report.append("---")
    report.append(f"**📋 評估與下一步**\n{evaluation_and_next_steps}")
    
    return "\n".join(report)

# ==========================================
# 註冊 MCP Prompt (終極完整版：支援物理/技術矛盾雙軌制)
# ==========================================
@mcp.prompt()
def triz(problem: str = "") -> str:
    """
    啟動完整的 TRIZ 創新解題流程（包含理想性分析與技術/物理矛盾雙軌制）
    """
    return (
        f"你現在是一位頂尖的 TRIZ 專家。我遇到了一個工程/技術問題：\n"
        f"【問題描述】：{problem if problem else '（請使用者補充問題）'}\n\n"
        f"請嚴格按照以下步驟引導我解決問題，並在每個步驟中主動呼叫對應的 TRIZ MCP 工具：\n"
        f"1. 呼叫 `triz_nine_windows` 展開系統視角。\n"
        f"2. 呼叫 `triz_function_analysis` 建立功能模型，找出核心的有用功能與有害/不足功能。\n"
        f"3. 呼叫 `triz_ideality_analysis` 定義「最終理想解 (IFR)」，發掘可用資源。\n"
        f"4. ⚖️ **矛盾判定與解決 (關鍵分支)**：\n"
        f"   - 如果問題是「同一個組件，同時需要兩種相反的物理狀態（例如：又要厚又要薄）」：請呼叫 `triz_physical_contradiction`，並運用四大分離原則構思解法。\n"
        f"   - 如果問題是「改善了參數 A，卻導致參數 B 變差」：請呼叫 `triz_contradiction_analysis`，接著依序呼叫 `triz_query_matrix` 與 `triz_get_inventive_principles` 找出發明原理。\n"
        f"5. 🌟 綜合以上所有步驟的討論，構思具體的解法，並呼叫 `triz_innovation_proposal` 產出一份正式的「TRIZ 創新方案建議書」交給我。\n\n"
        f"請先跟我打招呼，確認問題後，自動執行第 1 步。整個過程請保持對話互動，引導我思考，直到最後一步才生成總結報告。"
    )

# ==========================================
# 啟動伺服器
# ==========================================
if __name__ == "__main__":
    # 使用 stdio 傳輸層啟動 (標準 MCP 通訊方式)
    mcp.run(transport='stdio')
    # mcp.run(transport="http", host="0.0.0.0", port=8000)