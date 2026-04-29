import json, re, time
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.parse import quote

SRC = Path('/home/node/.openclaw/workspace/met_term/source_doc_no.json')
DATA = Path('/home/node/.openclaw/workspace/met_term/data')
CACHE = DATA / '_lm_translate_cache.json'
OUT_L = DATA / 'l_terms_all_cht.json'
OUT_M = DATA / 'm_terms_all_cht.json'

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

def gtranslate(text):
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
    'La Niña':'反聖嬰','labile':'不穩定的','laboratory tank':'實驗水槽','Labrador Current':'拉布拉多海流',
    'lacustrine climate':'湖泊型氣候','lag':'時滯','Lagrangian mean current':'拉格朗日平均流','Lagrangian timescale':'拉格朗日時間尺度',
    'lake breeze':'湖風','lake effect':'湖泊效應','lake evaporation':'湖泊蒸發','lake ice':'湖冰','lake surface temperature':'湖面溫度',
    'lake-effect snow':'湖效應雪','lake-effect snowstorm':'湖效應暴風雪','Lambert conic projection':'蘭伯特圓錐投影',
    "Lambert's formula":'蘭伯特公式',"Lambert's law":'蘭伯特定律','Lambertian surface':'蘭伯特表面',
    'laminar boundary layer':'層流邊界層','laminar flow':'層流','laminar sublayer':'層流底層','land breeze':'陸風','land evaporation':'陸面蒸發',
    'land ice':'陸地冰體','landing forecast':'著陸預報','Landsat':'陸地衛星','landspout':'陸龍捲','langley':'蘭利',
    'Langmuir cells':'朗繆爾胞','Langmuir circulation':'朗繆爾環流','Langmuir layer':'朗繆爾層','Langmuir number':'朗繆爾數',
    'Langmuir probe':'朗繆爾探針','latent energy':'潛能量','latent heat':'潛熱','latent instability':'潛在不穩定','latent-heat flux':'潛熱通量',
    'latitude':'緯度','lava flow':'熔岩流','lee wave':'背風波','left exit region':'左出口區','left mover':'左移風暴',
    'level of free convection':'自由對流高度','level of no motion':'無流層','lidar':'光達','lifting condensation level':'抬升凝結高度',
    'light breeze':'微風','light echo':'弱回波','lightning':'閃電','lightning channel':'閃電通道','lightning discharge':'閃電放電',
    'littoral current':'沿岸流','local standard time':'地方標準時','Loess Plateau':'黃土高原','long wave':'長波','longshore current':'沿岸流',
    'longwave radiation':'長波輻射','lookup table':'查找表','low':'低壓','low cloud':'低雲','low clouds':'低雲','low-level jet':'低空噴流',
    'low pressure':'低壓','low-pressure area':'低壓區','low-pressure system':'低壓系統','lull':'暫歇','luminance':'亮度','luminescence':'發光',
    'luminous efficiency':'發光效率','lunar atmospheric tide':'月球大氣潮','lunar day':'太陰日','lunar rainbow':'月虹','lunar tide':'月潮',
    'Lyman alpha emission line':'萊曼α發射線','Lyman-alpha hygrometer':'萊曼α濕度計','lysimeter':'蒸滲儀',
    'M component':'M分量','M meter':'M計','M-region':'M層區','macroclimate':'大氣候','macroturbulence':'大尺度亂流',
    'magnetic declination':'磁偏角','magnetic equator':'磁赤道','magnetic field':'磁場','magnetic meridian':'磁子午線',
    'magnetic north pole':'磁北極','magnetic storm':'磁暴','magnetogram':'地磁記錄圖','magnetograph':'磁力儀','magnetometer':'磁力計',
    'magnitude':'量級','main standard time':'主要標準時','main telecommunications network':'主要電信網路',
    'major ridge':'主脊','major trough':'主槽','Maloja wind':'馬洛亞風','Malvinas Current':'馬爾維納斯海流','mamma':'乳房雲',
    'man–machine mix':'人機混合作業','mandatory layer':'強制層','Mandatory level':'強制層位','Manning equation':'曼寧方程',
    'manometer':'壓力計','map plotting':'填圖','map projection':'地圖投影','mapped data':'成圖資料','marine climate':'海洋性氣候',
    'marine inversion':'海洋逆溫','marine layer':'海洋邊界層','maritime air':'海洋氣團','maritime climate':'海洋性氣候',
    'maritime polar air':'海洋極地氣團','maritime tropical air':'海洋熱帶氣團','markov chain':'馬可夫鏈','mass balance':'質量平衡',
    'massif':'山塊','mean':'平均值','mean annual runoff':'多年平均逕流量','mean anomaly':'平均距平','mean circulation':'平均環流',
    'mean sea level':'平均海平面','mean temperature':'平均氣溫','mean wind':'平均風','mechanical turbulence':'機械亂流',
    'median':'中位數','Mediterranean climate':'地中海型氣候','melting level':'融解層位','meridional circulation':'經向環流',
    'mesocyclone':'中尺度氣旋','mesohigh':'中尺度高壓','mesolow':'中尺度低壓','mesonet':'中尺度觀測網','mesopause':'中氣層頂',
    'mesoscale':'中尺度','mesosphere':'中氣層','mesospheric inversion':'中氣層逆溫','meteor':'流星','meteor burst':'流星爆發',
    'meteor radar':'流星雷達','meteor trail':'流星餘跡','meteoric water':'天降水','meteorological drought':'氣象乾旱',
    'meteorological element':'氣象要素','meteorological observation':'氣象觀測','meteorological optical range':'氣象光學視程',
    'meteorological satellite':'氣象衛星','meteorology':'氣象學','methane':'甲烷','microbarograph':'微氣壓自記器','microburst':'微下擊暴流',
    'microclimate':'微氣候','microphysics':'雲微物理學','microscale':'微尺度','mid-latitude':'中緯度','middle cloud':'中雲','middle clouds':'中雲',
    'midtroposphere':'中對流層','mist':'輕霧','mixing depth':'混合層深度','mixing ratio':'混合比','moderate breeze':'和風',
    'moderate rain':'中雨','moderate snow':'中雪','moist adiabat':'濕絕熱線','moist convection':'濕對流','moist instability':'濕不穩定',
    'moisture':'水氣','moisture content':'含水量','moisture flux':'水氣通量','molar concentration':'莫耳濃度','molecular diffusion':'分子擴散',
    'momentum':'動量','momentum flux':'動量通量','monsoon':'季風','monsoon depression':'季風低壓','monsoon onset':'季風爆發',
    'monthly mean':'月平均','mountain breeze':'山風','mountain wave':'山脈波','moving average':'移動平均','mud rain':'泥雨',
    'multicell storm':'多單體風暴','multiple regression':'多元迴歸','Munich chain':'慕尼黑鏈','Muskingum method':'馬斯京根法',
    'Mutatus':'積變雲','Myers rating':'邁爾斯評級'
}

manual_def = {
    'La Niña':'指熱帶中東太平洋海表溫度持續偏冷並伴隨大氣環流異常的 ENSO 冷事件，常影響全球降水、季風與颱風活動分布。',
    'Labrador Current':'北大西洋西北部沿拉布拉多與紐芬蘭外海向南流動的寒流，對海霧、海冰輸送與區域氣候具有重要影響。',
    'lag':'指某一氣象、水文或統計變量對另一變量變化產生反應時所呈現的時間延遲。',
    'Lagrangian mean current':'沿隨流體移動之觀測框架所定義的平均流速，可反映粒子實際漂移與波流交互作用之淨輸送。',
    'Lagrangian timescale':'描述流體微粒沿運動路徑上速度自相關衰減特徵的時間尺度，常用於亂流擴散與粒子輸送研究。',
    'landspout':'在非中氣旋環境下，由近地面渦旋被對流上升氣流拉伸而形成的細長型龍捲，通常與積雲或雷暴初生階段有關。',
    'leaf wetness duration':'植物葉面維持有液態水膜或露滴覆蓋的持續時間，常用於病害風險評估與農業氣象監測。',
    'light freeze':'最低氣溫略低於冰點、足以造成輕微結霜或局部凍害的弱凍事件。',
    'lumped chemical mechanism':'將多種化學物種或反應途徑加以合併簡化後所建立的化學反應機制，用於降低大氣化學模式計算成本。',
    'lake breeze':'白天地表受熱差異使近地面氣流自湖面吹向陸地的局地環流，夜間通常可轉為陸風。',
    'lake-effect snow':'冷空氣越過較暖湖面時獲得水汽與熱量，於下風岸形成增強降雪的現象。',
    'Lambert conic projection':'以圓錐面投影球面的地圖投影法，常用於中緯度地區天氣圖與航空圖製作。',
    'laminar flow':'流體以平滑層狀方式流動、擾動與混合作用較弱的流態，通常與較低雷諾數環境相關。',
    'land breeze':'夜間陸地降溫較快時，近地面氣流由陸地吹向水面的局地環流。',
    'Langmuir circulation':'在風應力與表面波共同作用下，海洋或湖面上層形成沿風向排列之縱向旋轉環流。',
    'latent heat':'物質在相變過程中於溫度近乎不變條件下吸收或釋放的熱量，對大氣能量轉換與對流發展極為重要。',
    'latent instability':'空氣團在抬升並達飽和後，因凝結釋放潛熱而使浮力增強的不穩定特性。',
    'lee wave':'氣流越過地形障礙後在背風側穩定層中產生的重力波，可伴隨雲帶、亂流與下沉增溫。',
    'level of free convection':'氣塊抬升至此高度後，其溫度高於環境並可在正浮力作用下自行上升的層位。',
    'lidar':'利用雷射脈衝量測大氣、雲、氣膠或地表目標回波特性的主動遙測系統。',
    'lifting condensation level':'未飽和空氣塊在乾絕熱抬升過程中首次達到飽和並開始凝結的高度。',
    'lightning':'雲內、雲間或雲地之間電荷快速中和所產生的瞬間大電流放電現象。',
    'longwave radiation':'波長較長、主要由地表與大氣依其溫度向外放射的熱紅外輻射。',
    'low-level jet':'位於邊界層上方或對流層低層的狹窄強風帶，對水汽輸送、對流觸發與污染傳輸具有重要作用。',
    'lull':'指降水、風或風暴活動在事件進行期間出現的短暫減弱或暫停階段。',
    'lunar tide':'由月球引力作用所引起之大氣或海洋週期性潮汐振盪。',
    'Lyman-alpha hygrometer':'利用萊曼 α 紫外吸收特性量測水汽濃度的高靈敏度濕度儀器。',
    'lysimeter':'用於量測土壤水分收支、蒸散作用與滲漏量的裝置，是水文與農業氣象研究的重要設備。',
    'M component':'指向東西或磁場相關座標分解後所得的 M 向分量，實際定義需依所用座標系與專業情境判定。',
    'manometer':'利用液柱高度差、彈性元件或其他感測方式量測氣體或液體壓力的儀器。',
    'meter':'泛指用於量測特定物理量、化學量或環境參數的計量儀器。',
    'multispectral scanner':'可在多個分離波段同步或序列量測地表與大氣輻射訊號的遙測掃描儀器。',
    'Myers rating':'用於描述特定氣象、工程或風險條件等級的邁爾斯評級法；其精確定義需依所屬應用領域判定。',
    'macroclimate':'指大範圍地區在長期平均下所呈現的整體氣候特徵，尺度可達區域、大陸或全球。',
    'magnetic declination':'地理北與磁北之間的水平夾角，會隨地點與時間而變化。',
    'magnetic storm':'地球磁場因太陽活動擾動而產生的劇烈變化現象，可影響高層大氣、通訊與導航系統。',
    'magnetometer':'量測磁場強度或方向的儀器，廣用於地磁監測、太空物理與地球科學觀測。',
    'major ridge':'在大尺度高度場或氣壓場中幅度較大、延伸較明顯的高壓脊結構。',
    'major trough':'在大尺度高度場或氣壓場中幅度較大、延伸較明顯的低壓槽結構。',
    'Maloja wind':'瑞士恩加丁谷地附近在特定地形與壓力分布下出現的局地谷風型強風。',
    'mamma':'懸掛於積雨雲砧部或其他雲底下方、呈袋狀或乳房狀下垂突起的雲體構造。',
    'Manning equation':'明渠流中用以估算平均流速或流量與水力半徑、坡度及糙率關係的經驗公式。',
    'map projection':'將地球曲面位置轉換到平面地圖上的方法，用以表示空間位置、距離、面積或方向。',
    'marine layer':'受海面調節影響、常具有高濕與逆溫特徵的近海邊界層。',
    'maritime polar air':'生成於高緯海洋上、性質偏冷且濕潤的氣團。',
    'maritime tropical air':'生成於低緯暖海面上、性質溫暖且濕潤的氣團。',
    'Markov chain':'一種隨機過程模型，其未來狀態轉移僅依賴當前狀態而與更早歷史無直接關係。',
    'mass balance':'系統在一定時間內輸入、輸出與儲存量之間的守恆關係。',
    'mean sea level':'長期平均後之海面高度基準，常作為測高、地形與氣壓訂正的參考面。',
    'mechanical turbulence':'由地表粗糙度、障礙物或風速垂直切變所產生的亂流。',
    'Mediterranean climate':'夏季乾熱、冬季溫和多雨的副熱帶氣候型態，常見於大陸西岸特定緯度帶。',
    'melting level':'固態降水粒子開始顯著融解的層位，常對雷達亮帶與降水相態判讀十分重要。',
    'meridional circulation':'以南北向輸送為主的大尺度環流，可指大氣或海洋中的經向平均流動結構。',
    'mesocyclone':'對流風暴內部尺度約數公里至數十公里、具持續旋轉特徵的中尺度渦旋。',
    'mesohigh':'由對流冷池或下沉氣流等中尺度過程造成的局地高壓區。',
    'mesolow':'由加熱、輻合或地形等中尺度過程造成的局地低壓區。',
    'mesonet':'以高時空解析度佈設的區域觀測站網，用於監測中尺度天氣與地表環境。',
    'mesopause':'中氣層頂部、溫度通常最低且上接熱層的過渡層。',
    'mesoscale':'介於綜觀尺度與微尺度之間的空間尺度範圍，常涵蓋海風、雷暴系統與地形環流等現象。',
    'mesosphere':'位於平流層之上、熱層之下的大氣層，氣溫通常隨高度遞減。',
    'meteorological drought':'由一段期間降水顯著少於常態所界定的乾旱型態，是其他乾旱類型的氣象起點。',
    'meteorological optical range':'在標準觀測條件下，目標物因大氣消光作用仍可被辨識的氣象光學視程。',
    'meteorological satellite':'搭載可見光、紅外、微波等感測器，用於持續觀測大氣、雲系、海面與地表狀態的人造衛星。',
    'meteorology':'研究大氣現象、天氣系統、氣候變化及其物理過程的科學。',
    'microburst':'自強對流雲底急速下沉並於近地面向外擴散的小尺度強烈下擊暴流，對航空安全威脅甚大。',
    'microclimate':'受地形、植被、建物或地表性質影響而在小範圍內形成的局地氣候。',
    'mixing ratio':'單位乾空氣質量所含水汽質量的比值，是描述大氣含水量的重要變數。',
    'moist adiabat':'飽和空氣塊抬升時在凝結潛熱釋放作用下所遵循的溫度變化曲線。',
    'moist convection':'受水汽凝結釋熱影響而增強之對流運動，是雷暴與深對流發展的關鍵機制。',
    'moisture flux':'單位時間穿過單位面積的水汽輸送量，可用以診斷水氣來源與降水潛勢。',
    'molecular diffusion':'分子隨濃度、溫度或化學勢梯度自發擴散的微觀傳輸過程。',
    'monsoon':'由海陸熱力差與季節性大尺度環流轉換共同驅動、風向與降水具有顯著季節反轉特徵的環流系統。',
    'monsoon depression':'季風槽中發展的低壓擾動，常伴隨廣泛降雨並影響南亞季風天氣。',
    'mountain wave':'穩定氣流越過山脈後於背風側產生的重力波動，可伴隨亂流、轉子與雲列。',
    'mud rain':'降水在下落過程中夾帶大量沙塵、火山灰或其他細粒物質，使雨滴沉降後留下泥狀沉積的現象。',
    'multicell storm':'由多個不同生命期對流單體組成、可持續再生與演變的雷暴系統。',
    'multiple regression':'同時使用多個自變量估計或解釋單一應變量變化的統計方法。',
    'Muskingum method':'以河道蓄洪概念模擬洪水歷線傳遞的經典水文演算法。'
}


def manual_zh(term):
    return trans_override.get(term) or gtranslate(term)


def make_def(term, zh):
    if term in manual_def:
        return manual_def[term]
    low = term.lower()
    low_norm = re.sub(r'[^a-z0-9]+', ' ', low).strip()
    if re.fullmatch(r'[A-Z0-9\-–/.]+', term):
        return f'「{term}」為氣象、海洋、水文、遙測或相關地球科學領域使用之縮寫、代號、儀器或產品名稱；其精確涵義仍需依專業語境判定。'
    rules = [
        ('wind', f'指與「{zh}」相關的局地風系、盛行風型或風場特徵，通常著重其形成機制、地形效應與天氣影響。'),
        ('current', f'指與「{zh}」相關的海流、氣流或輸送流系統，重點在其流向、成因及熱鹽或動量輸送作用。'),
        ('layer', f'指與「{zh}」相關的大氣、海洋、湖泊或地表層結構，常依熱力、密度、濕度或動力特徵區分。'),
        ('cloud', f'指與「{zh}」相關的雲系、雲形或雲微物理特徵，用於描述其外觀、生成條件與對應天氣狀態。'),
        ('ice', f'指與「{zh}」相關的冰相現象、冰體狀態或凍結產物，常應用於寒區氣象、海冰或冰川研究。'),
        ('equation', f'描述「{zh}」相關物理量、流動關係或診斷計算規則的方程式。'),
        ('model', f'用於表示「{zh}」相關過程、系統或變量關係的理論、概念或數值模式。'),
        ('index', f'用於量化「{zh}」相關狀態、強度、異常程度或風險高低的指標。'),
        ('radiation', f'指與「{zh}」相關的輻射傳輸、能量收支或電磁波放射現象。'),
        ('pressure', f'指與「{zh}」相關的壓力狀態、壓力分布或其派生診斷量。'),
        ('forecast', f'指以「{zh}」為主題的預報產品、預測方法或作業結果。'),
        ('observation', f'指與「{zh}」相關的觀測作業、量測資料或分析成果。'),
        ('method', f'指處理「{zh}」相關問題的分析、估算、模擬、分類或推算方法。'),
        ('instability', f'指與「{zh}」相關的不穩定機制，可導致擾動放大、波動增強或對流觸發。'),
        ('approximation', f'用於處理「{zh}」相關問題的近似假設，以簡化方程並保留主要物理機制。'),
        ('temperature', f'指與「{zh}」相關的溫度量、熱狀態或其空間時間分布特徵。'),
        ('water', f'指與「{zh}」相關的水體、水量、水文條件或含水狀態。'),
        ('filter', f'用於擷取、保留或抑制「{zh}」相關訊號或頻率成分的濾波方法或裝置。'),
        ('height', f'指與「{zh}」相關的高度層位、垂直尺度或其診斷量。'),
        ('wave', f'指與「{zh}」相關的波動、擾動或傳播現象，涉及振幅、相速與能量傳遞特性。'),
        ('meter', f'用於量測「{zh}」相關物理量的儀器或感測設備。'),
        ('storm', f'指與「{zh}」相關的風暴、劇烈天氣系統或對流組織。'),
        ('rain', f'指與「{zh}」相關的降雨現象、雨量特徵或降水型態。'),
        ('snow', f'指與「{zh}」相關的降雪現象、雪況條件或積雪特徵。'),
        ('humidity', f'指與「{zh}」相關之空氣水汽含量、濕度狀態或其觀測診斷量。'),
        ('circulation', f'指與「{zh}」相關的環流系統，用於描述大氣或海洋中的平均運動與輸送結構。'),
        ('climate', f'指「{zh}」所對應的氣候類型、區域氣候條件或其長期平均特徵。'),
        ('diffusion', f'指與「{zh}」相關的分散、混合或擴散過程，可涉及物質、熱量或動量傳輸。'),
        ('flux', f'指單位時間穿過單位面積之「{zh}」通量，用於量化質量、能量或動量輸送。'),
        ('ratio', f'指表示「{zh}」相關兩種量值關係的比值，常用於診斷、比較或分類。'),
        ('time', f'指與「{zh}」相關的時間尺度、時制、時相或統計時間特徵。'),
        ('level', f'指與「{zh}」相關的特徵層位、標準層、診斷高度或強度分級。'),
        ('number', f'指用於表徵「{zh}」相關物理機制、無因次特徵或分類條件的數值指標。'),
        ('satellite', f'指與「{zh}」相關的衛星平台、衛星任務或其觀測資料。'),
        ('radar', f'指與「{zh}」相關的雷達系統、雷達觀測或遙測產品。'),
        ('breeze', f'指與「{zh}」相關的局地微風環流，通常由熱力差異或地形效應所驅動。'),
    ]
    for key, val in rules:
        key_norm = re.sub(r'[^a-z0-9]+', ' ', key.lower()).strip()
        if re.search(r'(^| )' + re.escape(key_norm) + r'( |$)', low_norm):
            return val
    if low_norm.endswith(' line') or low_norm == 'line':
        return f'指與「{zh}」相關的線性結構、譜線、基準線或分析界線，常作為診斷與辨識依據。'
    if low_norm.endswith(' point') or low_norm == 'point':
        return f'指與「{zh}」相關的特徵點、基準點或分析位置，用於描述幾何、光學或動力結構。'
    if low_norm.endswith(' flow') or low_norm == 'flow':
        return f'指與「{zh}」相關的流動型態、平均流場或輸送結構。'
    if low_norm.endswith(' rate') or low_norm == 'rate':
        return f'指「{zh}」相關量值之變化速率、生成速率、交換速率或傳輸速率。'
    return f'指與「{zh}」相關的氣象、海洋、水文、環境或地球科學專業術語；其具體涵義仍需依學科脈絡與使用情境判定。'


def polish_definition(text):
    text = re.sub(r'\s+', ' ', text).strip()
    text = text.replace(' ，', '，').replace(' 。', '。').replace(' ；', '；').replace(' ：', '：')
    text = text.replace('其具體涵義仍需依學科脈絡與使用情境判定。', '其具體涵義仍需依實際學科脈絡與使用情境判定。')
    text = text.replace('局地微風環流', '局地環流')
    if not text.endswith(('。', '；')):
        text += '。'
    return text


def build(letter):
    seen = set(); ordered = []
    for t in terms:
        if t[:1].lower() == letter:
            k = t.casefold()
            if k not in seen:
                seen.add(k)
                ordered.append(t)
    rows = []
    for idx, term in enumerate(ordered, 1):
        zh = manual_zh(term)
        definition = polish_definition(make_def(term, zh))
        rows.append({'english': term, 'traditional_chinese': zh, 'definition_cht': definition})
        if idx % 25 == 0:
            print(letter, idx, 'of', len(ordered), flush=True)
    return ordered, rows

for letter, out in [('l', OUT_L), ('m', OUT_M)]:
    ordered, rows = build(letter)
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'wrote {len(rows)} rows to {out}')
    print('first', ordered[0], rows[0]['traditional_chinese'])
    print('last', ordered[-1], rows[-1]['traditional_chinese'])

CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding='utf-8')
