import json
from pathlib import Path

updates = {
    'right ascension': {
        'traditional_chinese': '赤經',
        'definition_cht': '天文學中的赤道座標量，指沿天球赤道自春分點起向東量至天體時圈的角距；須與赤緯配合，才能在赤道座標系中標示天體位置，可視為天球上的「經度」對應量。'
    },
    'right-hand rotation': {
        'traditional_chinese': '右手旋轉',
        'definition_cht': '依右手定則所界定的旋轉方向：以右手拇指指向正軸方向時，其餘四指彎曲所示即為正向旋轉的方向；在向量、座標與流體旋轉描述中常用來統一旋轉正負號與方向判定。'
    },
    'right-handed rectangular coordinates': {
        'traditional_chinese': '右手直角座標系',
        'definition_cht': '符合右手定則的三維直角座標系；當右手食指、中指與拇指分別對應三個正軸時，其排列可一致表示 x、y、z 軸的正向關係，廣用於動力學、地球物理與儀器幾何描述。'
    },
    'rime': {
        'traditional_chinese': '霧淞',
        'definition_cht': '由過冷霧滴或雲滴撞擊低於冰點的物體表面後迅速凍結所形成的白色或乳白色鬆脆冰沉積，常附著於樹枝、電線、桅杆與地形迎風面；其結構通常含有氣孔，與透明且較緻密的雨淞不同。'
    },
    'rime fog': {
        'traditional_chinese': '霧淞霧',
        'definition_cht': '由過冷小霧滴所組成、且容易在暴露物體上形成霧淞的霧；多出現在氣溫低於冰點時，當霧滴附著於迎風表面便迅速凍結，造成白色冰晶或顆粒狀積冰。'
    },
    'rime ice': {
        'traditional_chinese': '霧淞冰',
        'definition_cht': '由過冷水滴快速凍結所形成的白色不透明顆粒狀積冰，內含較多氣泡、質地較鬆且表面粗糙，常見於低溫雲、凍霧或山區強風環境中的物體迎風面。'
    },
    'rime rod': {
        'traditional_chinese': '霧淞觀測棒',
        'definition_cht': '用於觀測或量測霧淞附著量的棒狀暴露體或標準收集器，通常置於開闊迎風處，以比較不同時間的霧淞積聚厚度、形態或增長速率。'
    },
    'Rinehart projection': {
        'traditional_chinese': 'Rinehart 投影',
        'definition_cht': '雷達氣象學中的一種資料投影或顯示概念，指將雷達量測的距離—仰角幾何關係轉換投影到剖面或平面座標上，以利判讀回波結構、高度分布與空間位置；實際呈現方式須依所用雷達分析方法而定。'
    },
    'Ringelmann chart': {
        'traditional_chinese': '林格曼煙度圖',
        'definition_cht': '以不同深淺灰階組成的標準比對圖，用於目視判定煙柱的不透明度或煙度等級，常應用於燃燒排放、空氣污染巡查與煙塵監測的現場估測。'
    },
    'rip': {
        'traditional_chinese': '激流帶',
        'definition_cht': '海岸或潮流環境中因流速差、回流水、地形束縮或不同水流交會而形成的狹窄而湍急水帶，水面常呈現較粗亂或破碎的紋理；在一般海灘語境中亦常作為 rip current 的簡稱。'
    },
    'rip current': {
        'traditional_chinese': '離岸流',
        'definition_cht': '近岸碎波區內向岸輸送的海水集中回流外海時，所形成的狹窄、強勁且局部性的離岸水流；其流向通常垂直或近似垂直海岸，是海灘溺水風險的重要來源之一。'
    },
    'ripe': {
        'traditional_chinese': '成熟的',
        'definition_cht': '在雪文或積雪水文中，通常指雪層已升溫至等溫近 0°C、並具足夠含液水量，因而能開始向下傳輸或釋出融雪水的狀態；亦即雪層已具備實質融雪出流條件。'
    },
    'ripening of snow': {
        'traditional_chinese': '雪層成熟',
        'definition_cht': '積雪由低於冰點逐步吸收熱量，升溫至接近 0°C 並增加含液水量的過程；當雪層完成此一成熟階段後，後續融雪水才較容易穿透雪層並形成明顯出流。'
    },
    'ripple': {
        'traditional_chinese': '波紋',
        'definition_cht': '水面、沙面或其他流體／沉積物邊界上所出現的小尺度規則起伏，可由微風、流速剪切、振動或流體與底床交互作用所形成；在水面語境中常指短波長、低振幅的細小波。'
    },
    'ripple wave': {
        'traditional_chinese': '波紋波',
        'definition_cht': '泛指表現為細小波紋的短波長表面波，通常振幅小、尺度短，可由微風、局部擾動或流速變化激發；在水面上常屬重力與表面張力共同影響的微尺度波動。'
    },
    'rise time': {
        'traditional_chinese': '上升時間',
        'definition_cht': '訊號、脈衝或量測輸出由較低指定值上升至較高指定值所需的時間，電子與雷達工程中常以 10% 到 90%（或 20% 到 80%）振幅區間來定義，用以描述系統響應速度。'
    },
    'rising limb': {
        'traditional_chinese': '上升段',
        'definition_cht': '水文歷線或河川流量歷線中，自流量開始增大至洪峰出現之前的上升部分；其形狀反映降雨、融雪、集流速度與流域滯蓄特性。'
    },
    'rising tide': {
        'traditional_chinese': '漲潮',
        'definition_cht': '潮位由低向高上升的階段，即自低潮後至高潮前的海面上升期；在潮流語境中通常對應於洪潮或向岸、向上游推進的潮汐影響。'
    },
    'river': {
        'traditional_chinese': '河川',
        'definition_cht': '沿天然河道由高處向低處持續或季節性流動的地表水體，最終多匯入湖泊、其他河川、內海或海洋；其形成與流量變化受降水、融雪、地下水補注、地形與地質條件共同控制。'
    },
    'river basin': {
        'traditional_chinese': '流域',
        'definition_cht': '由分水嶺所界定、所有地表逕流最終匯入同一河川系統出口的集水區域；其內可再細分為多個次流域，是水文分析、水資源管理與洪旱評估的基本空間單元。'
    },
}

paths = [Path('data/r_terms_all_cht.json'), Path('data/glossary_all_cht.json')]
for path in paths:
    data = json.loads(path.read_text())
    changed = 0
    for row in data:
        eng = row.get('english')
        if eng in updates:
            row.update(updates[eng])
            changed += 1
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    print(path, changed)
