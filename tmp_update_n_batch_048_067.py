import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

UA = 'Mozilla/5.0'

terms = [
    {
        'english': 'negative isothermal vorticity advection',
        'traditional_chinese': '負等溫渦度平流',
        'definition_cht': '在等溫分析或等熵／等溫層面診斷中，某地因平流作用而接收到較低的渦度值；常用於描述高空流場中渦度減少的平流效應，與下沉或天氣系統減弱等診斷判釋有關。',
        'checks': [
            'https://glossary.ametsoc.org/wiki/vorticity_advection',
            'https://en.wikipedia.org/wiki/Vorticity'
        ]
    },
    {
        'english': 'negative rain',
        'traditional_chinese': '負雨量',
        'definition_cht': '指因蒸發、截留回蒸或觀測／水量平衡記號慣例而以負值表示的有效降水量；在實際降水現象中並非「向上降雨」，而是表示水分收支呈淨減少。',
        'checks': [
            'https://en.wikipedia.org/wiki/Precipitation',
            'https://en.wikipedia.org/wiki/Water_balance'
        ]
    },
    {
        'english': 'negative viscosity',
        'traditional_chinese': '負黏度',
        'definition_cht': '在流體或地球物理流體力學中，指渦旋或擾動作用非但不耗散大尺度流動動能，反而把小尺度能量回饋到大尺度流場的有效黏滯行為；常見於二維亂流、噴流維持與某些大氣海洋參數化討論。',
        'checks': [
            'https://en.wikipedia.org/wiki/Eddy_viscosity',
            'https://en.wikipedia.org/wiki/Inverse_energy_cascade'
        ]
    },
    {
        'english': 'nemere',
        'traditional_chinese': '內梅雷風',
        'definition_cht': '羅馬尼亞與喀爾巴阡山弧區的地方風名，通常指自東北或東方吹出的寒冷強陣風，常在冬季造成降溫與風害。',
        'checks': [
            'https://en.wikipedia.org/wiki/Local_winds',
            'https://ro.wikipedia.org/wiki/Nemira'
        ]
    },
    {
        'english': 'Neoglacial',
        'traditional_chinese': '新冰期',
        'definition_cht': '全新世中晚期冰川在許多山區與高緯地區重新擴張、氣候較前期轉冷的時段或事件總稱，常用於古氣候與第四紀研究。',
        'checks': [
            'https://en.wikipedia.org/wiki/Neoglaciation',
            'https://www.britannica.com/science/Holocene-Epoch'
        ]
    },
    {
        'english': 'neon',
        'traditional_chinese': '氖',
        'definition_cht': '化學元素，原子序 10，屬稀有氣體；在大氣中含量極低、化性穩定，常作為大氣組成或氣體分析中的微量惰性成分。',
        'checks': [
            'https://en.wikipedia.org/wiki/Neon',
            'https://pubchem.ncbi.nlm.nih.gov/element/Neon'
        ]
    },
    {
        'english': 'neper',
        'traditional_chinese': '奈培',
        'definition_cht': '以自然對數表示振幅比或場量比的對數單位，常用於聲學、電信與波動衰減分析；1 奈培對應振幅比 e:1。',
        'checks': [
            'https://en.wikipedia.org/wiki/Neper',
            'https://www.britannica.com/science/neper'
        ]
    },
    {
        'english': 'nephanalysis',
        'traditional_chinese': '雲圖分析',
        'definition_cht': '依地面、航空、衛星或其他觀測資料，分析某一時刻雲量、雲型與雲區分布的作業或成果圖，用於綜觀天氣判釋與預報。',
        'checks': [
            'https://glossary.ametsoc.org/wiki/nephanalysis',
            'https://en.wiktionary.org/wiki/nephanalysis'
        ]
    },
    {
        'english': 'nephcurve',
        'traditional_chinese': '濁度曲線',
        'definition_cht': '以比濁或散射量測結果繪成、用以表示懸浮粒子濃度與光散射響應關係的曲線；亦可指相關校正曲線。',
        'checks': [
            'https://en.wiktionary.org/wiki/nephelometer',
            'https://en.wikipedia.org/wiki/Turbidity'
        ]
    },
    {
        'english': 'nephelometer',
        'traditional_chinese': '散射濁度計',
        'definition_cht': '利用粒子對入射光之散射強度來測量懸浮微粒、霧滴或液體濁度的儀器；在大氣科學中常用於氣膠、能見度與散射係數觀測。',
        'checks': [
            'https://en.wikipedia.org/wiki/Nephelometer',
            'https://amt.copernicus.org/articles/14/2989/2021/'
        ]
    },
    {
        'english': 'nephelometry',
        'traditional_chinese': '散射比濁法',
        'definition_cht': '依樣品對光的散射強度來估算懸浮粒子或膠體濃度的量測方法，是 nephelometer 的基本測量原理。',
        'checks': [
            'https://en.wikipedia.org/wiki/Nephelometer',
            'https://en.wikipedia.org/wiki/Turbidity'
        ]
    },
    {
        'english': 'nepheloscope',
        'traditional_chinese': '觀雲鏡',
        'definition_cht': '用於觀測雲移方向與相對速度的儀器，通常藉鏡面、格線或基準標記追蹤雲體運動。',
        'checks': [
            'https://en.wiktionary.org/wiki/nephoscope',
            'https://www.merriam-webster.com/dictionary/nephoscope'
        ]
    },
    {
        'english': 'nephology',
        'traditional_chinese': '雲學',
        'definition_cht': '研究雲的形成、形態、分類、演變與分布之學科，屬氣象學的重要分支。',
        'checks': [
            'https://en.wiktionary.org/wiki/nephology',
            'https://www.britannica.com/science/cloud-meteorology'
        ]
    },
    {
        'english': 'nephometer',
        'traditional_chinese': '測雲儀',
        'definition_cht': '早期用於測定雲高、雲移方向或相關雲量幾何資訊的儀器名稱；不同文獻中所指型式可略有差異。',
        'checks': [
            'https://en.wiktionary.org/wiki/nephometer',
            'https://archive.org/details/meteorologicalin00unse/page/204/mode/2up'
        ]
    },
    {
        'english': 'nephoscope',
        'traditional_chinese': '測雲鏡',
        'definition_cht': '觀測雲體移動方向與估計雲速的儀器，常藉鏡面反射天空並配合方位刻度判讀雲行。',
        'checks': [
            'https://en.wikipedia.org/wiki/Nephoscope',
            'https://www.merriam-webster.com/dictionary/nephoscope'
        ]
    },
    {
        'english': 'nested grids',
        'traditional_chinese': '巢狀格網',
        'definition_cht': '數值模式中在較粗解析度母網格內嵌入一個或多個較細解析度子網格的配置，用以在重點區域提高模擬精細度，同時兼顧計算效率。',
        'checks': [
            'https://en.wikipedia.org/wiki/Nested_grid_model',
            'https://www2.mmm.ucar.edu/wrf/users/wrf_users_guide/build/html/namelist_variables.html'
        ]
    },
    {
        'english': 'net balance',
        'traditional_chinese': '淨平衡量',
        'definition_cht': '某一期間內收入與支出、累積與消耗或增量與減量相互抵銷後得到的淨結果；在冰川學常指累積與消融之差，在能量或水量分析中亦可類推使用。',
        'checks': [
            'https://en.wikipedia.org/wiki/Glacier_mass_balance',
            'https://nsidc.org/learn/parts-cryosphere/glaciers/glacier-mass-balance'
        ]
    },
    {
        'english': 'net primary production',
        'traditional_chinese': '淨初級生產量',
        'definition_cht': '自營生物經光合作用固定的總有機碳中，扣除自身呼吸消耗後所剩可供生物量累積與食物網利用的部分。',
        'checks': [
            'https://en.wikipedia.org/wiki/Net_primary_productivity',
            'https://earthobservatory.nasa.gov/features/MeasuringVegetation/measuring_vegetation_2.php'
        ]
    },
    {
        'english': 'net pyranometer',
        'traditional_chinese': '淨短波輻射計',
        'definition_cht': '以成對感測器分別量測向下與向上太陽短波輻射，並取其差值以求得淨短波輻射的儀器。',
        'checks': [
            'https://www.baranidesign.com/faq-articles/2020/1/19/net-radiometers-definition-working-principle-and-faqs',
            'https://www.kippzonen.com/Product/14/CNR4-Net-Radiometer#.Y6Rca3bMK3A'
        ]
    },
    {
        'english': 'net pyrgeometer',
        'traditional_chinese': '淨長波輻射計',
        'definition_cht': '以成對感測器量測向下與向上地氣系統長波紅外輻射，並取其差值以求得淨長波輻射的儀器。',
        'checks': [
            'https://www.baranidesign.com/faq-articles/2020/1/19/net-radiometers-definition-working-principle-and-faqs',
            'https://www.kippzonen.com/Product/14/CNR4-Net-Radiometer#.Y6Rca3bMK3A'
        ]
    }
]

def fetch(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': UA})
        with urllib.request.urlopen(req, timeout=25) as r:
            raw = r.read(5000).decode('utf-8', 'ignore')
        txt = re.sub(r'<[^>]+>', ' ', raw)
        txt = re.sub(r'\s+', ' ', txt).strip()
        return {'url': url, 'ok': True, 'snippet': txt[:320]}
    except Exception as e:
        return {'url': url, 'ok': False, 'error': str(e)}

report = []
for term in terms:
    checks = [fetch(u) for u in term['checks']]
    report.append({'english': term['english'], 'checks': checks})

Path('tmp_n_048_067_checks.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

for file in [Path('data/n_terms_all_cht.json'), Path('data/glossary_all_cht.json')]:
    arr = json.loads(file.read_text(encoding='utf-8'))
    by_eng = {item['english']: item for item in arr}
    for term in terms:
        item = by_eng.get(term['english'])
        if item:
            item['traditional_chinese'] = term['traditional_chinese']
            item['definition_cht'] = term['definition_cht']
            item['source_url'] = term['checks'][0]
    file.write_text(json.dumps(arr, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

print('updated files and wrote tmp_n_048_067_checks.json')
