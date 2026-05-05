import json
from pathlib import Path

updates = {
    "captive balloon sounding": {
        "traditional_chinese": "系留氣球探空",
        "definition_cht": "利用繫留於地面的氣球搭載儀器進行的高空或邊界層觀測，用以測定溫度、濕度、風或其他氣象要素，常見於微氣象與中尺度研究。",
    },
    "capture": {
        "traditional_chinese": "截取",
        "definition_cht": "在地下水學中，指因抽水使地下水位或測壓面下降，而將原本來自含水層邊界補注來源的水量轉移至井或抽水區的現象。",
    },
    "carabiné": {
        "traditional_chinese": "卡拉比內風",
        "definition_cht": "法國與西班牙對一種突發而猛烈強風的地方性名稱，亦作 brisa carabinera 或 brise carabinee。",
    },
    "carbon": {
        "traditional_chinese": "碳",
        "definition_cht": "化學元素，符號為 C，為大氣、海洋、生態與地球化學循環中的關鍵成分；常以二氧化碳、有機物、碳酸鹽等形式參與碳循環。",
    },
    "carbon assimilation": {
        "traditional_chinese": "碳同化",
        "definition_cht": "生物系統將大氣中的二氧化碳或其他無機碳吸收並轉化為有機物的過程，通常透過光合作用完成。",
    },
    "carbon bond mechanism": {
        "traditional_chinese": "碳鍵機制",
        "definition_cht": "一種用於大氣有機化學模擬的集總化學機制，常應用於都市空氣污染模式；其特色是依碳原子的鍵結環境來表示有機反應物。",
    },
    "carbon budget": {
        "traditional_chinese": "碳收支",
        "definition_cht": "某一碳庫內碳含量因輸入與輸出通量而產生的淨變化；在氣候研究中亦可延伸指特定升溫目標下容許的累積排放量。",
    },
    "carbon dioxide": {
        "traditional_chinese": "二氧化碳",
        "definition_cht": "化學式為 CO2 的無色氣體，為乾空氣中的重要微量成分，也是關鍵溫室氣體；可溶於海水，並透過光合作用與呼吸作用參與全球碳循環。",
    },
    "Carbon dioxide atmospheric concentrations": {
        "traditional_chinese": "大氣二氧化碳濃度",
        "definition_cht": "指大氣中二氧化碳的含量，通常以體積混合比或乾空氣莫耳分率表示，常用單位為百萬分率（ppmv 或 ppm）。",
    },
    "carbon dioxide band": {
        "traditional_chinese": "二氧化碳吸收帶",
        "definition_cht": "電磁波譜中二氧化碳對大氣紅外輻射傳輸具有顯著影響的波段，其強吸收中心約位於 14.7 微米附近。",
    },
    "carbon dioxide equivalence": {
        "traditional_chinese": "二氧化碳當量",
        "definition_cht": "用以將不同溫室氣體對溫室效應或輻射強迫的貢獻換算成相當於二氧化碳的濃度或排放量之表示方式，常用於比較各氣體的相對氣候影響。",
    },
    "carbon dioxide fertilization": {
        "traditional_chinese": "二氧化碳施肥",
        "definition_cht": "藉由提高植物或作物冠層周圍空氣中的二氧化碳濃度，以促進光合作用與生長表現的處理或現象。",
    },
    "carbon dioxide fertilizing effect": {
        "traditional_chinese": "二氧化碳施肥效應",
        "definition_cht": "植物或作物對二氧化碳施肥所呈現的反應，例如產量提升、用水效率增加、固氮增強，或對低溫與弱光條件的部分補償。",
    },
    "carbon disulfide": {
        "traditional_chinese": "二硫化碳",
        "definition_cht": "化學式為 CS2 的還原性含硫氣體，主要來自工業製程，也有部分天然排放；進入大氣後可被氫氧自由基氧化，並多轉化為羰基硫。",
    },
    "carbon monoxide": {
        "traditional_chinese": "一氧化碳",
        "definition_cht": "化學式為 CO 的無色無味且具毒性的氣體，常為有機物不完全燃燒或氧化的中間產物；大氣中濃度變化可反映燃燒排放與光化學過程。",
    },
    "carbon pool": {
        "traditional_chinese": "碳庫",
        "definition_cht": "生物地球化學循環中儲存碳的庫體或儲集區，例如大氣、海洋、土壤、植被與沉積物。",
    },
    "carbon sink": {
        "traditional_chinese": "碳匯",
        "definition_cht": "自其他碳庫接收碳，且在一定期間內淨吸收量大於淨釋放量的碳庫或系統。",
    },
    "carbon source": {
        "traditional_chinese": "碳源",
        "definition_cht": "向其他碳庫輸出碳，且在一定期間內淨釋放量大於淨吸收量的碳庫或系統。",
    },
    "carbon tetrachloride": {
        "traditional_chinese": "四氯化碳",
        "definition_cht": "化學式為 CCl4 的含氯有機化合物，曾廣泛用作工業溶劑，並是大氣氯收支的重要來源之一，對平流層臭氧具有破壞潛勢。",
    },
    "carbon-black seeding": {
        "traditional_chinese": "炭黑播種",
        "definition_cht": "一種雲播種方式，將微細炭黑或煙灰粒子散布於大氣中，以吸收輻射能並加熱周圍空氣，可能進一步促進對流發展。",
    },
}

for rel in ['data/c_terms_all_cht.json', 'data/glossary_all_cht.json']:
    path = Path('/home/node/.openclaw/workspace/met_term') / rel
    arr = json.loads(path.read_text())
    changed = 0
    for row in arr:
        key = row['english']
        if key in updates:
            row.update(updates[key])
            changed += 1
    path.write_text(json.dumps(arr, ensure_ascii=False, indent=2) + '\n')
    print(path.name, changed)
