import json
from pathlib import Path

updates = {
    "bubbles": {
        "traditional_chinese": "氣泡",
        "definition_cht": "指液體、固體或半固體介質中所包裹的氣體小囊體。在海洋、湖沼、冰雪與沉積環境中，氣泡的大小、含量與分布常用來分析氣體交換、冰體形成、聲學散射或過去環境條件。",
    },
    "bubbly ice": {
        "traditional_chinese": "含泡冰",
        "definition_cht": "內含大量微小氣泡的冰體。此類冰因凍結過程中空氣被封存而形成，常見於河冰、湖冰、海冰與冰川上部，並會影響冰的光學、力學與聲學性質。",
    },
    "bucket temperature": {
        "traditional_chinese": "桶測水溫",
        "definition_cht": "以桶自海面或其他水體取樣後，在桶內量得的水溫。此量測方式曾廣泛用於海面水溫觀測，其數值會受取樣深度、蒸發、日照與桶體材質等因素影響，常需進行觀測偏差訂正。",
    },
    "bucket thermometer": {
        "traditional_chinese": "桶測溫度計",
        "definition_cht": "用於量測桶取水樣溫度的溫度計，主要見於早期海面水溫觀測。其讀值代表桶內樣水溫度，可能因暴露時間、通風、蒸發冷卻與儀器反應時間而產生系統性偏差。",
    },
    "Buckingham Pi theory": {
        "traditional_chinese": "白金漢π定理",
        "definition_cht": "即 Buckingham pi theorem，為量綱分析的基本定理；指出若某物理問題涉及 n 個變數、k 個基本量綱，則可改寫為 n−k 個無因次參數之關係式。在大氣與流體力學中常用於建立相似律、縮尺實驗與經驗公式。",
    },
    "budget year": {
        "traditional_chinese": "收支年",
        "definition_cht": "用於統計某系統在一年內各項收入與支出、增加與減少或源與匯之總收支的年度期間。在冰川質量平衡、水量平衡與能量平衡研究中，起訖時間不一定與曆年一致，而常依觀測或物理週期設定。",
    },
    "budgets of atmospheric species": {
        "traditional_chinese": "大氣成分收支",
        "definition_cht": "指對特定大氣成分（如臭氧、水氣、二氧化碳、氣膠或化學反應物）之來源、生成、輸送、轉化、沉降與去除等過程進行定量收支分析，以說明其濃度分布、停留時間與時空變化。",
    },
    "buffer factor": {
        "traditional_chinese": "緩衝因子",
        "definition_cht": "在海洋碳化學中常指 Revelle factor，表示海水表層吸收二氧化碳時，海水總無機碳變化與二氧化碳分壓相對變化之比，用以衡量海洋對大氣二氧化碳增加的緩衝能力。",
    },
    "BUFR": {
        "traditional_chinese": "氣象資料通用二進位格式",
        "definition_cht": "Binary Universal Form for the Representation of meteorological data 的縮寫，為世界氣象組織維護的標準化二進位資料格式，用於交換氣象、海洋與相關觀測資料，能以表驅動方式編碼複雜觀測內容與中繼資料。",
    },
    "buildup index": {
        "traditional_chinese": "聚積指數",
        "definition_cht": "加拿大森林火險天氣指數系統中的一項指標，由腐植層濕度碼與乾旱碼組合而成，用以表示中深層可燃物可供燃燒的有效蓄積量，常用來評估火勢發展與燃料消耗潛勢。",
    },
    "bulk average": {
        "traditional_chinese": "整體平均",
        "definition_cht": "對某一有限體積、厚層、區域或樣本整體所取的平均值，用以代表其總體狀態，而不解析其中細部結構或局部起伏；在邊界層、海洋混合層與材料性質估算中皆常使用。",
    },
    "bulk heat flux": {
        "traditional_chinese": "整體熱通量",
        "definition_cht": "利用平均氣象量（如風速、溫差、濕度差與傳輸係數）依整體空氣動力公式估算之熱通量，常指海氣或地氣界面的感熱與潛熱交換，而非直接解析湍流脈動所得之通量。",
    },
    "bulk method": {
        "traditional_chinese": "整體法",
        "definition_cht": "以區域、層結或樣本的平均性質來估算通量、交換量或整體行為的方法，不直接解析小尺度湍流或微觀過程；在海氣通量、混合層與水文輸送估算中相當常見。",
    },
    "bulk mixed layer model": {
        "traditional_chinese": "整體混合層模式",
        "definition_cht": "將大氣或海洋混合層視為性質近乎均勻的單一整體，並以層平均溫度、濕度、動量或密度及其收支來描述混合層演變的簡化模式。",
    },
    "bulk modulus": {
        "traditional_chinese": "體積彈性模數",
        "definition_cht": "物質抵抗均勻受壓而產生體積改變的能力指標，定義為壓力變化與相對體積變化之比。於大氣、海洋與地球物理中常用以描述流體或固體介質的可壓縮性。",
    },
    "bulk Richardson number": {
        "traditional_chinese": "整體理查森數",
        "definition_cht": "以有限厚度層內的平均浮力差與平均風切變估算之無因次量，用以衡量層結穩定作用相對於機械擾動產生湍流的強弱，常用於判定邊界層穩定度與對流發展環境。",
    },
    "bulk stable boundary layer growth": {
        "traditional_chinese": "整體穩定邊界層增長",
        "definition_cht": "在整體邊界層模式中，以層平均收支與夾捲參數化描述夜間或穩定條件下邊界層厚度隨時間增加的過程，用於簡化分析穩定邊界層的形成與演變。",
    },
    "bulk transfer coefficient": {
        "traditional_chinese": "整體傳輸係數",
        "definition_cht": "整體空氣動力公式中的經驗或半經驗係數，用以連結平均風場與平均溫濕差，將動量、感熱或水氣等量的界面通量參數化；其值會隨穩定度、粗糙度與觀測高度而變化。",
    },
    "bulk transfer law": {
        "traditional_chinese": "整體傳輸定律",
        "definition_cht": "以平均風速及兩介面間的平均溫度、濕度或濃度差來表示動量、熱量或物質通量的參數化關係式，廣泛應用於海氣與地氣界面交換估算。",
    },
    "bulk turbulence scale": {
        "traditional_chinese": "整體湍流尺度",
        "definition_cht": "以層平均量、整體混合層特徵或主要收支量所定義的代表性湍流尺度，用來概括湍流渦動的典型強度、長度或時間尺度，常見於邊界層參數化與相似理論應用。",
    },
}

base = Path('/home/node/.openclaw/workspace/met_term')
for rel in ['data/b_terms_all_cht.json', 'data/glossary_all_cht.json']:
    path = base / rel
    data = json.loads(path.read_text(encoding='utf-8'))
    changed = 0
    for row in data:
        key = row.get('english')
        if key in updates:
            if row.get('traditional_chinese') != updates[key]['traditional_chinese'] or row.get('definition_cht') != updates[key]['definition_cht']:
                row.update(updates[key])
                changed += 1
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(rel, changed)
