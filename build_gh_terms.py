import json, re, time
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.parse import quote

SRC = Path('/home/node/.openclaw/workspace/met_term/source_doc_gh.json')
DATA = Path('/home/node/.openclaw/workspace/met_term/data')
CACHE = DATA / '_gh_translate_cache.json'
OUT_G = DATA / 'g_terms_all_cht.json'
OUT_H = DATA / 'h_terms_all_cht.json'

obj = json.loads(SRC.read_text())
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

cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}

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
                CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=2))
            time.sleep(0.08)
            return out
        except Exception as e:
            last_err = e
            time.sleep(1 + i)
    raise last_err

trans_override = {
    'G-region':'G層','G-scale':'G尺度','gaign':'蓋恩風','gain':'增益','Gale':'烈風','Gale warning':'烈風警報',
    'Galerkin approximation':'伽遼金近似','Galerkin methods':'伽遼金方法','galilean invariance':'伽利略不變性',
    'galle':'加勒風','gallows frame':'吊架框架','galvanic current':'原電流','galvanometer':'檢流計',
    'gamma ray':'伽瑪射線','gap wind':'峽口風','garden sprinkler effect':'灑水器效應','garland cloud':'花環雲',
    'gas constant':'氣體常數','gas thermometer':'氣體溫度計','gasohol':'酒精汽油','Gaussian distribution':'高斯分布',
    'Gaussian plume model':'高斯煙流模式','gegenschein':'對日照','geodesic':'測地線','geodetic latitude':'大地緯度',
    'geodetic leveling':'大地水準測量','geodynamics':'地球動力學','geographic coordinates':'地理座標',
    'geographic grid':'地理格網','geographic information system':'地理資訊系統','geographic latitude':'地理緯度',
    'geographic longitude':'地理經度','geographic north pole':'地理北極','geographic south pole':'地理南極',
    'geologic thermometer':'地質溫度計','geological hydrology':'地質水文學','geomagnetic field':'地磁場',
    'geomagnetic storm':'地磁暴','geomagnetic tail':'地磁尾','geometric altitude':'幾何高度','geometrical optics':'幾何光學',
    'geopotential':'位勢','geopotential altitude':'位勢高度','geopotential height':'位勢高度','geostationary':'地球同步的',
    'geostationary orbit':'地球同步軌道','geostrophic approximation':'地轉近似','geostrophic contour current':'地轉等值流',
    'geostrophic wind':'地轉風','geotaxis':'趨地性','geothermal gradient':'地熱梯度','geothermometer':'地溫計',
    'geotropism':'向地性','geotropic wind':'地轉風','geotropy':'向地性','germination':'萌發','gibbous phase':'盈凸相',
    'gigacycle':'十億週','gigahertz':'吉赫','GIM':'地磁指數圖','ginger line':'金傑線','GIS':'地理資訊系統',
    'glacial anticyclone':'冰川反氣旋','glacial epoch':'冰期','glacial period':'冰期','glaciated':'冰川覆蓋的',
    'glaciation':'冰化作用','glacier':'冰川','glacier wind':'冰川風','glaciology':'冰川學','glare ice':'光滑冰',
    'glass electrode':'玻璃電極','glass thermometer':'玻璃溫度計','global circulation':'全球環流',
    'global climate model':'全球氣候模式','global radiation':'全天空總輻射','global warming':'全球暖化',
    'globule':'小液滴','gloomy sky':'陰暗天空','glory':'輝光','GMT':'格林威治標準時間','gnomon':'日晷指針',
    'go-devil':'旋風小塵柱','goes':'GOES 衛星','gold leaf electroscope':'金箔驗電器','golden number':'黃金數',
    'goniometer':'測角器','Gorda Current':'戈爾達海流','gorge wind':'峽谷風','gradient':'梯度','gradient current':'梯度流',
    'gradient flux':'梯度通量','gradient Richardson number':'梯度理查森數','gradient wind':'梯度風','graupel':'霰',
    'gravity':'重力','gravity anomaly':'重力異常','gravity current':'重力流','gravity meter':'重力儀','gravity wave':'重力波',
    'Great Salt Lake':'大鹽湖','green flash':'綠閃光','greenhouse effect':'溫室效應','greenwich time':'格林威治時間',
    'gregale':'格雷加勒風','grey atmosphere':'灰體大氣','greybody':'灰體','gribble':'舟蛆','grid analysis':'格點分析',
    'grid point':'格點','grid-point value':'格點值','grin':'格林效應','ground clutter':'地物雜波','ground fog':'地面霧',
    'ground return':'地面回波','ground speed':'對地速度','ground water':'地下水','groundwave':'地波','growing degree day':'生長度日',
    'growing season':'生長季','growth rate':'成長率','GTD':'地面真實資料','gulf stream':'灣流','gust':'陣風',
    'gust front':'陣風鋒','gustnado':'陣風龍捲','gutta':'滴流','guttation':'吐水作用','guttra':'滴狀雲','guxen':'焚風型突風',
    'Guyana Current':'蓋亞那海流','guzzle':'急流槽口','GVAR':'地球同步可見紅外分析系統','gyres':'環流','gyro-frequency':'迴旋頻率',
    'haar':'海霧冷濕風','Haboob':'哈布沙暴','Hadley cell':'哈德里環流','Hadley regime':'哈德里環流型態',
    'hail':'冰雹','hail stage':'雹成長期','hailpad':'雹墊','Hailstone':'雹粒','half life':'半衰期','half power point':'半功率點',
    'halo':'暈','halocline':'鹽躍層','halosteric':'鹽致密度的','halothermal':'鹽熱的','harmattan':'哈麥丹風',
    'harmonic':'諧波','harmonic analysis':'諧波分析','harmonic mean':'調和平均','harmonic tide analysis':'潮汐諧和分析',
    'haze':'霾','haze horizon':'霾際線','haze layer':'霾層','hazy':'霾的','head':'水頭','head current':'前端流',
    'head sea':'迎浪','head wind':'逆風','heat':'熱','heat balance':'熱平衡','heat budget':'熱收支','heat capacity':'熱容',
    'heat dome':'熱穹','heat engine':'熱機','heat equator':'熱赤道','heat exhaustion':'熱衰竭','heat index':'酷熱指數',
    'heat island':'熱島','heat lightning':'熱閃電','heat low':'熱低壓','heat stroke':'中暑','heat transfer':'熱傳','heat wave':'熱浪',
    'heated thermocouple':'加熱熱電偶','heating degree day':'暖房度日','heavy rain':'大雨','heavy shower':'強陣雨','heavy snow':'大雪',
    'heavy swell':'大湧浪','height':'高度','height anomaly':'高度距平','height contour':'高度等值線','height tendency':'高度趨勢',
    'heliograph':'日照計','helium':'氦','Helmholtz wave':'亥姆霍茲波','hemispheric index':'半球指數','hertz':'赫茲',
    'heterosphere':'異質層','high':'高壓','high center':'高壓中心','high cloud':'高雲','high clouds':'高雲','high energy particle':'高能粒子',
    'high fog':'高位霧','high frequency':'高頻','high inversion':'高空逆溫','highland climate':'高地氣候','high-level':'高層的',
    'high-level clouds':'高層雲','high-level humidity':'高層濕度','high-level inversion':'高層逆溫','high-level jet stream':'高層噴流',
    'high-level turbulence':'高空亂流','high-pass filter':'高通濾波器','high-pressure area':'高壓區','high-pressure system':'高壓系統',
    'high-speed photography':'高速攝影','high-order closure':'高階封閉法','high-water mark':'高水位痕','histogram':'直方圖',
    'historical geology':'歷史地質學','hoar':'白霜','hoar frost':'霜','hodograph':'風矢端跡圖','hoist':'升降裝置','holding tank':'儲存槽',
    'hole-punch cloud':'穿孔雲','holometeoric':'全天氣的','homopause':'同溫層頂混合界面','homosphere':'均質層','hook echo':'鉤狀回波',
    'horizontal visibility':'水平能見度','horizontal wind shear':'水平風切','horse latitudes':'副熱帶無風帶','hot spot':'熱點',
    'hot-wire anemometer':'熱線風速計','hour angle':'時角','hourly rainfall':'時雨量','hovmoller diagram':'霍夫莫勒圖',
    'HSS':'高速掃描系統','humidity':'濕度','humidity element':'濕度感應元件','humidity sounding':'濕度探空','humidometer':'濕度計',
    'humilis':'淡積雲','hummock':'冰丘','hurricane':'颶風','hurricane eye':'颶風眼','hurricane hunter':'颶風偵察機',
    'hurricane season':'颶風季','hurricane warning':'颶風警報','hygrograph':'濕度記錄器','hygrometer':'濕度計',
    'hygroscopic nucleus':'吸濕凝結核','hygrothermograph':'溫濕度自記器','hylometer':'測林儀','hybrid coordinate':'混合座標',
    'hydraulic gradient':'水力坡降','hydraulic jump':'水躍','hydraulic mean depth':'水力平均深度','hydraulic radius':'水力半徑',
    'hydraulic roughness':'水力粗糙度','hydraulics':'水力學','hydro-meteorology':'水文氣象學','hydrocarbon':'碳氫化合物',
    'hydroclimatology':'水文氣候學','hydrodynamics':'流體動力學','hydroelectric power':'水力發電','hydrogen':'氫',
    'hydrograph':'水文歷線','hydrograph recession':'歷線退水段','hydrograph separation':'歷線分離','hydrographic survey':'水文測量',
    'hydrologic cycle':'水文循環','hydrological budget':'水文收支','hydrology':'水文學','hydrometeor':'水象',
    'hydrometeor classification':'水象分類','hydrometeorology':'氣象水文學','hydrophone':'水聽器','hydrophyte':'水生植物',
    'hydrostatic approximation':'流體靜力近似','hydrostatic balance':'流體靜力平衡','hydrostatic equation':'流體靜力方程',
    'hydrostatic pressure':'靜水壓','hydrotherapy':'水療法','hydrothermal':'熱水的','hygrometry':'濕度測定','hyperbolic wave':'雙曲波',
    'hyperthermia':'高熱症','hyperspectral':'高光譜的','hypolimnion':'深水層','hypothermia':'低體溫症','hypsithermal period':'溫暖期',
    'hypsography':'地勢測量','hypsometer':'測高儀','Hypsometric equation':'測高方程','hypsometry':'地勢學','hythergraph':'溫濕圖'
}

manual_def = {
    'Gale warning':'預報或觀測顯示平均風力將達烈風等級時所發布的海上或沿海警報，用以提醒航行與作業防範強風危害。',
    'Galerkin approximation':'求解偏微分方程與數值模式時常用的近似方法，藉由將解表示於有限基底空間中，以獲得可計算的離散方程組。',
    'Galerkin methods':'一類以試函數與權函數同屬同一函數空間為特徵的加權殘值法，廣泛用於有限元素法與流體數值模擬。',
    'gas constant':'描述氣體狀態方程中壓力、體積與溫度關係的常數；在氣象上常區分通用氣體常數與乾空氣、濕空氣之比氣體常數。',
    'Gaussian distribution':'以平均值與變異數刻畫之連續機率分布，常用於描述觀測誤差、亂流統計與多種自然變量的近似分布。',
    'Gaussian plume model':'描述污染物在平均風場與湍流擴散作用下於下風處濃度分布的經典模式，常用於空氣污染擴散評估。',
    'gegenschein':'位於反太陽點附近、由行星際塵埃反射與後向散射日光所形成的微弱亮區，常見於晴朗暗夜天空。',
    'geodesic':'曲面上兩點之間局部最短路徑，在地球科學中常用於大地測量、球面導航與網格離散幾何。',
    'geographic information system':'整合空間資料之擷取、管理、分析與視覺化的資訊系統，廣泛應用於天氣、氣候、水文與災害分析。',
    'geomagnetic storm':'太陽風或日冕物質拋射擾動地磁場而引起的劇烈變化現象，可能影響高層大氣、通訊、導航與電力系統。',
    'geopotential':'單位質量空氣自海平面或參考面移至某高度時所具有的位能，常用於描述大氣壓力面之高度與動力結構。',
    'geopotential height':'將位勢除以標準重力加速度所得之高度量，為高空天氣圖與大尺度環流分析中的基本變數。',
    'geostationary orbit':'衛星位於赤道上空、繞地公轉週期與地球自轉相同的圓形軌道，使其相對地表近似固定於同一經度。',
    'geostrophic wind':'在科氏力與氣壓梯度力達近似平衡時所形成、平行等壓線吹送的理想風，是中高緯大尺度流場分析的重要近似。',
    'glaciation':'可指雲中過冷水滴轉變為冰晶之冰化過程，亦可泛指地表受冰川作用影響之冰川化現象；實際意義依語境而定。',
    'glacier wind':'受冰川表面強冷卻影響，冷密空氣沿坡面向下流動而形成的局地下坡風。',
    'global circulation':'地球大氣在受太陽輻射差異、自轉與下墊面作用下形成之行星尺度平均環流系統，包括哈德里環流、西風帶與極地環流等。',
    'global climate model':'以數值方程模擬大氣、海洋、陸面與冰雪系統交互作用之全球尺度氣候模式，用於氣候變遷研究與情境推估。',
    'global warming':'由溫室氣體增加等因素導致地球近地表與海洋平均溫度長期上升的現象。',
    'glory':'觀測者背向太陽時，於雲滴或霧滴所形成的反太陽點周圍彩色同心光環現象，與後向散射及繞射有關。',
    'gradient Richardson number':'以浮力穩定效應與垂直風切強度之比值衡量層結穩定度與亂流生成傾向的無因次參數。',
    'gradient wind':'在曲線流動中，氣壓梯度力、科氏力與離心力達平衡時的理想風速關係，常用於分析彎曲等壓線附近的環流。',
    'graupel':'由過冷水滴凍附於雪晶或冰晶表面所形成的白色不透明粒狀固態降水，粒徑通常小於冰雹。',
    'gravity current':'因密度差異而在重力驅動下沿地表或界面水平推進的流體，如冷池外流、海風前緣或鹽水入侵。',
    'gravity wave':'流體中受重力或浮力作為回復力所形成的波動，可見於大氣穩定層結、山脈背風波與海洋內波。',
    'green flash':'日出或日落瞬間因大氣折射與色散作用，使太陽上緣短暫出現綠色閃現的光學現象。',
    'greenhouse effect':'大氣吸收並再放射地表長波輻射，從而抑制熱量直接逸散至太空並提升近地面溫度的效應。',
    'grid analysis':'將離散觀測資料經插值、客觀分析或同化方法轉換為規則格點場的分析程序。',
    'ground clutter':'雷達接收到自地形、建築物或其他固定地物反射而非來自降水目標的回波雜訊。',
    'ground fog':'主要侷限於近地表淺薄層中的霧，多由夜間地表冷卻使接地空氣達飽和而形成。',
    'ground water':'賦存於土壤孔隙、裂隙或含水層中的地下水體，是水文循環與水資源系統的重要組成。',
    'gulf stream':'北大西洋西部自墨西哥灣沿美國東岸向東北流動的強暖流，對區域與行星尺度氣候具有重要調節作用。',
    'gust':'在短時間內風速顯著增強的瞬時強風，通常用以描述相對於平均風之快速脈動。',
    'gust front':'雷暴下沉冷空氣向外擴散時所形成的近地面密度鋒，可觸發新對流並伴隨風向、風速與溫度突變。',
    'gustnado':'沿陣風鋒或下擊暴流邊界生成之淺層短生命旋轉渦柱，雖外觀近似龍捲，但成因與母體環流不同。',
    'GVAR':'地球同步氣象衛星之可見光與紅外資料傳輸系統，用於即時下傳衛星影像與相關產品。',
    'gyres':'在風應力、科氏力與海盆邊界共同作用下形成的大尺度環狀海洋環流系統，可分為副熱帶與副極地環流。',
    'haar':'蘇格蘭與北海沿岸常見的冷濕海霧或霧狀低雲伴隨之海風型天氣，常由暖濕空氣流經較冷海面所致。',
    'Haboob':'乾旱或半乾旱地區由雷暴下擊暴流推動的大規模沙塵牆，常伴隨突發強風與能見度驟降。',
    'Hadley cell':'熱帶地區由赤道上升、上層向副熱帶輸送、下沉並於近地面回流至赤道所構成的經向環流。',
    'hail':'在強對流雲中，過冷水滴反覆凍結增長而成、直徑通常大於霰的固態降水粒子。',
    'halocline':'海洋或湖泊中鹽度隨深度快速變化的層次，常影響密度分層、混合與聲學傳播。',
    'harmonic analysis':'將週期性或準週期性訊號分解為不同頻率正弦與餘弦分量的分析方法，廣用於潮汐、氣候振盪與時間序列研究。',
    'haze':'由大量微小乾粒子懸浮於空氣中所造成的能見度降低現象，與霧不同，其相對濕度通常較低且不致使空氣達飽和。',
    'heat budget':'對某一系統內熱量輸入、輸出、儲存與轉換項進行定量平衡分析的收支關係。',
    'heat dome':'由持續性高壓脊與下沉增溫共同造成之大範圍暖熱堆積型天氣形勢，常導致長時間極端高溫。',
    'heat index':'綜合氣溫與相對濕度以表徵人體實際悶熱感受之指標。',
    'heat island':'都市區因人工鋪面、建築結構與人為排熱等因素，使氣溫高於周邊郊區的現象。',
    'heat lightning':'遠處雷暴所產生、觀測地僅見閃光而聽不到雷聲的閃電現象，通常因距離過遠導致雷聲衰減。',
    'heat low':'地表強烈加熱造成近地層空氣膨脹上升而形成的淺薄低壓系統，常見於乾旱或大陸內陸地區。',
    'heat transfer':'熱量藉由傳導、對流或輻射在不同介質或系統間傳遞的過程。',
    'heat wave':'在一定區域與季節條件下，連續數日出現顯著高於常態之高溫事件。',
    'Helmholtz wave':'由兩層流體速度差與密度分層共同作用所產生的界面波動，常與凱爾文－亥姆霍茲不穩定發展有關。',
    'heterosphere':'高層大氣中各氣體成分因分子擴散而依分子量分層分布的區域，位於均質層之上。',
    'high-pass filter':'允許高於某截止頻率之訊號通過、抑制較低頻成分的濾波器，用於資料處理與頻譜分析。',
    'hoar frost':'水汽在低於冰點的表面直接凝華形成的白色針狀、羽毛狀或粒狀冰晶沉積。',
    'hodograph':'將風矢量端點依高度或時間連續描繪而成的曲線圖，可用於分析風切、對流環境與暴風旋轉潛勢。',
    'hole-punch cloud':'當飛機穿越含過冷水滴之中高層雲時誘發冰晶快速成長，造成雲中局部空洞或條帶的現象。',
    'hook echo':'都卜勒或反射率雷達上位於超級胞後側、呈鉤狀彎曲的回波特徵，常與中氣旋及龍捲生成潛勢相關。',
    'horizontal wind shear':'風速或風向在水平方向上隨距離改變的現象，對中尺度環流、對流組織與航空安全皆具重要影響。',
    'horse latitudes':'副熱帶高壓帶附近盛行沉降、風弱少雨的緯度帶，大致位於南北緯 30 度附近。',
    'hovmoller diagram':'以時間與空間其中一維為座標、顯示某變數沿另一維變化的圖式，常用於分析波動傳播與季內振盪。',
    'humidity':'空氣中水汽含量的統稱，可用相對濕度、比濕、混合比、露點等不同物理量表示。',
    'hurricane':'北大西洋或東北太平洋生成之熱帶氣旋，當其最大持續風速達規定門檻以上時稱為颶風。',
    'hygrometer':'量測空氣濕度或相關水汽參數的儀器。',
    'hygroscopic nucleus':'能吸附水汽並促使水滴在未達純水飽和條件下成長的微粒，是雲滴形成的重要凝結核類型。',
    'hydraulic jump':'明渠急流在短距離內突然轉為緩流、伴隨水深躍增與能量耗散的現象。',
    'hydroclimatology':'研究氣候條件與水文循環要素之交互作用及其時空變異的學科。',
    'hydrodynamics':'研究流體在力作用下運動規律及其動量、能量傳輸特性的學科。',
    'hydrograph':'表示河川流量、水位或其他水文量隨時間變化的曲線，是流域響應分析的重要工具。',
    'hydrologic cycle':'地球系統中水分在蒸發、凝結、降水、入滲、逕流、地下流與蒸散等過程間持續循環的整體機制。',
    'hydrometeor':'由大氣中水或冰所組成並可被觀測之粒子集合體，包括雲滴、雨滴、雪、霰、冰雹等。',
    'hydrometeorology':'結合氣象與水文，研究降水、蒸發、土壤水分、逕流與洪旱等過程及其相互作用的學科。',
    'hydrostatic approximation':'在垂直尺度遠小於水平尺度的大尺度流動中，假設垂直加速度可忽略，使垂直壓力梯度力與重力近似平衡的近似。',
    'hydrostatic balance':'大氣或海洋中垂直方向上，向上的壓力梯度力與向下的重力近似互相平衡的基本力學關係。',
    'hydrostatic equation':'表述流體靜力平衡下壓力隨高度變化率與流體密度、重力間關係的方程式。',
    'hyperspectral':'具有大量且窄波段連續光譜資訊的特性，可用於精細辨識地物、雲系、氣膠與大氣成分。',
    'hypolimnion':'湖泊分層期間位於溫躍層之下、通常較冷且與表層交換受限的深水層。',
    'Hypsometric equation':'描述兩壓力面之厚度與該層虛溫平均值關係的基本方程，廣泛用於高空分析與層厚計算。',
    'hythergraph':'以圖形同時呈現溫度與濕度關係或其時間變化特徵的圖表，用於氣候比較與舒適度分析。'
}

def manual_zh(term):
    return trans_override.get(term) or gtranslate(term)

def make_def(term, zh):
    if term in manual_def:
        return manual_def[term]
    low = term.lower()
    if re.fullmatch(r'[A-Z0-9\-–/]+', term):
        return f'「{term}」為氣象、海洋、水文、遙測或相關領域使用之縮寫、代號或產品名稱；其精確涵義需依專業語境判定。'
    rules = [
        ('wind', f'指與「{zh}」相關的風場型態、局地風系或風向風速特徵，用於描述其成因、結構與影響。'),
        ('current', f'指與「{zh}」相關的海流、氣流或密度流系統，著重其流向、形成機制及輸送作用。'),
        ('front', f'指與「{zh}」相關的鋒面或密度邊界結構，常伴隨風、溫度與濕度的明顯變化。'),
        ('layer', f'指與「{zh}」相關的大氣、海洋或湖泊層結構，通常依熱力、密度、鹽度或動力特徵加以區分。'),
        ('cloud', f'指與「{zh}」相關的雲系、雲形或雲微物理特徵，用於描述其外觀、形成機制與所對應的大氣狀態。'),
        ('ice', f'指與「{zh}」相關的冰相現象、冰體型態或凍結狀態，常用於寒區氣象、海冰或冰川研究。'),
        ('equation', f'描述「{zh}」相關物理量之間關係、守恆條件或診斷計算方法的方程式。'),
        ('model', f'用於表徵「{zh}」相關過程或系統的理論、概念或數值模式，以分析其主要物理機制。'),
        ('chart', f'用於呈現「{zh}」相關分析結果、場型分布或統計資訊的圖表。'),
        ('graph', f'以圖形方式呈現「{zh}」相關量值變化、對應關係或分類結果的圖表。'),
        ('coefficient', f'表示「{zh}」相關強度、效率、交換能力或比例關係的係數，常作為方程式或參數化中的重要參數。'),
        ('function', f'描述「{zh}」相關變數關係、響應特性或分布型態的函數表述。'),
        ('index', f'用於量化「{zh}」相關狀態、程度、異常幅度或風險的指標。'),
        ('spectrum', f'指與「{zh}」相關的頻譜、能譜或波譜分布，用於分析不同尺度上的能量配置。'),
        ('radiation', f'指與「{zh}」相關的輻射收支、能量傳輸或電磁傳播效應。'),
        ('pressure', f'指與「{zh}」相關的壓力概念、壓力分布或其衍生診斷量。'),
        ('forecast', f'指以「{zh}」為核心的預報方法、預測產品或其結果。'),
        ('station', f'指與「{zh}」相關的觀測站、測站設施或資料蒐集位置。'),
        ('observation', f'指與「{zh}」相關的觀測作業、量測資料或診斷結果。'),
        ('theorem', f'「{zh}」相關的理論定理或數學命題，用於說明特定物理或統計性質。'),
        ('law', f'「{zh}」相關的定律或經驗法則，用以概括物理關係、尺度關係或統計規律。'),
        ('method', f'指處理「{zh}」相關問題的分析、估算、分類、反演或推算方法。'),
        ('instability', f'指與「{zh}」相關的不穩定機制，可導致擾動增幅、波動發展或對流觸發。'),
        ('approximation', f'用於處理「{zh}」相關問題的近似假設，以保留主要物理機制並簡化數學描述。'),
        ('velocity', f'指與「{zh}」相關的速度量，用於描述流體、粒子或波動之運動快慢與方向。'),
        ('temperature', f'指與「{zh}」相關的溫度量、溫度分布或代表性熱狀態特徵。'),
        ('water', f'指與「{zh}」相關的水體、水團、水量條件或水文狀態，常用於海洋與水文分析。'),
        ('lightning', f'指與「{zh}」相關的放電或閃電現象，用於辨識雷暴電活動及其結構特徵。'),
        ('filter', f'用於擷取、保留或抑制「{zh}」相關頻率成分、訊號變化或尺度資訊的濾波方法或裝置。'),
        ('height', f'指與「{zh}」相關的高度量測、垂直尺度或特徵層位。'),
        ('wave', f'指與「{zh}」相關的波動、波形或擾動結構，用於描述其傳播、振盪與能量傳遞特性。'),
        ('meter', f'用於量測「{zh}」相關物理量的儀器、計量設備或感測裝置。'),
        ('frequency', f'指與「{zh}」相關的頻率特性、振盪速率或波動尺度指標。'),
        ('storm', f'指與「{zh}」相關的風暴、擾動系統或劇烈天氣現象。'),
        ('rain', f'指與「{zh}」相關的降雨現象、雨量特徵或降水統計量。'),
        ('snow', f'指與「{zh}」相關的降雪現象、雪況條件或雪量特徵。'),
        ('humidity', f'指與「{zh}」相關之空氣水汽含量、濕度狀態或其觀測診斷量。'),
        ('hydro', f'指與「{zh}」相關的水文、水力、流體或水圈過程與性質。'),
        ('distribution', f'指「{zh}」所代表的分布型態或機率分布，用於描述變量在空間、時間或數值上的配置特徵。'),
        ('transfer', f'指與「{zh}」相關的傳輸、交換或移轉過程，常涉及熱量、氣體、動量或物質通量。'),
        ('kinetics', f'指「{zh}」所涉及的反應動力學、轉化速率或化學過程特徵。'),
        ('reaction', f'指與「{zh}」相關的化學或物理反應過程，用於說明物質轉換與能量變化。'),
        ('shear', f'指與「{zh}」相關的風切、速度梯度或形變特徵，常用於診斷對流與流場結構。'),
        ('relation', f'指「{zh}」所表達之變量對應、換算或經驗關係。'),
        ('section', f'指與「{zh}」相關的斷面、河段或分析區段，用於量測、監測或計算。'),
        ('site', f'指與「{zh}」相關的站址、測點或作業地點。'),
        ('curve', f'指表示「{zh}」相關變化關係、分布形態或統計特徵的曲線。'),
        ('grid', f'指與「{zh}」相關的格網系統、網格配置或離散化架構。'),
        ('circulation', f'指與「{zh}」相關的環流系統，描述大氣或海洋中流體之平均運動與輸送結構。'),
        ('coordinates', f'指表示「{zh}」相關位置、方向或空間基準的座標系統。'),
        ('geodesy', f'研究地球形狀、重力場、參考系與精密定位測量的學科。'),
        ('optics', f'指與「{zh}」相關的光學理論、光路特性或輻射傳播現象。'),
        ('mean', f'指「{zh}」所代表之平均量、統計均值或代表性平均狀態。'),
        ('effect', f'指與「{zh}」相關的物理、化學或觀測效應，用於描述特定機制造成的結果。'),
        ('satellite', f'指與「{zh}」相關的人造衛星、衛星任務或其觀測平台。'),
        ('ray', f'指與「{zh}」相關的射線、輻射束或粒子束。'),
        ('time', f'指與「{zh}」相關的時間尺度、時制或地質年代概念。'),
        ('epoch', f'指與「{zh}」相關的年代分期、時段或地質時代單位。'),
        ('era', f'指與「{zh}」相關的較長時間分期、地質代或歷史階段。'),
        ('age', f'指與「{zh}」相關的年代、地質期或發展階段。'),
        ('burst', f'指與「{zh}」相關的突發現象、短時強化事件或脈衝式變化。'),
        ('capacity', f'指「{zh}」所代表的容納能力、儲存能力或熱容量等性質。'),
        ('conductivity', f'指與「{zh}」相關的傳導能力、導電率或輸送能力。'),
        ('flux', f'指單位時間穿過單位面積之「{zh}」通量，用以量化能量、質量或動量傳輸。'),
        ('unit', f'指量測或表示「{zh}」時所使用的單位、尺度或計量基準。'),
        ('scanning', f'指與「{zh}」相關的掃描方式、掃描幾何或觀測程序。'),
        ('helicity', f'描述流場旋轉與流向排列程度的物理量，常用於對流風暴環境與渦度分析。'),
    ]
    for key, val in rules:
        if key in low:
            return val
    if low.endswith('point'):
        return f'指與「{zh}」相關的特徵點、基準點或分析辨識位置，用於描述幾何、光學或動力結構。'
    if low.endswith('line'):
        return f'指與「{zh}」相關的線性界面、基準線或分析線，常作為場型判讀與結構定位的輔助。'
    if low.endswith('rate'):
        return f'指「{zh}」的變化速率、交換速率、生成速率或傳輸速率，用於量化過程快慢。'
    if low.endswith('flow'):
        return f'指與「{zh}」相關的流動型態、平均流場或輸送結構。'
    if low.endswith('ratio'):
        return f'指表示「{zh}」相關兩種量值之間關係的比值，常用於診斷、比較或分類。'
    if low.endswith('period'):
        return f'指與「{zh}」相關、以特定時間尺度界定的氣候期、週期或統計時段。'
    if low.endswith('climate'):
        return f'指「{zh}」所代表之區域或類型氣候特徵，通常由溫度、降水與地形條件共同界定。'
    if low.endswith('regime'):
        return f'指與「{zh}」相關的主導流況、環流型態或統計狀態。'
    if low.endswith('stage'):
        return f'指與「{zh}」相關的發展階段、演變時期或作業階段。'
    return f'指與「{zh}」相關的氣象、海洋、水文、環境或地球科學專業術語；其具體涵義仍需依學科脈絡與使用情境判定。'


def polish_definition(text):
    text = re.sub(r'\s+', ' ', text).strip()
    text = text.replace(' ，', '，').replace(' 。', '。').replace(' ；', '；').replace(' ：', '：')
    text = text.replace('，並', '，並').replace('，可', '，可').replace('，常', '，常')
    if not text.endswith(('。', '；')):
        text += '。'
    text = text.replace('氣象、海洋、水文、遙測或相關領域', '氣象、海洋、水文、遙測或相關地球科學領域')
    text = text.replace('其精確涵義需依專業語境判定', '其精確涵義仍需依專業語境判定')
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
        rows.append({
            'english': term,
            'traditional_chinese': zh,
            'definition_cht': definition,
        })
        if idx % 25 == 0:
            print(letter, idx, 'of', len(ordered), flush=True)
    return ordered, rows

for letter, out in [('g', OUT_G), ('h', OUT_H)]:
    ordered, rows = build(letter)
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=2))
    print(f'wrote {len(rows)} rows to {out}')
    print('first', ordered[0], rows[0]['traditional_chinese'])
    print('last', ordered[-1], rows[-1]['traditional_chinese'])

CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=2))
