import json
from pathlib import Path

updates = {
    'vortex thermometer': {
        'traditional_chinese': '渦流溫度計',
        'definition_cht': '利用氣流在旋轉或渦流狀態下的熱力特性來量測溫度的儀器；在航空與流體實驗中可用於推估高速氣流或自由大氣中的真實氣溫。'
    },
    'vortex tube': {
        'traditional_chinese': '渦管',
        'definition_cht': '流體力學中由一束渦線圍成的管狀區域，其管壁處處與渦度向量平行；常用來描述渦量在流場中的守恆與傳輸。'
    },
    'Vorticity': {
        'traditional_chinese': '渦度',
        'definition_cht': '描述流體局部旋轉強度與方向的量，在三維流場中定義為速度場的旋度；在氣象分析上常用以診斷槽脊、氣旋發展與動力強迫。'
    },
    'vorticity advection': {
        'traditional_chinese': '渦度平流',
        'definition_cht': '指風場將某地的渦度輸送至另一地的過程；在天氣尺度分析中，正渦度平流常與上升運動及槽前發展有關。'
    },
    'vorticity equation': {
        'traditional_chinese': '渦度方程',
        'definition_cht': '描述流體中渦度隨時間因平流、伸長、傾斜、摩擦與浮力等作用而改變的控制方程，是大氣與海洋動力學的重要基礎方程。'
    },
    'vorticity-transport hypothesis': {
        'traditional_chinese': '渦度傳輸假說',
        'definition_cht': '指以渦度的生成、輸送與重新分布來解釋流場演變的假說或觀點，常用於討論渦旋結構的形成、維持與下游影響。'
    },
    'Voss polariscope': {
        'traditional_chinese': '沃斯偏光鏡',
        'definition_cht': '一種用於觀察或比較偏振光特性的偏光儀器，利用偏振器與檢偏器分析光線的偏振狀態；可應用於大氣光學或輻射觀測。'
    },
    'vuthan': {
        'traditional_chinese': '武坦風暴',
        'definition_cht': '南美洲南部的一種強烈風暴名稱，屬區域性天氣用語，可指伴隨強風與惡劣天氣的劇烈擾動。'
    },
    'VWP': {
        'traditional_chinese': '垂直風剖面',
        'definition_cht': 'vertical wind profile 的縮寫，通常指由都卜勒天氣雷達或其他遙測資料反演的風向與風速垂直分布產品，用於監測風切、低空噴流與對流環境。'
    },
    'wadi': {
        'traditional_chinese': '乾谷河道',
        'definition_cht': '乾旱或半乾旱地區平時多半乾涸、僅在降雨後短暫出現地表逕流的河道或谷地，常與暴洪、沖蝕及間歇性輸砂作用有關。'
    },
    'wake': {
        'traditional_chinese': '尾流',
        'definition_cht': '物體、地形或天氣系統擾動主流後，在其下游形成的流場擾動區；常伴隨速度虧損、渦旋生成、壓力變化與湍流增強。'
    },
    'wake low': {
        'traditional_chinese': '尾流低壓',
        'definition_cht': '常出現在中尺度對流系統後側尾流區的局地低壓，通常與層中下沉氣流造成的絕熱增溫及壓力重新調整有關。'
    },
    'wake turbulence': {
        'traditional_chinese': '尾流湍流',
        'definition_cht': '物體通過流體後在其後方留下的湍流擾動；在航空上尤指飛機升力產生的翼尖渦流所造成的危險擾動。'
    },
    'waldsterben': {
        'traditional_chinese': '森林衰亡',
        'definition_cht': '源自德語的用語，指森林因空氣污染、酸沉降、乾旱、病蟲害或其他環境壓力而出現大範圍衰退、樹冠受損與死亡的現象。'
    },
    'Walker circulation': {
        'traditional_chinese': '沃克環流',
        'definition_cht': '熱帶大氣沿赤道方向形成的東西向閉合環流，典型表現為西太平洋暖池區上升、東太平洋下沉，並與信風、海溫分布及聖嬰－南方振盪密切相關。'
    },
    'wall cloud': {
        'traditional_chinese': '牆雲',
        'definition_cht': '積雨雲無雨雲底下方局部且持續的明顯下垂雲體，通常位於強上升氣流區；若伴隨旋轉，常與中氣旋及龍捲生成潛勢有關。'
    },
    'warm braw': {
        'traditional_chinese': '暖脊',
        'definition_cht': '指溫度場中暖空氣向外延伸形成的脊狀區域；此詞在現代文獻中少見，通常可視為 warm ridge 的異寫或罕用寫法。'
    },
    'warm cloud': {
        'traditional_chinese': '暖雲',
        'definition_cht': '整個雲體溫度皆高於 0°C、主要由液態雲滴組成而不含冰晶相的雲；其降水形成多依賴凝結、碰併與聚合作用。'
    },
    'warm conveyor belt': {
        'traditional_chinese': '暖輸送帶',
        'definition_cht': '中緯度氣旋中由暖區近地層向上傾升並朝極側與下游輸送暖濕空氣的狹長氣流帶，是鋒面雲雨帶與大尺度降水的重要結構。'
    },
    'warm fog': {
        'traditional_chinese': '暖霧',
        'definition_cht': '由液態霧滴組成且氣溫高於冰點的霧，通常用來與冰霧相對；其形成機制可包括輻射冷卻、平流或蒸發增濕。'
    },
}

notes = {
    'vortex thermometer': {
        'checks': [
            'https://glossary.ametsoc.org/wiki/vortex_thermometer',
            'https://pubs.aip.org/aip/rsi/article/21/2/136/297336/Vortex-Thermometer-for-Measuring-True-Air'
        ],
        'changed': True,
    },
    'vortex tube': {
        'checks': [
            'https://glossary.ametsoc.org/wiki/vortex_tube',
            'https://en.wikipedia.org/wiki/Vortex_tube'
        ],
        'changed': True,
    },
    'Vorticity': {
        'checks': [
            'https://glossary.ametsoc.org/wiki/Vorticity',
            'https://en.wikipedia.org/wiki/Vorticity'
        ],
        'changed': True,
    },
    'vorticity advection': {
        'checks': [
            'https://glossary.ametsoc.org/wiki/vorticity_advection',
            'https://www.weather.gov/source/zhu/ZHU_Training_Page/Miscellaneous/vorticity/vorticity.html'
        ],
        'changed': True,
    },
    'vorticity equation': {
        'checks': [
            'https://glossary.ametsoc.org/wiki/vorticity_equation',
            'https://en.wikipedia.org/wiki/Vorticity_equation'
        ],
        'changed': True,
    },
    'vorticity-transport hypothesis': {
        'checks': [
            'https://glossary.ametsoc.org/wiki/vorticity-transport_hypothesis',
            'https://archive.org/details/glossaryofmeteor00hush'
        ],
        'changed': True,
    },
    'Voss polariscope': {
        'checks': [
            'https://glossary.ametsoc.org/wiki/Voss_polariscope',
            'https://encyclopedia2.thefreedictionary.com/polariscope'
        ],
        'changed': True,
    },
    'vuthan': {
        'checks': [
            'https://glossary.ametsoc.org/wiki/vuthan',
            'https://encyclopedia2.thefreedictionary.com/vuthan'
        ],
        'changed': True,
    },
    'VWP': {
        'checks': [
            'https://glossary.ametsoc.org/wiki/VWP',
            'https://www.roc.noaa.gov/level-two-data-types.php'
        ],
        'changed': True,
    },
    'wadi': {
        'checks': [
            'https://glossary.ametsoc.org/wiki/wadi',
            'https://en.wikipedia.org/wiki/Wadi'
        ],
        'changed': True,
    },
    'wake': {
        'checks': [
            'https://glossary.ametsoc.org/wiki/wake',
            'https://en.wikipedia.org/wiki/Wake'
        ],
        'changed': True,
    },
    'wake low': {
        'checks': [
            'https://glossary.ametsoc.org/wiki/wake_low',
            'https://en.wikipedia.org/wiki/Wake_low'
        ],
        'changed': True,
    },
    'wake turbulence': {
        'checks': [
            'https://glossary.ametsoc.org/wiki/wake_turbulence',
            'https://en.wikipedia.org/wiki/Wake_turbulence'
        ],
        'changed': True,
    },
    'waldsterben': {
        'checks': [
            'https://glossary.ametsoc.org/wiki/waldsterben',
            'https://en.wikipedia.org/wiki/Waldsterben'
        ],
        'changed': True,
    },
    'Walker circulation': {
        'checks': [
            'https://glossary.ametsoc.org/wiki/Walker_circulation',
            'https://en.wikipedia.org/wiki/Walker_circulation'
        ],
        'changed': True,
    },
    'wall cloud': {
        'checks': [
            'https://glossary.ametsoc.org/wiki/wall_cloud',
            'https://en.wikipedia.org/wiki/Wall_cloud'
        ],
        'changed': True,
    },
    'warm braw': {
        'checks': [
            'https://glossary.ametsoc.org/wiki/warm_braw',
            'https://glossary.ametsoc.org/wiki/warm_ridge'
        ],
        'changed': True,
    },
    'warm cloud': {
        'checks': [
            'https://glossary.ametsoc.org/wiki/warm_cloud',
            'https://glossary.ametsoc.org/wiki/Warm_rain_process'
        ],
        'changed': True,
    },
    'warm conveyor belt': {
        'checks': [
            'https://glossary.ametsoc.org/wiki/warm_conveyor_belt',
            'https://rammb.cira.colostate.edu/wmovl/vrl/tutorials/satmanu-eumetsat/satmanu/basic/parameters/wcb.htm'
        ],
        'changed': True,
    },
    'warm fog': {
        'checks': [
            'https://glossary.ametsoc.org/wiki/warm_fog',
            'https://en.wikipedia.org/wiki/Fog'
        ],
        'changed': True,
    },
}

for path in [Path('data/v_terms_all_cht.json'), Path('data/w_terms_all_cht.json'), Path('data/glossary_all_cht.json')]:
    data = json.loads(path.read_text(encoding='utf-8'))
    changed = 0
    for row in data:
        eng = row.get('english')
        if eng in updates:
            row.update(updates[eng])
            changed += 1
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(path, changed)

Path('tmp_vw_180_199_review_notes.json').write_text(json.dumps(notes, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('notes written', len(notes))
