import json
from pathlib import Path

updates = {
    'sling thermometer': {
        'traditional_chinese': '吊索溫度計',
        'definition_cht': '裝設於框架或吊柄上、可由人工旋轉以形成通風的溫度計；常用於野外量測氣溫，亦可作為吊索乾濕計的組成元件。',
        'source_url': 'https://glossary.ametsoc.org/wiki/sling-thermometer/'
    },
    'slope area method': {
        'traditional_chinese': '坡降面積法',
        'definition_cht': '水文學中在洪水過後，依高水位痕跡推估水面坡降，並配合兩個以上河道斷面測量及糙率估計，再以 Manning 或 Chezy 公式間接反算洪峰流量的方法。',
        'source_url': 'https://glossary.ametsoc.org/wiki/slope-area-method/'
    },
    'slope flow': {
        'traditional_chinese': '坡面氣流',
        'definition_cht': '由坡面受熱或冷卻所驅動、沿坡向上或向下流動的局地氣流；白天地表增暖常形成上坡風，夜間冷卻則常形成下坡風。',
        'source_url': 'https://glossary.ametsoc.org/wiki/slope-flow/'
    },
    'slope of a front': {
        'traditional_chinese': '鋒面坡度',
        'definition_cht': '鋒面相對水平面的傾斜程度，數值上通常指鋒面與水平面夾角的正切。',
        'source_url': 'https://glossary.ametsoc.org/wiki/slope-of-a-front/'
    },
    'slope of an isobaric surface': {
        'traditional_chinese': '等壓面坡度',
        'definition_cht': '等壓面相對水平面的傾斜程度，通常定義為其與水平面夾角的正切，可用以描述等壓面起伏。',
        'source_url': 'https://glossary.ametsoc.org/wiki/slope-of-an-isobaric-surface/'
    },
    'Slope Water': {
        'traditional_chinese': '陸坡水',
        'definition_cht': '物理海洋學中指大陸棚外緣至灣流之間、沿大陸坡分布的水團，常見於北大西洋西部，性質介於近岸棚水與外海水之間，並受兩者混合作用影響。',
        'source_url': 'https://glossary.ametsoc.org/wiki/Slope_Water'
    },
    'slope winds': {
        'traditional_chinese': '坡風',
        'definition_cht': '受浮力作用驅動、沿傾斜地形上升或下滑的局地風系，包含白天的上坡風與夜間的下坡風，為山谷風環流的重要組成。',
        'source_url': 'https://glossary.ametsoc.org/wiki/slope-winds/'
    },
    'slope windstorm': {
        'traditional_chinese': '下坡風暴',
        'definition_cht': '又稱坡降風暴，指強烈綜觀氣流越過山脊後，在脊頂上方強逆溫層限制下，於背風坡近地面形成的劇烈陣風型下坡風，常具有破壞性。',
        'source_url': 'https://glossary.ametsoc.org/wiki/slope-windstorm/'
    },
    'slow manifold': {
        'traditional_chinese': '慢流形',
        'definition_cht': '動力氣象與數值模式中，指隨時間只緩慢演變的一組大氣狀態或解空間；快速重力波等高頻模態被排除後，系統主要在此子空間內演化。',
        'source_url': 'https://glossary.ametsoc.org/wiki/slow-manifold/'
    },
    'slow tail': {
        'traditional_chinese': '慢尾',
        'definition_cht': '某些天電訊號中落後於初始甚低頻脈衝到達的極低頻尾部成分，主要因低頻相速度較慢所致，並常與閃電持續電流等機制有關。',
        'source_url': 'https://glossary.ametsoc.org/wiki/slow-tail/'
    },
    'sludge': {
        'traditional_chinese': '冰泥',
        'definition_cht': '海冰初生階段中，大量片冰或針冰在水面聚集形成的濃稠糊狀冰水混合層，外觀常呈濃湯狀或油脂狀，厚度通常不深。',
        'source_url': 'https://glossary.ametsoc.org/wiki/sludge/'
    },
    'sluff': {
        'traditional_chinese': '鬆雪滑落',
        'definition_cht': '坡面上少量積雪沿坡向下的小規模滑移或鬆散雪崩，通常規模不大但可作為雪層不穩定的徵兆。',
        'source_url': 'https://glossary.ametsoc.org/wiki/sluff/'
    },
    'slug test': {
        'traditional_chinese': '瞬時水位試驗',
        'definition_cht': '地下水水文中，藉由迅速抬升或降低井內水位，並量測其回復至原平衡水位所需時間，以估算井附近含水層水力傳導係數的試驗方法。',
        'source_url': 'https://glossary.ametsoc.org/wiki/slug-test/'
    },
    'slush': {
        'traditional_chinese': '雪泥',
        'definition_cht': '地面積雪或冰在雨水、暖溫或化學融冰作用下部分融化後形成的鬆軟含水混合物；亦可泛指泥濘濕滑的融雪狀態。',
        'source_url': 'https://glossary.ametsoc.org/wiki/slush/'
    },
    'slush icing': {
        'traditional_chinese': '雪泥積冰',
        'definition_cht': '航空氣象中，飛機在接近 0°C 的濕雪與過冷液滴環境飛行時，於外露表面同時累積冰與水所形成的積冰現象。',
        'source_url': 'https://glossary.ametsoc.org/wiki/slush-icing/'
    },
    'small calorie': {
        'traditional_chinese': '小卡路里',
        'definition_cht': '又稱克卡，為使 1 克水升高 1 攝氏度所需的能量，約等於 4.1855 焦耳，用以區別於營養學常用的大卡（千卡）。',
        'source_url': 'https://glossary.ametsoc.org/wiki/small-calorie/'
    },
    'small circle': {
        'traditional_chinese': '小圓',
        'definition_cht': '球面與不通過球心之平面相交所形成的圓；相對地，通過球心者稱為大圓。',
        'source_url': 'https://glossary.ametsoc.org/wiki/small-circle/'
    },
    'small eddy closure': {
        'traditional_chinese': '小渦閉合',
        'definition_cht': '一階湍流閉合法，將未解析的小尺度渦動通量參數化為沿平均量局地梯度方向的擴散或黏滯效應，亦即梯度傳輸理論或 K 理論。',
        'source_url': 'https://glossary.ametsoc.org/wiki/small-eddy-closure/'
    },
    'small eddy theory': {
        'traditional_chinese': '小渦理論',
        'definition_cht': '將小尺度湍渦視為類似分子傳輸的混合作用，並以渦黏滯或渦擴散概念描述其對平均場傳輸影響的理論；本質上屬梯度傳輸型參數化。',
        'source_url': 'https://glossary.ametsoc.org/wiki/small-eddy-theory/'
    },
    'Small hail': {
        'traditional_chinese': '小雹（多指霰／軟雹）',
        'definition_cht': '舊稱中常指粒徑較小、呈白色不透明且易碎的冰粒降水，現代分類多歸入霰或軟雹，而非典型由強烈對流形成的大型雹石。',
        'source_url': 'https://en.wikipedia.org/wiki/Graupel'
    },
}

for path_str in ['data/s_terms_all_cht.json', 'data/glossary_all_cht.json']:
    path = Path(path_str)
    data = json.loads(path.read_text())
    arr = data['terms'] if isinstance(data, dict) else data
    changed = 0
    for row in arr:
        u = updates.get(row.get('english'))
        if u:
            row.update(u)
            changed += 1
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    print(path_str, changed)

Path('tmp_s_411_430_review_notes.json').write_text(json.dumps({
    'range': 's terms 411-430',
    'checks': [
        'AMS glossary pages via r.jina.ai mirror for the 20 sequential terms',
        'Secondary checks from Wikipedia API / Bing RSS / glossary cross-references depending on term'
    ],
    'updated_terms': list(updates.keys())
}, ensure_ascii=False, indent=2) + '\n')
print('notes written')
