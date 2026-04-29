import json, re, time
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.parse import quote

BASE = Path('/home/node/.openclaw/workspace/met_term')
SRC = BASE / 'source_doc_rs.json'
DATA = BASE / 'data'
CACHE = DATA / '_rs_translate_cache.json'
OUTS = {
    'r': DATA / 'r_terms_all_cht.json',
    's': DATA / 's_terms_all_cht.json',
}

obj = json.loads(SRC.read_text(encoding='utf-8'))
terms = []
for block in obj.get('body', {}).get('content', []):
    para = block.get('paragraph')
    if not para:
        continue
    parts = []
    for el in para.get('elements', []):
        tr = el.get('textRun', {})
        if 'content' in tr:
            parts.append(tr['content'])
    text = ''.join(parts).replace('\v', ' ').replace('\n', ' ').strip()
    if text:
        terms.append(text)

cache = json.loads(CACHE.read_text(encoding='utf-8')) if CACHE.exists() else {}

def gtranslate(text: str) -> str:
    if text in cache:
        return cache[text]
    url = 'https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=zh-TW&dt=t&q=' + quote(text)
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    last_err = None
    for i in range(6):
        try:
            with urlopen(req, timeout=20) as r:
                data = json.loads(r.read().decode('utf-8'))
            out = ''.join(part[0] for part in data[0]).strip()
            cache[text] = out
            if len(cache) % 25 == 0:
                CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding='utf-8')
            time.sleep(0.08)
            return out
        except Exception as e:
            last_err = e
            time.sleep(1 + i)
    raise last_err

trans_override = {
    'R-scale': 'R 尺度',
    'R-scope': 'R 顯示器',
    'RVR': '跑道視程',
    'S-curve': 'S 曲線',
    'S-curve method': 'S 曲線法',
    'S-scale': 'S 尺度',
    'S-values': 'S 值',
    'S wave': 'S 波',
    'SSB': '單旁波帶',
    'SST': '海表溫度',
    'ST': '同溫層',
    'STJ': '副熱帶噴流',
    'SVP': '飽和水氣壓',
    'SW Monsoon': '西南季風',
    'SWMR': '標準化加權均方根',
    'systematic observations': '系統性觀測',
    'systematic error': '系統誤差',
    'surface air temperature': '地表氣溫',
    'surface analysis': '地面天氣分析',
    'surface chart': '地面天氣圖',
    'surface inversion': '地面逆溫',
    'surface low': '地面低壓',
    'surface pressure': '地面氣壓',
    'surface wave': '表面波',
    'storm surge': '風暴潮',
    'storm track': '風暴路徑',
    'streamline': '流線',
    'stream function': '流函數',
    'specific humidity': '比濕',
    'solar constant': '太陽常數',
    'solar radiation': '太陽輻射',
    'solstice': '至點',
    'snow line': '雪線',
    'snowmelt': '融雪',
    'snowpack': '積雪層',
    'scattering coefficient': '散射係數',
    'shortwave radiation': '短波輻射',
    'semiannual oscillation': '半年振盪',
    'sea breeze': '海風',
    'sea ice': '海冰',
    'sea level': '海平面',
    'sea-level pressure': '海平面氣壓',
    'seiche': '靜振',
    'sensible heat': '顯熱',
    'sleet': '霰',
    'smog': '煙霧',
    'snow': '雪',
    'snowflake': '雪花',
    'snowfall': '降雪',
    'sonde': '探空儀',
    'sounding': '探空',
    'squall': '颮',
    'stratosphere': '平流層',
    'stratocumulus': '層積雲',
    'stratus': '層雲',
    'subsidence': '下沉',
    'subtropical high': '副熱帶高壓',
    'supercell': '超級胞',
    'supersaturation': '過飽和',
    'synoptic chart': '綜觀天氣圖',
    'synoptic meteorology': '綜觀氣象學',
}


def manual_zh(term: str) -> str:
    if term in trans_override:
        return trans_override[term]
    return gtranslate(term)


def classify_definition(term: str, zh: str) -> str:
    low = term.lower()

    exact = {
        'RVR': '航空氣象中用以表示飛行員在跑道中心線上可見跑道標誌或燈光距離的能見度指標，常作為起降作業與低能見度程序的重要依據。',
        'SST': '海洋表層水體的溫度，是海氣交互作用、颱風發展、氣候監測與海洋遙測分析的重要基本量。',
        'SSB': '無線電通訊中僅保留單一旁波帶並抑制載波的調變方式，可降低頻寬需求並提升訊號傳輸效率。',
        'STJ': '位於副熱帶上對流層至下平流層附近的強風帶，與大尺度環流、鋒面活動及天氣系統移動密切相關。',
        'SVP': '在特定溫度下，水汽與液態水或冰面達熱力平衡時所對應的水氣壓，是濕度計算與相變分析的重要基準量。',
        'solstice': '太陽視赤緯達全年最北或最南位置的時刻，分別對應夏至與冬至，反映季節循環中的關鍵天文節點。',
        'streamline': '在某一瞬間處處與流速向量相切的曲線，用以表示流場方向結構，常用於大氣與海洋流動分析。',
        'stream function': '描述二維不可壓縮流場的標量函數，其等值線可對應流線，常用於動力氣象與流體分析。',
        'specific humidity': '單位濕空氣總質量中所含水汽質量的比值，為描述大氣含濕量的基本熱力變數之一。',
        'storm surge': '受強風、低氣壓及海岸地形等因素影響，使海面在短時間內異常升高的現象，常造成沿海淹水與災害。',
        'sea breeze': '由海陸熱力差異驅動、白天自海向陸吹送的局地環流，常影響沿海地區風向、對流與降水分布。',
        'sea-level pressure': '將測站氣壓折算至平均海平面後所得之氣壓值，便於不同海拔地區進行天氣系統分析與比較。',
        'seiche': '封閉或半封閉水體在外力擾動後形成的駐波式水面振盪，可出現在湖泊、水庫、海灣或港口中。',
        'sensible heat': '不伴隨相變、能直接造成物質溫度升降的熱量，在地表能量收支與邊界層交換中極為重要。',
        'sleet': '由雨滴、雪或融化再凍結粒子組成的冬季降水型態，實際定義可依地區作業慣例略有差異。',
        'smog': '由污染物、煙塵、霧滴及光化學反應共同造成的大氣混濁現象，會影響能見度與人體健康。',
        'sonde': '隨氣球、火箭或其他載具升空之探測儀器，用於量測大氣溫度、濕度、壓力、風等垂直剖面資訊。',
        'sounding': '藉由探空儀、遙測或其他方法取得大氣垂直結構資料的觀測程序與其結果。',
        'squall': '風速在短時間內明顯增強且持續數分鐘以上的強陣風現象，常伴隨對流、鋒面或雷暴系統。',
        'stratosphere': '位於對流層頂以上的大氣層，氣溫一般隨高度上升而增暖，臭氧吸收紫外線為其重要熱源。',
        'stratocumulus': '具有層狀延展與積狀雲塊特徵的低雲，常呈大片或帶狀分布，對輻射與邊界層結構影響顯著。',
        'stratus': '貼近低空、雲底較整齊且水平延展明顯的層狀雲，常伴隨陰天、毛毛雨或低能見度現象。',
        'subsidence': '大氣氣塊向下沉降的運動，可造成絕熱增溫、雲量減少與穩定度增強，常見於高壓系統中。',
        'subtropical high': '位於副熱帶地區的大尺度高壓系統，對季風、水汽輸送、颱風路徑與區域氣候具有重要影響。',
        'supercell': '具有持續中尺度旋轉上升氣流的強烈對流風暴型態，常與大冰雹、龍捲風、強陣風及豪雨有關。',
        'supersaturation': '空氣中的水汽含量超過在該溫度下飽和狀態的現象，是雲滴與冰晶形成的重要條件之一。',
        'surface air temperature': '靠近地表、依標準觀測規範量得之空氣溫度，是氣候監測、預報與環境評估的重要基本量。',
        'surface analysis': '以地面觀測資料繪製並研判氣壓、鋒面、風場與天氣系統分布的綜合天氣分析作業。',
        'surface chart': '呈現地面氣象要素與天氣系統配置的分析圖或預報圖，常用於綜觀診斷與作業判讀。',
        'surface inversion': '發生於近地表層、氣溫隨高度上升而增暖的逆溫結構，常抑制垂直混合並有利污染累積。',
        'surface low': '位於地表分析圖上的低壓中心或低壓系統，常與輻合、上升運動及雲雨天氣有關。',
        'surface pressure': '測站所在位置實際量得之大氣壓力，可作為氣象分析、模式初始場與高度換算的基礎資料。',
        'surface wave': '沿介面或近地表傳播的波動，可見於海洋、水體、地震或大氣邊界附近之擾動現象。',
        'shortwave radiation': '以太陽入射為主、波長較短的電磁輻射通量，是地表與大氣能量收支的重要來源。',
        'snow line': '山區或地表上降雪與降雨、積雪與無雪區之分界高度或界線，受溫度、地形與降水條件影響。',
        'snowmelt': '積雪在增溫、降雨或能量輸入作用下轉變為液態水的過程，對春季逕流與洪水形成十分重要。',
        'snowpack': '地表累積形成的積雪層，其厚度、密度、含水量與層結構為雪文與水文研究的重要參數。',
        'snowfall': '雪晶、雪花或其他固態冰粒自雲中降落至地面的降水現象或其累積量。',
        'snowflake': '由冰晶聚合成的雪之基本顆粒，形狀受溫度、濕度與成長環境控制。',
        'systematic error': '量測或計算結果中持續朝同一方向偏離真值的誤差成分，常由儀器校正、方法假設或環境偏差造成。',
        'systematic observations': '依固定規範、時間、位置或程序持續進行的觀測作業，以確保資料具有可比較性與長期一致性。',
        'Système Internationale': '即國際單位制，為科學與工程領域統一採用的標準計量單位系統。',
        'syzygy': '天體大致排列於同一直線的幾何配置，常見於朔、望等情形，並會影響潮汐強度。',
    }
    if term in exact:
        return exact[term]

    if re.fullmatch(r'[A-Z0-9][A-Z0-9\-– ]*', term):
        return f'「{term}」為氣象、海洋、水文、遙測、航空或地球科學領域常用之縮寫、代號或分類名稱；其具體意義須依專業語境判定。'

    rules = [
        ('radar', f'指與「{zh}」相關的雷達系統、觀測設備或其回波產品，用於偵測目標位置、強度、速度或結構特徵。'),
        ('radiation', f'指與「{zh}」相關的輻射能量、通量、收支或傳輸過程，是天氣與氣候系統能量交換的重要環節。'),
        ('rain', f'指與「{zh}」相關的降雨、雨量、雨滴微物理或降水分析概念。'),
        ('snow', f'指與「{zh}」相關的降雪、積雪、雪晶微物理或雪文過程。'),
        ('storm', f'指與「{zh}」相關的風暴系統、劇烈天氣現象或其演變特徵。'),
        ('surge', f'指與「{zh}」相關的水位、流量、電訊或物理量之快速增強或突升現象。'),
        ('runoff', f'指與「{zh}」相關的地表逕流、流域集水或水文輸送過程。'),
        ('river', f'指與「{zh}」相關的河川、水道或其水文地貌特徵。'),
        ('ridge', f'指與「{zh}」相關的高壓脊、波脊或地形脊狀結構，常用於描述場型延伸與分布。'),
        ('ridge', f'指與「{zh}」相關的高壓脊、波脊或地形脊狀結構，常用於描述場型延伸與分布。'),
        ('rotation', f'指與「{zh}」相關的旋轉、轉動或渦旋運動特徵，可用於描述流體、地球或儀器系統之運動。'),
        ('reflection', f'指與「{zh}」相關的反射作用、反照特性或回波訊號，用於輻射、遙測或波動傳播分析。'),
        ('refraction', f'指與「{zh}」相關的折射現象，即波動或輻射通過介質時因速度改變而偏折。'),
        ('ratio', f'指「{zh}」所代表的比值量，用於表徵兩項物理量之相對關係與變化特徵。'),
        ('range', f'指與「{zh}」相關的距離範圍、變動區間或量測可及範圍。'),
        ('rate', f'指與「{zh}」相關的變化率、速率或通量強度，用於量化單位時間內的增減情形。'),
        ('region', f'指以「{zh}」命名的區域、層區或空間範圍，常用於描述特定物理過程發生之位置。'),
        ('record', f'指與「{zh}」相關的觀測紀錄、資料登錄或長期統計結果。'),
        ('response', f'指系統對「{zh}」所代表外力、擾動或邊界條件變化的反應特徵。'),
        ('resolution', f'指與「{zh}」相關的解析度或分辨能力，可描述時間、空間、光譜或儀器辨識精細程度。'),
        ('roughness', f'指地表、介面或材質之粗糙程度，會影響阻力、湍流交換與流場結構。'),
        ('runway', f'指與航空跑道之觀測、狀態、能見度或作業條件相關的專業術語。'),
        ('satellite', f'指與「{zh}」相關的人造衛星、衛星觀測系統或遙測產品。'),
        ('salinity', f'指海水或其他水體中溶解鹽類含量及其分布特徵，為海洋與水文分析的重要參數。'),
        ('sea', f'指與海洋、海面、海冰、海氣交互作用或海岸過程相關的專業概念。'),
        ('sediment', f'指與沉積物、輸砂、搬運或沉積作用相關的地球科學與水文術語。'),
        ('sensor', f'指量測「{zh}」相關物理量之感測元件、探測器或儀器組件。'),
        ('shear', f'指流場在空間上之速度或應變差異，可用於描述風切、流體變形及動力不穩定特徵。'),
        ('shelf', f'指陸棚、平台或其對應之海洋、冰體或地形單元。'),
        ('signal', f'指與「{zh}」相關的訊號特徵、波形、傳輸或分析結果。'),
        ('slope', f'指與坡度、斜率、地形傾斜或變量隨位置變化相關的量值或概念。'),
        ('soil', f'指與土壤性質、土壤水分、地表交換或陸面過程相關的術語。'),
        ('solar', f'指與太陽輻射、太陽活動、日照幾何或其地球環境效應相關的概念。'),
        ('spectrum', f'指與「{zh}」相關的頻譜分布，用於分析能量、變異或訊號在頻率空間中的配置。'),
        ('speed', f'指與「{zh}」相關的速度、速率或移動快慢之量測與描述。'),
        ('spray', f'指由風浪、破碎、噴灑或機械作用產生的細小液滴或其輸送現象。'),
        ('stability', f'指大氣、海洋或流體系統對擾動之穩定或不穩定特性，是診斷對流與混合的重要概念。'),
        ('station', f'指觀測站、測站、基地或固定量測位置相關之專業名稱。'),
        ('stream', f'指與氣流、水流、洋流或狹長輸送帶狀結構相關的專業概念。'),
        ('stress', f'指流體、固體或界面所受之應力、剪應力或力學作用量。'),
        ('temperature', f'指與「{zh}」相關的溫度量、溫度場或熱狀態特徵。'),
        ('therm', f'指與熱力、溫度或熱能傳輸過程相關的術語。'),
        ('thunder', f'指與雷暴、雷聲、強對流或其伴隨電現象相關的專業概念。'),
        ('trough', f'指與槽線、低壓槽或波谷結構相關的天氣與流場特徵。'),
        ('turbulence', f'指與亂流、渦動或隨機擾動混合過程相關的流體動力概念。'),
        ('type', f'指某一觀測、天氣、儀器、地貌或統計對象之分類型式。'),
        ('vector', f'指「{zh}」所代表的向量診斷量，常用於分析流體運動、強迫機制與場型結構。'),
        ('velocity', f'指與「{zh}」相關的速度向量、運移速度或流速結構。'),
        ('vortex', f'指與渦旋、旋渦或旋轉流場相關的動力結構。'),
        ('wave', f'指與「{zh}」相關的波動、擾動或傳播現象，可見於大氣、海洋、水文或電磁系統。'),
        ('water', f'指與「{zh}」相關的水體、水文狀態、水量平衡或含水特徵。'),
        ('wind', f'指與「{zh}」相關的風場、局地風、環流或風速風向特徵。'),
        ('zone', f'指與「{zh}」相關的地帶、分區或特定作用範圍。'),
        ('index', f'指以「{zh}」為名之指標，用於量化特定氣象、水文、海洋或環境狀態的強弱與變化。'),
        ('coefficient', f'指「{zh}」所代表的係數或經驗參數，用於表徵物理過程、統計關係或模式設定。'),
        ('equation', f'描述「{zh}」相關物理量之間關係、守恆條件或近似動力平衡的方程式。'),
        ('method', f'指用於分析、估算、觀測、計算或作業處理「{zh}」之方法、程序或技術。'),
        ('theory', f'指與「{zh}」相關的理論架構，用以解釋其形成機制、數學關係或預報意涵。'),
        ('model', f'指模擬或描述「{zh}」相關現象之概念模型、數值模式或理論架構。'),
        ('layer', f'指大氣、海洋、土壤、冰雪或介質中的層狀結構與其物理性質。'),
        ('cloud', f'指與「{zh}」相關的雲形、雲系或雲物理現象，可反映局地或大尺度大氣狀態。'),
        ('current', f'指與「{zh}」相關的海流、氣流或水體輸送現象，著重其流向、來源、結構與輸送作用。'),
        ('circulation', f'指與「{zh}」相關的環流型態、閉合流動結構或大尺度運動配置。'),
        ('climate', f'指與「{zh}」相關的氣候狀態、長期平均特徵或氣候變率。'),
        ('oscillation', f'指與「{zh}」相關的振盪現象或氣候變率型態，用以描述大氣或海洋系統在時間上的週期性或準週期性變化。'),
        ('front', f'指與「{zh}」相關的鋒面結構，代表不同性質氣團之交界及其伴隨天氣變化。'),
        ('pressure', f'指與「{zh}」相關的氣壓、壓力場或其診斷量，用於描述流體受力與分布狀態。'),
        ('gradient', f'指與「{zh}」相關之空間變化率或梯度量，用於描述物理量隨距離的變化強弱。'),
        ('humidity', f'指與空氣濕度、水汽含量及其時空分布相關的物理量或概念。'),
        ('precipitation', f'指與降水型態、降水量、形成機制或其統計分布相關的專業術語。'),
        ('evaporation', f'指液態水轉變為水汽的相變過程，並常用於描述蒸發量與地表水分通量。'),
        ('condensation', f'指水汽轉變為液態水的凝結過程，為雲霧與降水形成的重要機制之一。'),
    ]
    for key, desc in rules:
        if key in low:
            return desc

    if low.startswith('semi'):
        return f'「{term}」為帶有「半」、「準」或部分週期／部分結構特性的專業術語，實際意義需依學科語境判定。'
    if low.startswith('sub'):
        return f'指位於較低層次、次級尺度、下伏位置或次分類別的「{zh}」概念，常見於大氣、海洋與水文分層描述。'
    if low.startswith('super'):
        return f'指具有增強、超常、超尺度或高度發展特性的「{zh}」概念，常用於描述劇烈天氣、物理狀態或作業分類。'
    if low.startswith('syn'):
        return f'指與綜合、同時、共生或綜觀尺度分析相關的「{zh}」概念，常見於天氣診斷與系統描述。'
    if low.startswith('strato') or low.startswith('strati'):
        return f'指與層狀雲、大氣層結構或平流層環境相關的「{zh}」專業概念。'
    if low.startswith('storm'):
        return f'指與「{zh}」相關的風暴、對流系統或劇烈天氣現象及其影響。'
    return f'指與「{zh}」相關的氣象、海洋、水文、遙測、航空或地球科學專業術語；其內涵依專業語境可涉及物理過程、觀測量、環流結構、統計方法、儀器系統或環境現象。'


def polish(defn: str) -> str:
    s = defn.strip()
    s = s.replace('  ', ' ')
    s = s.replace('依專業語境可涉及', '依專業語境可涉及')
    s = s.replace('用於量化特定氣象、水文、海洋或環境狀態', '用於量化特定氣象、水文、海洋或環境狀態')
    s = s.replace('可見於大氣、海洋、水文或電磁系統', '可見於大氣、海洋、水文或電磁系統')
    if not s.endswith('。'):
        s += '。'
    s = s.replace('。。', '。')
    return s

for letter in ['r', 's']:
    seen = set()
    rows = []
    for t in terms:
        if t[:1].lower() != letter:
            continue
        key = t.casefold()
        if key in seen:
            continue
        seen.add(key)
        zh = manual_zh(t)
        defn = polish(classify_definition(t, zh))
        rows.append({
            'english': t,
            'traditional_chinese': zh,
            'definition_cht': defn,
        })
    OUTS[letter].write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding='utf-8')

CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding='utf-8')
print('done', {k: len(json.loads(v.read_text(encoding='utf-8'))) for k, v in OUTS.items()})
