#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Project: Yi Energy (易能量演算法核心引擎)
Version: V1.0.4 (API 剛性校準終審版)
Author: Zheng Yi-shen (INFJ / QA/QC Engineer)
Description: 修正 lunar_python 底層 API 誤用錯誤（應為 getTime()），確保產線流暢通關。
"""

import datetime
import sys
from lunar_python import Lunar, Solar

class YiEnergyEngine:
    def __init__(self):
        # --- 核心規格定錨：原局地支矩陣 ---
        self.user_name = "Zheng Yi-shen"
        self.mbti = "INFJ"
        self.origin_matrix = {
            "shen": True,  # 申金 (食傷產線)
            "zi": True,    # 子水 (財星核心)
            "chen": True,  # 辰土 (水庫/本體)
            "xu": True     # 戌土 (火庫/自我)
        }

    def calculate_stresses(self, year: int, month: int, day: int, hour: int) -> dict:
        """
        核心演算法：輸入國曆時間，計算當前時空應力 (防裁剪字串優化)
        """
        # 1. 進行曆法轉換
        solar = Solar.fromYmdHms(year, month, day, hour, 0, 0)
        lunar = Lunar.fromSolar(solar)

        # 2. 提取時空四柱干支 (QC 剛性校準)
        eight_characters = lunar.getEightChar()
        year_ganzi = eight_characters.getYear()    
        month_ganzi = eight_characters.getMonth()  
        day_ganzi = eight_characters.getDay()      
        hour_ganzi = eight_characters.getTime()    # 剛性修正：lunar_python 標準時柱 API 為 getTime()

        y_gan, y_zhi = year_ganzi[0], year_ganzi[1]
        m_gan, m_zhi = month_ganzi[0], month_ganzi[1]
        d_gan, d_zhi = day_ganzi[0], day_ganzi[1]
        h_gan, h_zhi = hour_ganzi[0], hour_ganzi[1]

        all_zhi = [y_zhi, m_zhi, d_zhi, h_zhi]
        all_gan = [y_gan, m_gan, d_gan, h_gan]

        # 3. 初始化指標與狀態矩陣
        wealth_score = 1.0       
        stress_score = 1.0       
        active_statuses = []     
        logs = []

        # =====================================================================
        # 【演算法核心邏輯 A】：水為核心 (申子辰三合財星大匯流)
        # =====================================================================
        water_elements = all_zhi.count("子") + all_gan.count("壬") + all_gan.count("癸")
        if "子" in all_zhi:
            wealth_score += 2.5
            active_statuses.append("WEALTH_FLOW")
            logs.append("🌊 [申子辰] 財星大潮解鎖：\n       流時/日見子水引動主線程。")
        elif water_elements > 0:
            wealth_score += (water_elements * 0.8)
            active_statuses.append("WEALTH_READY")
            logs.append(f"💰 財星浮頭：天干見 {water_elements} 重壬/癸水透出。")

        if h_zhi in ["申", "酉"]:
            wealth_score += 1.0
            if "WEALTH_FLOW" not in active_statuses and "WEALTH_READY" not in active_statuses:
                active_statuses.append("PRODUCTION_ON")
            logs.append(f"🔨 [金生水] 食傷產線送料：\n       當前為 {h_zhi} 時，生財效率倍增。")

        # =====================================================================
        # 【演算法核心邏輯 B】：環境熔斷與轉軌 (辰戌相衝)
        # =====================================================================
        xu_count = all_zhi.count("戌")
        if xu_count > 0 and self.origin_matrix["chen"]:
            stress_score += (xu_count * 1.5)
            active_statuses.append("TURBULENCE")
            logs.append(f"💥 [辰戌大衝] 觸發：\n       逢 {xu_count} 重戌土衝擊辰土水庫。")

        if "乙" in all_gan and "庚" in all_gan:
            stress_score -= 1.0
            wealth_score += 0.5
            active_statuses.append("STRESS_VALVE")
            logs.append("🤝 [乙庚合金] 壓力分流閥啟動：\n       傷官吐秀，高壓轉化為大成。")

        # =====================================================================
        # 【演算法核心邏輯 C】：靈魂定錨與身強資產固化 (火土幫身)
        # =====================================================================
        if "午" in all_zhi and self.origin_matrix["xu"]:
            wealth_score += 0.5
            active_statuses.append("ANCHORED")
            logs.append("🔥 [午戌半合火局] 補能：\n       印星大點火，固化終身資產。")
        if "未" in all_zhi:
            if "辰" in all_zhi or self.origin_matrix["chen"]:
                active_statuses.append("BREAKTHROUGH")
                logs.append("🔨 [辰未相破]：打破舊循環，\n       建立全新家庭責任與架構。")

        # =====================================================================
        # 【演算法核心邏輯 D】：風險控制 (強木克土)
        # =====================================================================
        wood_count = all_zhi.count("寅") + all_zhi.count("卯")
        if wood_count >= 1:
            if "申" in all_zhi or self.origin_matrix["shen"]:
                stress_score += (wood_count * 1.2)
                active_statuses.append("LOW_POWER_DEFENSE")
                logs.append(f"🚨 [強木克土] 官殺體制極限施壓。\n🛡️ 啟動低耗能防禦，自動隔離雜訊。")

        # 4. 良率與邊界限制
        wealth_score = min(max(wealth_score, 1.0), 5.0)
        stress_score = min(max(stress_score, 1.0), 5.0)

        # 5. 彙整系統狀態矩陣
        if not active_statuses:
            system_status = "NORMAL"
        else:
            unique_statuses = []
            for status in active_statuses:
                if status not in unique_statuses:
                    unique_statuses.append(status)
            system_status = " + ".join(unique_statuses)

        return {
            "timestamp": f"{year}-{month:02d}-{day:02d} {hour:02d}:00",
            "ganzi_four_pillars": f"{year_ganzi} | {month_ganzi} | {day_ganzi} | {hour_ganzi}",
            "wealth_score": round(wealth_score, 2),
            "stress_score": round(stress_score, 2),
            "system_status": system_status,
            "engine_logs": logs
        }

if __name__ == "__main__":
    engine = YiEnergyEngine()

    if len(sys.argv) >= 2:
        try:
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
            now = datetime.datetime.now()
            y, m, d, h = now.year, now.month, now.day, now.hour
    else:
        now = datetime.datetime.now()
        y, m, d, h = now.year, now.month, now.day, now.hour

    report = engine.calculate_stresses(y, m, d, h)

    # 調整至 40 個字元寬度的剛性控制台面板
    print("=" * 42)
    print(f" ⚙️ 【Yi Energy V1.0.4】時空應力報告")
    print("=" * 42)
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
        print(f"     * [NORMAL] 產線平穩，無外部應力。")
    print("=" * 42)
