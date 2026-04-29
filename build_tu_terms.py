import json, re, time
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.parse import quote

BASE = Path('/home/node/.openclaw/workspace/met_term')
SRC = BASE / 'source_doc_vw.json'
DATA = BASE / 'data'
CACHE = DATA / '_tu_translate_cache.json'
OUTS = {
    't': DATA / 't_terms_all_cht.json',
    'u': DATA / 'u_terms_all_cht.json',
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
    'T-E index': 'T-E 指數',
    'T-E ratio': 'T-E 比值',
    'T-year event': 'T 年重現期事件',
    'T–S curve': 'T–S 曲線',
    'T–S diagram': 'T–S 圖',
    'T–S relation': 'T–S 關係',
    "t'' test": 't'' 檢定',
    'TAF': '機場終端區預報',
    'Television and Infrared Observation Satellite': '電視與紅外觀測衛星',
    'TEMPAL code': 'TEMPAL 碼',
    'Tethered balloon': '繫留氣球',
    'Teweles–Wobus index': '特韋萊斯－沃布斯指數',
    'TGF': '熱陣風因子',
    'TIROS': '電視紅外觀測衛星',
    'TIROS Operational System': 'TIROS 作業系統',
    "TIROS-N'' Operational Vertical Sounder": 'TIROS-N 作業垂直探測儀',
    'TKE': '亂流動能',
    'TOMS': '臭氧總量測繪光譜儀',
    'TOVS': 'TIROS 作業垂直探測系統',
    'Tower of the Winds': '風塔',
    'Townsend support': '湯森支撐',
    'Trade winds': '信風',
    'throughfall': '穿落雨',
    'throughflow': '壤中流',
    'tailwind': '順風',
    'tailwater': '尾水',
    'tail Doppler radar': '尾部都卜勒雷達',
    'Taiwan Warm Current': '臺灣暖流',
    'tangential wind': '切向風',
    'teleconnection': '遙相關',
    'telecommunication': '電信通訊',
    'telemetry': '遙測',
    'telephotometer': '遙光度計',
    'telephotometry': '遙光度測定',
    'Temperate zone': '溫帶',
    'temperate belt': '溫帶',
    'type-β leader': 'β 型先導',
    'Traditional aneroid': '傳統空盒氣壓計',
    'trajectory': '軌跡',
    'trajectory analysis': '軌跡分析',
    'trajectory equation': '軌跡方程',
    'Transpiration': '蒸散作用',
    'Tropical meteorology': '熱帶氣象學',
    'Tropical Rainfall Measuring Mission': '熱帶降雨測量任務',
    'Tropical storm': '熱帶風暴',
    'tropical upper-tropospheric trough': '熱帶上對流層槽',
    'Tropical Wind Energy Conversion and Reference Level Experiment': '熱帶風能轉換與參考層實驗',
    'TROWAL': '暖空氣舌槽',
    'TRS': '熱帶氣旋',
    'TSTORM': '雷暴',
    'TTAA': '高空氣象編碼 TTAA',
    'TTBB': '高空氣象編碼 TTBB',
    'TTCC': '高空氣象編碼 TTCC',
    'TTDD': '高空氣象編碼 TTDD',
    'TUTT': '熱帶上對流層槽',
    'TWT': '雙程傳播時間',
    'Typhoon': '颱風',
    'u index': 'u 指數',
    'U.S. airways code': '美國航路代碼',
    'UARS': '高層大氣研究衛星',
    'UHF': '超高頻',
    "Ulloa's ring": '烏略亞環',
    'ultra high frequency': '超高頻',
    'ultraviolet': '紫外線',
    'ultraviolet index': '紫外線指數',
    'Upper Atmosphere Research Satellite': '高層大氣研究衛星',
    'UTC': '協調世界時',
    'UV': '紫外線',
    'UV and IR hygrometers': '紫外與紅外濕度計',
    'UV-A': 'A 波段紫外線',
    'UV-B': 'B 波段紫外線',
    'UV-C': 'C 波段紫外線',
}

manual_def = {
    'T-year event': '在統計上平均每 T 年發生一次、或年超越機率約為 1/T 的水文或氣象極端事件，常用於工程設計與風險評估。',
    'T–S diagram': '以溫度與鹽度為座標繪製海水性質的圖解工具，可用於辨識水團、混合作用與海洋層結構。',
    'tabular iceberg': '頂部平坦、邊緣近於陡直的大型板狀冰山，通常由冰棚崩解形成。',
    'TAF': '機場終端區預報之國際標準航空天氣預報產品，用於提供機場附近一定時段內之風、能見度、天氣與雲況資訊。',
    'taiga': '分布於高緯寒溫帶地區、以針葉林為主的寒帶森林生態區，對區域地表能量與水文循環具有重要影響。',
    'tailwind': '沿運動方向吹送的背景風，會增加飛行器或移動物體相對地面的前進速度。',
    'tailwater': '位於水工構造物、渠道或水壩下游的受控水位或尾水區，會影響出流條件與能量消散。',
    'telluric lines': '地球大氣吸收或發射所形成的光譜線，常出現在太陽或恆星光譜觀測中，可用於大氣成分分析與光譜校正。',
    'temperate climate': '四季較分明、年溫差與降水型態適中的中緯度氣候類型。',
    'Tethered balloon': '以纜繩固定於地面、可搭載感測器進行近地層與邊界層觀測的氣球平台。',
    'tethersonde': '懸掛於繫留氣球上的探空儀器，用於量測低層大氣之溫度、濕度、風與壓力結構。',
    'tetroon': '可在近中性浮力條件下隨氣流漂移的四面體追蹤氣球，用於研究氣流輸送與擴散。',
    'teleconnection': '相距甚遠的兩個或多個區域之大氣海洋異常彼此具有統計關聯的現象，是氣候診斷與季節預報的重要概念。',
    'telemetry': '將感測器量得的資料以無線或有線方式遠距傳送至接收端的技術。',
    'thawing index': '在一定期間內日平均氣溫高於冰點部分的累積溫度指標，常用於凍土、融雪與工程評估。',
    'theta-e chart': '以等效位溫等熱力參數表示大氣狀態的圖表，用於分析空氣團穩定度與潛在對流能量。',
    'thermocline': '水體中溫度隨深度快速變化的層結，常分隔表層混合層與深層水體。',
    'thermocouple': '利用兩種不同金屬接點溫差產生熱電勢以量測溫度的感測器。',
    'thermodynamic diagram': '以壓力、溫度與相關熱力參數構成的大氣分析圖，用於判讀穩定度、雲底、對流與探空結構。',
    'thermodynamics': '研究能量、熱、功及其轉換規律的學科，是大氣熱力與相變分析的重要基礎。',
    'throughfall': '降水穿過林冠空隙或沿枝葉滴落後到達地表的部分，是森林水文研究中的重要降水分量。',
    'throughflow': '水分在土壤層內沿坡向側向移動的壤中流過程，常影響坡地逕流形成。',
    'thickness': '兩個等壓面之間的位勢高度差，常用於表徵該層平均虛溫與冷暖空氣分布。',
    'thunderstorm': '由深對流發展形成、伴隨雷電、陣風、強降雨或冰雹等劇烈天氣的對流風暴。',
    'thunderstorm cell': '雷暴系統中具獨立上升與下沉氣流結構的對流單體。',
    'TIROS': '美國早期電視紅外觀測衛星系列，開啟了作業氣象衛星觀測的先河。',
    'TKE': '單位質量亂流速度擾動所對應的平均動能，是描述亂流強度的重要動力量。',
    'TOMS': '搭載於衛星上的臭氧總量遙測儀器，用於觀測全球總臭氧分布與變化。',
    'TOVS': 'TIROS 系列作業衛星上的垂直探測系統，用於反演大氣溫度與濕度垂直結構。',
    'trade inversion': '信風帶下沉運動所造成的低層逆溫層，常限制對流雲頂高度並影響海洋邊界層結構。',
    'Trade winds': '副熱帶高壓吹向赤道低壓帶的東風帶，是熱帶大尺度環流的重要組成。',
    'trajectory': '流體微粒或氣塊隨時間移動所描繪的路徑。',
    'trajectory analysis': '利用氣塊前向或後向軌跡追蹤空氣來源、傳輸途徑與擴散影響的分析方法。',
    'transient eddy': '生命期有限、隨時間快速演變的渦動或擾動成分，常用於描述天氣尺度變率與動量熱量輸送。',
    'transmissometer': '量測大氣透射率或消光程度的儀器，常用於能見度與機場觀測。',
    'transpiration': '植物經由氣孔將水分以水汽形式釋放至大氣中的過程，是陸氣水分交換的重要組成。',
    'tropopause': '對流層與平流層之間的大氣分界層，常表現為溫度直減率顯著改變。',
    'tropopause fold': '高空鋒生或急流附近平流層空氣向下伸入對流層的褶皺結構，常與臭氧高值、乾侵入及晴空亂流有關。',
    'troposphere': '大氣最接近地表的一層，天氣現象與多數水汽活動主要發生於此。',
    'trough': '氣壓場或高度場中向低值延伸的槽狀區域，常伴隨輻合、抬升與天氣變化。',
    'TROWAL': '閉塞鋒系統中暖濕空氣向高空抬升所形成的暖空氣舌槽結構，常與持續性降水帶相連。',
    'TRS': '熱帶氣旋之作業縮寫，可泛指在熱帶海洋上發展的旋轉性低壓風暴系統。',
    'turbulence': '流體中速度、溫度或其他物理量呈現不規則脈動與強烈混合作用的流動狀態。',
    'turbulence kinetic energy': '由三向速度擾動所構成的單位質量平均動能，用於定量描述亂流強度。',
    'Typhoon': '在西北太平洋或南海生成、中心附近最大持續風達颶風等級的熱帶氣旋。',
    'typical year': '依長期統計條件選取、可代表某地常年氣候特徵的典型年度資料。',
    'u index': '以風場或統計量之 u 分量為核心所建立的指標，其精確定義需依所屬分析方法或資料產品判定。',
    'UARS': '美國用於研究高層大氣化學、輻射與動力過程的人造衛星任務。',
    'UHF': '頻率介於甚高頻與特高頻之間的電磁波段，常用於雷達、通訊與遙測系統。',
    "Ulloa's ring": '在雲霧或濕潤大氣中由光散射形成的環狀光學現象。',
    'ultimate infiltration capacity': '在既定土壤與地表條件下，經長時間降雨後所趨近的穩定最大入滲能力。',
    'ultrafine particles': '粒徑極小、通常小於 0.1 微米的氣膠粒子，對空氣品質、能見度與健康影響研究十分重要。',
    'ultraviolet': '波長短於可見光紫端的電磁輻射，常用於輻射、生物效應與大氣光化學研究。',
    'undercatch': '降水量器因風場、飛濺或裝置效應而使實際量測值偏低的系統性低估現象。',
    'underflow': '密度較大的流體沿較輕流體下方前進的底層流動，常見於河口、湖泊或海洋分層環境。',
    'undersun': '由冰晶反射日光於觀測者下方形成的亮斑光象，常見於高空飛行觀測。',
    'universal time': '以地球自轉為基準的標準時間系統，現代作業常以協調世界時加以實現。',
    'unstable lapse rate': '垂直溫度遞減率足以促使抬升氣塊維持或增強浮力的不穩定層結。',
    'updraft': '空氣向上的垂直運動，可由加熱、地形抬升、輻合或對流發展所驅動。',
    'upglide': '氣流沿等熵面或較冷空氣上方緩慢抬升的運動，常與層狀雲系及持續性降水相關。',
    'upper air': '相對於近地面而言的大氣高層區域，常指需藉探空、雷達或衛星加以觀測的自由大氣。',
    'Upper Atmosphere Research Satellite': '專門觀測中高層大氣化學、輻射與動力結構的研究衛星。',
    'urban heat island': '都市區因地表材質、人為熱排放與通風條件差異而比周邊郊區偏暖的現象。',
    'urban hydrology': '研究都市化對降雨逕流、滯洪、排水與地表水文反應影響的水文學分支。',
    'urban runoff': '都市地表降水未入滲而沿排水系統或地表快速匯流的逕流。',
    'urban–rural circulation': '由都市與鄉村地表熱力與粗糙度差異所驅動的局地環流系統。',
    'UTC': '全球通用的標準時間系統，以原子時為基礎並透過閏秒與地球自轉保持協調。',
    'UV': '波長短於可見光的紫外電磁輻射總稱。',
    'UV-A': '波長約 315 至 400 奈米的紫外線波段，穿透力較強並可抵達地表。',
    'UV-B': '波長約 280 至 315 奈米的紫外線波段，對生物與光化學作用較為顯著，且受臭氧層影響明顯。',
    'UV-C': '波長約 100 至 280 奈米的短波紫外線，絕大部分會被大氣上層吸收而不易到達地表。',
}


def manual_zh(term: str) -> str:
    return trans_override.get(term) or gtranslate(term)


def acronym_definition(term: str) -> str:
    return f'「{term}」為氣象、海洋、水文、遙測、航空或相關地球科學領域常用之縮寫、代碼、作業產品或儀器名稱；其精確內涵需依專業語境判定。'


def make_definition(term: str, zh: str) -> str:
    if term in manual_def:
        return manual_def[term]

    low = term.lower()
    low_norm = re.sub(r'[^a-z0-9]+', ' ', low).strip()

    if re.fullmatch(r'[A-Z0-9][A-Z0-9\-–/. ]*', term):
        return acronym_definition(term)

    rules = [
        ('index', f'指以「{zh}」為名之指標，用於量化特定氣象、水文、海洋或環境狀態的強弱、異常程度或風險。'),
        ('ratio', f'指「{zh}」所代表的比值量，用於描述兩項物理量或統計量之相對關係。'),
        ('curve', f'指以圖形方式表現「{zh}」相關變量關係的曲線，用於分析趨勢、結構或診斷特性。'),
        ('diagram', f'指呈現「{zh}」相關物理量、分布或關係之圖解工具，常用於分析與作業判讀。'),
        ('relation', f'指描述「{zh}」相關變量之間對應關係、函數形式或物理聯繫的概念。'),
        ('test', f'指用於檢驗「{zh}」相關假設、差異或統計顯著性的測試方法。'),
        ('iceberg', f'指與「{zh}」相關的冰山型態、結構或海冰漂移特徵。'),
        ('climate', f'指「{zh}」所對應的氣候型態、區域氣候條件或其長期平均特徵。'),
        ('glacier', f'指與「{zh}」相關的冰川型態、熱力狀態或演變特徵。'),
        ('forest', f'指與「{zh}」相關的森林生態區或地表覆蓋類型，並與區域氣候及水文過程相互作用。'),
        ('current', f'指與「{zh}」相關的海流、氣流或輸送流系統，重點在其流向、成因及熱鹽或動量輸送作用。'),
        ('wind', f'指與「{zh}」相關的局地風系、盛行風型或風場特徵，著重其形成機制、方向與天氣影響。'),
        ('approximation', f'用於處理「{zh}」相關問題的近似假設，以簡化方程並保留主要物理機制。'),
        ('equation', f'描述「{zh}」相關物理量、流動關係或診斷計算規則的方程式。'),
        ('theorem', f'指與「{zh}」相關的數學或物理定理，用於說明變量關係、守恆性質或推導基礎。'),
        ('hypothesis', f'指解釋「{zh}」相關現象、近似條件或推論架構的假說。'),
        ('number', f'指用於表徵「{zh}」相關物理機制、無因次特徵或分類條件的數值指標。'),
        ('effect', f'指由特定作用機制造成的「{zh}」現象或影響結果。'),
        ('signal', f'指與「{zh}」相關的觀測訊號、回波、記錄或通訊資訊。'),
        ('acceleration', f'指與「{zh}」相關的加速度分量或速度變化率。'),
        ('stress', f'指流體、地表或介質內與「{zh}」相關的應力作用或力通量。'),
        ('stresses', f'指流體、地表或介質內與「{zh}」相關的應力作用或力通量。'),
        ('polynomial', f'指用於近似、展開或分析「{zh}」相關變量關係的多項式表達。'),
        ('zone', f'指與「{zh}」相關的帶狀或區域性空間分區。'),
        ('belt', f'指沿特定緯度、地形或環境條件延伸的帶狀區域。'),
        ('photometer', f'指量測光強、亮度、透光度或輻射強度的光度儀器。'),
        ('photometry', f'指量測與分析光強、亮度或輻射訊號的光度測定方法。'),
        ('telecommunication', f'指將觀測、通訊或控制訊號進行遠距傳送的電信技術或系統。'),
        ('teleconnection', f'指遙遠地區之間大氣或海洋異常彼此相關的遙相關型態。'),
        ('telemetry', f'指將量測資料自遠端平台傳送至接收站的遙測技術。'),
        ('radiation', f'指與「{zh}」相關的輻射能量、通量、收支或傳輸過程。'),
        ('formula', f'指用於表達「{zh}」相關經驗關係、計算規則或近似解的公式。'),
        ('balloon', f'指與「{zh}」相關的大氣觀測氣球平台、載具或其觀測作業。'),
        ('sonde', f'指用於量測大氣狀態的探空儀器或感測系統。'),
        ('probability', f'指描述「{zh}」相關事件、微觀狀態或統計結果發生可能性的機率概念。'),
        ('thermometer', f'指用於量測溫度或熱狀態的溫度計儀器。'),
        ('thermoscope', f'指用於顯示或比較溫度變化的早期測溫裝置。'),
        ('temperature', f'指與「{zh}」相關的溫度量、熱狀態或其空間時間變化特徵。'),
        ('layer', f'指與「{zh}」相關的大氣、海洋、湖泊或地表層結構，常依熱力、密度、濕度或動力特徵區分。'),
        ('air mass', f'指具有相對一致溫濕特性的廣大空氣體，並與其源地及移動路徑密切相關。'),
        ('air', f'指與「{zh}」相關的大氣狀態、空氣性質或其穩定度特徵。'),
        ('visibility', f'指大氣條件下目標物可被辨識的視程或能見度狀態。'),
        ('ceiling', f'指最低重要雲層底高或對航空作業具限制性的雲底高度條件。'),
        ('conductivity', f'指土壤、介質或流體傳導水分、熱量、電流或其他物理量的能力。'),
        ('hydrograph', f'指流量、水位或逕流隨時間變化的歷線圖，用於水文分析。'),
        ('distribution', f'指與「{zh}」相關的統計分布、空間分布或頻率配置。'),
        ('oscillation', f'指與「{zh}」相關的振盪現象或變率型態，用於描述系統的週期性或準週期性變化。'),
        ('equilibrium', f'指與「{zh}」相關的平衡狀態，表示系統內主要力、通量或熱力過程達相對穩定配置。'),
        ('motion', f'指與「{zh}」相關的運動型態、運移過程或流體動力特徵。'),
        ('aquifer', f'指可儲存並傳導地下水的含水層或相關水文地質單元。'),
        ('shear', f'指風速或流速隨空間變化形成的切變結構，常影響亂流與對流發展。'),
        ('thaw', f'指與「{zh}」相關的冰雪或凍土融解現象、過程或其影響。'),
        ('thermal', f'指與「{zh}」相關的熱力狀態、熱量傳輸或由熱作用驅動的現象。'),
        ('thermo', f'指與「{zh}」相關的熱力、溫度或能量轉換概念。'),
        ('cloud', f'指與「{zh}」相關的雲形、雲系、雲層或雲物理特徵。'),
        ('storm', f'指與「{zh}」相關的風暴、劇烈天氣系統或對流組織。'),
        ('thunder', f'指與「{zh}」相關的雷暴、雷電聲光現象或其伴隨天氣。'),
        ('snow', f'指與「{zh}」相關的降雪、積雪或雪況物理過程。'),
        ('rain', f'指與「{zh}」相關的降雨、雨量或降水過程。'),
        ('water', f'指與「{zh}」相關的水體、水量、水相或大氣含水狀態。'),
        ('gauge', f'指用於量測「{zh}」相關量值的雨量器、計量器或監測裝置。'),
        ('wave', f'指與「{zh}」相關的波動、擾動或傳播現象，可發生於大氣、海洋或電磁系統。'),
        ('pollutants', f'指排放至大氣或環境中的污染物質，會影響空氣品質、能見度、輻射或人體健康。'),
        ('transmission', f'指與「{zh}」相關的能量、訊號、電磁波或輻射傳遞過程。'),
        ('transit', f'指與「{zh}」相關的通過、輸送或過境現象。'),
        ('transport', f'指與「{zh}」相關的物質、能量、動量或污染物輸送過程。'),
        ('transmittance', f'指「{zh}」所對應的透射率量，用於描述輻射或光束穿透介質後的保留比例。'),
        ('transmissivity', f'指介質對輻射、光線或流體傳輸之透過能力，可用於輻射傳輸或地下水分析。'),
        ('transmissometer', f'指量測大氣透射率、能見度或消光程度的儀器。'),
        ('transmitter', f'指發射電磁訊號、能量或脈衝的裝置，常見於雷達與遙測系統。'),
        ('sky cover', f'指天空被雲層遮蔽的覆蓋程度或其觀測分類。'),
        ('tropical', f'指與熱帶地區大氣環流、氣候條件、降水型態或天氣系統相關的概念。'),
        ('upper-tropospheric trough', f'指位於對流層上部的槽狀低值系統，常影響熱帶擾動發展與高空環流配置。'),
        ('tropopause', f'指對流層頂及其相關結構、變化或診斷特性。'),
        ('troposphere', f'指與對流層相關的大氣結構、物理過程或診斷量。'),
        ('trough', f'指與「{zh}」相關的槽狀低值系統、延伸低壓帶或其動力結構。'),
        ('turbidity', f'指介質因懸浮粒子造成混濁與消光的程度，常用於水體與大氣光學分析。'),
        ('turbulence', f'指與「{zh}」相關的亂流流動、擾動統計量或混合作用特徵。'),
        ('turbulent', f'指具有亂流性質的流場、邊界層或輸送過程。'),
        ('flow', f'指與「{zh}」相關的流動型態、平均流場或輸送結構。'),
        ('flux', f'指單位時間穿過單位面積之「{zh}」通量，用於量化質量、熱量、水氣或動量輸送。'),
        ('transport', f'指與「{zh}」相關之物質、能量、水氣或動量輸送現象。'),
        ('spectrum', f'指與「{zh}」相關的頻譜分布，用於分析能量、變異或尺度特徵。'),
        ('energy', f'指與「{zh}」相關的能量形式、能量收支或轉換過程。'),
        ('length scales', f'指表徵「{zh}」相關渦動、結構或變異空間尺度的特徵長度。'),
        ('model', f'指用於表示「{zh}」相關過程、結構或變量關係的理論、概念或數值模式。'),
        ('year', f'指與「{zh}」相關的年尺度統計、代表年資料或週期性氣候特徵。'),
        ('infiltration', f'指降水或地表水進入土壤孔隙的入滲過程及其能力。'),
        ('particles', f'指懸浮於大氣或流體中的微粒物質，可影響輻射、能見度、雲滴形成與健康風險。'),
        ('ultraviolet', f'指與「{zh}」相關的紫外輻射波段、強度或其生物與光化學效應。'),
        ('underflow', f'指密度流沿較輕流體下方推進的底層流動現象。'),
        ('lapse rate', f'指大氣溫度隨高度變化的遞減率，用於判斷層結穩定度。'),
        ('updraft', f'指空氣向上運動的上升氣流或其相關結構。'),
        ('upglide', f'指氣流沿等熵面或冷空氣上方緩升的抬升運動。'),
        ('upper air', f'指自由大氣高層之觀測、分析或作業概念。'),
        ('hygrometers', f'指量測空氣水汽含量、相對濕度或相關濕度參數的儀器。'),
        ('atmosphere', f'指與「{zh}」相關的大氣層結、組成、動力或輻射特徵。'),
        ('urban', f'指與都市地表、人為熱源、排水系統或都市氣候效應相關的概念。'),
        ('runoff', f'指降水未入滲而沿地表或排水系統匯流的逕流過程。'),
        ('circulation', f'指與「{zh}」相關的局地或大尺度環流結構及其輸送作用。'),
        ('hydrology', f'指研究「{zh}」相關降水、逕流、入滲與排水反應的水文概念或分支。'),
        ('heat island', f'指因地表熱力與人為活動差異造成局地增溫的都市氣候現象。'),
        ('time', f'指與「{zh}」相關的時間系統、時間尺度或時制概念。'),
    ]

    for key, desc in rules:
        key_norm = re.sub(r'[^a-z0-9]+', ' ', key.lower()).strip()
        if re.search(r'(^| )' + re.escape(key_norm) + r'( |$)', low_norm):
            return desc

    if low.startswith('thermo'):
        return f'指與「{zh}」相關的熱力學狀態、溫度結構、熱能交換或其觀測診斷概念。'
    if low.startswith('tropo'):
        return f'指與「{zh}」相關的對流層結構、熱帶大氣或高空環流特徵。'
    if low.startswith('trans'):
        return f'指與「{zh}」相關的跨介質、跨區域或過程性傳遞、輸送、透射或轉換現象。'
    if low.startswith('urban'):
        return f'指與都市地表特性、人為熱排放、排水系統或都市氣候環境相關的專業術語。'
    if low.startswith('ultra'):
        return f'指與「{zh}」相關之極高頻、極細粒徑或超高強度等特徵的專業術語。'
    if low.startswith('under'):
        return f'指與「{zh}」相關的下方結構、低估效應、下層流動或光學現象。'
    if low.startswith('up'):
        return f'指與「{zh}」相關的上升、上方層結、向上輸送或抬升運動概念。'

    return f'指與「{zh}」相關的氣象、海洋、水文、遙測、環境或地球科學專業術語；其具體涵義仍需依實際學科脈絡與使用情境判定。'


def polish(defn: str) -> str:
    s = re.sub(r'\s+', ' ', defn).strip()
    s = s.replace(' ，', '，').replace(' 。', '。').replace(' ；', '；').replace(' ：', '：')
    s = s.replace('之「', '的「')
    s = s.replace('其具體涵義仍需依實際學科脈絡與使用情境判定。', '其具體涵義仍需依實際學科脈絡與使用情境判定。')
    if not s.endswith(('。', '；')):
        s += '。'
    return s

for letter in ['t', 'u']:
    seen = set()
    ordered = []
    for t in terms:
        if t[:1].lower() != letter:
            continue
        key = t.casefold()
        if key in seen:
            continue
        seen.add(key)
        ordered.append(t)

    rows = []
    for idx, term in enumerate(ordered, 1):
        zh = manual_zh(term)
        defn = polish(make_definition(term, zh))
        rows.append({
            'english': term,
            'traditional_chinese': zh,
            'definition_cht': defn,
        })
        if idx % 25 == 0:
            print(letter, idx, 'of', len(ordered), flush=True)

    OUTS[letter].write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding='utf-8')
    print('wrote', letter, len(rows), OUTS[letter])
    print('first', ordered[0])
    print('last', ordered[-1])

CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding='utf-8')
