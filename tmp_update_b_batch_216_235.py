import json
from pathlib import Path

updates = {
    "bird burst": {
        "traditional_chinese": "鳥群爆發回波",
        "definition_cht": "天氣雷達於日出前後常見的生物性回波現象，指棲息地中的鳥群集體起飛後，在雷達上形成由中心向外擴張的環狀或近環狀回波；其都卜勒速度場在低層可呈現類似微下衝的發散訊號。",
    },
    "birefringence": {
        "traditional_chinese": "雙折射",
        "definition_cht": "各向異性介質的一種光學性質，指光在材料中的折射率會隨傳播方向或偏振方向而改變，因而使入射光分裂為兩束偏振態不同、傳播速率不同的光線；亦稱雙重折射。",
    },
    "Birkeland currents": {
        "traditional_chinese": "伯克蘭電流",
        "definition_cht": "沿地球磁力線在磁層與高緯電離層之間流動的電流系統，屬場向電流，與極光活動及極區電流系統密切相關。",
    },
    "bise": {
        "traditional_chinese": "比斯風",
        "definition_cht": "瑞士一帶的地方風，通常指橫越瑞士高原、由東北向西南吹送的冷而乾的東北風；在特定壓場配置下可增強並伴隨低溫、雲量增加或降水。",
    },
    "Bishop wave": {
        "traditional_chinese": "畢曉普波",
        "definition_cht": "美國加州畢曉普附近、內華達山脈背風側形成的著名大氣背風波個案，常伴隨透鏡雲、轉子雲及強烈上升與亂流現象。",
    },
    "Bishop's ring": {
        "traditional_chinese": "畢曉普環",
        "definition_cht": "日輪或月輪附近可見的淡而寬廣之褐紅色光環或暈圈，多與高空極細火山灰或硫酸鹽氣膠對光的散射或繞射有關，1883 年喀拉喀托火山爆發後曾廣泛觀測到。",
    },
    "bistatic": {
        "traditional_chinese": "雙基地的",
        "definition_cht": "描述發射端與接收端分設於不同地點之遙測或雷達觀測配置的形容詞；相對於單基地系統，其幾何關係需同時考慮發射器、目標與接收器的位置。",
    },
    "bistatic radar": {
        "traditional_chinese": "雙基地雷達",
        "definition_cht": "發射機與接收機設於不同位置的雷達系統；電磁波由發射端射向目標後，再由另一地點的接收端量測散射訊號。",
    },
    "bit": {
        "traditional_chinese": "位元",
        "definition_cht": "數位資訊與資料傳輸的基本單位，為 binary digit 的縮寫，只能表示兩種狀態，通常記為 0 與 1。",
    },
    "bit rate": {
        "traditional_chinese": "位元率",
        "definition_cht": "單位時間內傳輸或處理的位元數，通常以 bits per second（bps）表示；其概念不同於鮑率，後者描述每秒符號變化次數。",
    },
    "bittern": {
        "traditional_chinese": "苦鹵",
        "definition_cht": "海水或鹽鹵在氯化鈉析出後所剩的高鹽度苦味母液，富含鎂鹽、鈣鹽、鉀鹽及其他離子，常見於鹽田蒸發與鹵水濃縮過程。",
    },
    "bivane": {
        "traditional_chinese": "雙翼風向儀",
        "definition_cht": "用於量測三維風向擾動的儀器，通常由兩片互相垂直的輕質翼面裝於可在水平與垂直平面轉動的平衡桿上，以偵測水平風向與仰俯角變化；部分型式可兼測風速。",
    },
    "BL": {
        "traditional_chinese": "邊界層（縮寫）",
        "definition_cht": "boundary layer 的縮寫；在氣象學中通常指大氣邊界層，即直接受地表摩擦、熱力與水氣通量影響、並能在約一小時或更短時間內回應地表強迫的近地層大氣。",
    },
    "black blizzard": {
        "traditional_chinese": "黑色塵暴",
        "definition_cht": "含塵極濃、範圍廣且常伴隨強風的嚴重沙塵暴或塵暴；因空中塵土密布使天空昏黑如暴風雪而得名，亦可作為 duststorm 的別稱。",
    },
    "black fog": {
        "traditional_chinese": "黑霧",
        "definition_cht": "受煤煙、煤焦油微粒與二氧化硫等污染物嚴重混入的濃霧或煙霧，常呈黑灰、黃綠或污濁外觀；為早期工業城市典型的污染霧現象，亦近似所稱的 pea-soup fog。",
    },
    "black frost": {
        "traditional_chinese": "黑霜",
        "definition_cht": "就植物受害而言的一種乾凍現象，指植物組織在未形成具保護作用的白霜或霜華時即發生內部凍結，常造成植株發黑枯死，因此亦屬致死霜凍。",
    },
    "black ice": {
        "traditional_chinese": "黑冰",
        "definition_cht": "路面、橋面或其他表面上形成的薄而透明、視覺上不易察覺的冰層，常由細雨、毛毛雨、融雪水或過冷霧滴在表面溫度低於 0°C 時凍結而成，對交通極具危險性。",
    },
    "black northeaster": {
        "traditional_chinese": "黑色東北烈風",
        "definition_cht": "澳洲與紐西蘭一帶對強勁東北風或東北烈風的名稱，通常伴隨陰暗天色、厚雲、風浪或惡劣天氣；可視為地方性 northeaster 的一種。",
    },
    "black squall": {
        "traditional_chinese": "黑颮",
        "definition_cht": "伴隨深色雲系、且通常帶有強陣風與大雨的颮；航海與天氣描述中常用以指來勢迅猛、天色驟暗的局地強風天氣。",
    },
    "black storm": {
        "traditional_chinese": "黑色風暴",
        "definition_cht": "泛指伴隨濃密暗黑雲層的風暴，尤常指雷暴；重點在於其陰沉厚重的雲貌與惡劣天氣徵象。",
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
            row.update(updates[key])
            changed += 1
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(rel, changed)
