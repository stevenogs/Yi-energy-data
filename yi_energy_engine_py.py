#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Project: Yi Energy (易能量演算法核心引擎)
Version: V1.0.1 (手機自動化防呆升級版)
Author: Zheng Yi-shen (INFJ / QA/QC Engineer)
Description: 全宇宙唯一針對 [申、子、辰、戌] 命盤與肉身大數據回測校準的能量觀測引擎。
             底層曆法標準完全對齊 JavaScript 版本 lunar.js。
"""

import datetime
import sys  # 引入系統參數模組，負責對接 iOS 捷徑
from lunar_python import Lunar, Solar

class YiEnergyEngine:
    def __init__(self):
        # --- 核心規格定錨：原局地支矩陣 ---
        self.user_name = "Zheng Yi-shen"
        self.mbti = "INFJ"
        self.origin_matrix = {
            "shen": True,  # 申金 (食傷產線/前導)
            "zi": True,    # 子水 (財星核心/主線程)
            "chen": True,  # 辰土 (水庫/本體硬體)
            "xu": True     # 戌土 (火庫/自我意識)
        }

    def calculate_stresses(self, year: int, month: int, day: int, hour: int) -> dict:
        """
        核心演算法：輸入國曆時間，透過同源萬年曆轉換，計算當前時空應力
        """
        # 1. 進行曆法轉換 (對齊 lunar.js 規格)
        solar = Solar.fromYmdHms(year, month, day, hour, 0, 0)
        lunar = Lunar.fromSolar(solar)

        # 2. 提取時空四柱干支
        eight_characters = lunar.getEightChar()
        year_ganzi = eight_characters.getYear()    # 流年
        month_ganzi = eight_characters.getMonth()  # 流月
        day_ganzi = eight_characters.getDay()      # 流日
        hour_ganzi = eight_characters.getTime()    # 流時

        # 拆解天干地支
        y_gan, y_zhi = year_ganzi[0], year_ganzi[1]
        m_gan, m_zhi = month_ganzi[0], month_ganzi[1]
        d_gan, d_zhi = day_ganzi[0], day_ganzi[1]
        h_gan, h_zhi = hour_ganzi[0], hour_ganzi[1]

        all_zhi = [y_zhi, m_zhi, d_zhi, h_zhi]
        all_gan = [y_gan, m_gan, d_gan, h_gan]

        # 3. 初始化三大指標係數
        wealth_score = 1.0       # 偏財/噴寶率 (1.0 - 5.0)
        stress_score = 1.0       # 內在應力值 (1.0 - 5.0)
        system_status = "NORMAL" # 系統初始狀態
        logs = []

        # =====================================================================
        # 【演算法核心邏輯 A】：水為核心 (申子辰三合財星大匯流)
        # =====================================================================
        water_elements = all_zhi.count("子") + all_gan.count("壬") + all_gan.count("癸")
        if "子" in all_zhi:
            wealth_score += 2.5
            logs.append("🌊 [申子辰] 財星大潮全面解鎖：流時/日見子水引動主線程。")
        elif water_elements > 0:
            wealth_score += (water_elements * 0.8)
            logs.append(f"💰 財星浮頭：天干見 {water_elements} 重壬/癸水透出。")

        if h_zhi in ["申", "酉"]:
            wealth_score += 1.0
            logs.append(f"🔨 [金生水] 食傷產線送料：當前為 {h_zhi} 時前導，吐秀生財效率倍增。")

        # =====================================================================
        # 【演算法核心邏輯 B】：環境熔斷與轉軌 (辰戌相衝)
        # =====================================================================
        xu_count = all_zhi.count("戌")
        if xu_count > 0 and self.origin_matrix["chen"]:
            stress_score += (xu_count * 1.5)
            system_status = "TURBULENCE"
            logs.append(f"💥 [辰戌大衝] 觸發：大環境逢 {xu_count} 重戌土衝擊原局辰土水庫，不破不立。")

        if "乙" in all_gan and "庚" in all_gan:
            stress_score -= 1.0
            wealth_score += 0.5
            logs.append("🤝 [乙庚合金] 壓力分流閥啟動：傷官吐秀，邏輯口條極致封頂，高壓轉化為大成。")

        # =====================================================================
        # 【演算法核心邏輯 C】：靈魂定錨與身強資產固化 (火土幫身)
        # =====================================================================
        if "午" in all_zhi and self.origin_matrix["xu"]:
            wealth_score += 0.5
            system_status = "ANCHORED"
            logs.append("🔥 [午戌半合火局] 補能：靈魂印星大點火，身強有力，固化終身核心資產。")
        if "未" in all_zhi:
            if "辰" in all_zhi or self.origin_matrix["chen"]:
                logs.append("🔨 [辰未相破] 發生：打破舊循環，全新家庭責任與資產架構建立。")

        # =====================================================================
        # 【演算法核心邏輯 D】：風險控制 (強木克土 · 惡意雜訊超載)
        # =====================================================================
        wood_count = all_zhi.count("寅") + all_zhi.count("卯")
        if wood_count >= 1:
            if "申" in all_zhi or self.origin_matrix["shen"]:
                stress_score += (wood_count * 1.2)
                system_status = "LOW_POWER_DEFENSE"
                logs.append(f"🚨 [強木克土/寅申衝] 警報：官殺體制極限施壓。")
                logs.append("🛡️ 系統啟動【低耗能防禦模式】：自動隔離外界惡意雜訊，靜待天道品保清算。")

        # 4. 良率與邊界限制 (Min/Max Clamp)
        wealth_score = min(max(wealth_score, 1.0), 5.0)
        stress_score = min(max(stress_score, 1.0), 5.0)

        # 5. 輸出產線檢驗報告
        return {
            "timestamp": f"{year}-{month:02d}-{day:02d} {hour:02d}:00",
            "ganzi_four_pillars": f"{year_ganzi}年 | {month_ganzi}月 | {day_ganzi}日 | {hour_ganzi}時",
            "wealth_score": round(wealth_score, 2),
            "stress_score": round(stress_score, 2),
            "system_status": system_status,
            "engine_logs": logs
        }

# =====================================================================
# 實時觀測調度端 (支援 iOS 捷徑自動防呆切換)
# =====================================================================
if __name__ == "__main__":
    engine = YiEnergyEngine()

    # 檢查是否有來自 iOS 捷徑傳入的引數
    if len(sys.argv) >= 2:
        try:
            # 將傳入的所有引數組合並清理 (相容空格、斜線或橫槓)
            raw_arg = " ".join(sys.argv[1:])
            cleaned_arg = raw_arg.replace("/", " ").replace("-", " ")
            time_parts = cleaned_arg.split()
            
            if len(time_parts) >= 4:
                y = int(time_parts[0])
                m = int(time_parts[1])
                d = int(time_parts[2])
                h = int(time_parts[3])
            else:
                raise ValueError
        except Exception:
            # 萬一捷徑字串解析失敗，觸發安全防護：直接抓取手機當前系統時間
            now = datetime.datetime.now()
            y, m, d, h = now.year, now.month, now.day, now.hour
    else:
        # 【終極防呆模式】如果捷徑沒傳參數（放空），直接由 Python 在本地端獲取當前時間
        now = datetime.datetime.now()
        y, m, d, h = now.year, now.month, now.day, now.hour

    # 執行當前時空的動態應力演算
    report = engine.calculate_stresses(y, m, d, h)

    # 輸出符合 scannability 的精美終端品保報告
    print("=" * 60)
    print(f" ⚙️ 【Yi Energy V1.0】實時時空應力觀測報告")
    print("=" * 60)
    print(f" 👑 系統狀態 : {report['system_status']}")
    print(f" ├─ 觀測時間 : {report['timestamp']}")
    print(f" ├─ 曆法四柱 : {report['ganzi_four_pillars']}")
    print(f" ├─ 財氣噴寶 : {report['wealth_score']} / 5.0")
    print(f" ├─ 內在應力 : {report['stress_score']} / 5.0")
    print(f" └─ 時空日誌 : ")
    if report['engine_logs']:
        for log in report['engine_logs']:
            print(f"     * {log}")
    else:
        print(f"     * [NORMAL] 產線運行平穩，無特殊外部應力引動。")
    print("=" * 60)
