import json
from pathlib import Path

updates = {
    'range–height indicator': {
        'traditional_chinese': '距離－高度指示器',
        'definition_cht': '雷達顯示方式之一，將天線固定於某一方位角並作仰角掃描，以水平軸表示距離、垂直軸表示高度，用來呈現該方位上的垂直剖面回波；常縮寫為 RHI。'
    },
    'Rankine temperature scale': {
        'traditional_chinese': '朗肯溫標',
        'definition_cht': '一種絕對熱力學溫標，其零點為絕對零度，且每一度的大小與華氏一度相同；因此常用於英制工程熱力學，性質上相當於以華氏刻度表示的絕對溫標。'
    },
    'Rankine vortex': {
        'traditional_chinese': '朗肯渦旋',
        'definition_cht': '理想化渦旋模型，假設渦心內部為固體體旋轉、切向風速隨半徑成正比，渦心外部則近似無旋流、切向風速隨半徑反比遞減；常用於描述龍捲風、塵捲風或其他旋轉流場。'
    },
    'RAOB': {
        'traditional_chinese': '高空探空觀測',
        'definition_cht': 'radiosonde observation 的縮寫，指以無線電探空儀隨氣球升空所取得的高空觀測資料，通常包括氣壓、氣溫、濕度、風向與風速等垂直剖面資訊。'
    },
    "Raoult's law": {
        'traditional_chinese': '拉午耳定律',
        'definition_cht': '物理化學中描述理想液體混合物蒸氣壓的定律：各成分的分壓等於其純物質蒸氣壓乘以該成分在液相中的莫耳分率；在氣象上常用於理解溶液滴的平衡蒸氣壓與雲滴微物理。'
    },
    'rapid distortion theory': {
        'traditional_chinese': '快速畸變理論',
        'definition_cht': '亂流理論之一，討論亂流在強而快速變動的平均流應變或剪切作用下，於短時間內被拉伸、轉向與重分配的響應；其近似常忽略此短時段內的非線性亂流交互作用。'
    },
    'rapid interval imaging': {
        'traditional_chinese': '快速間隔成像',
        'definition_cht': '指以較一般作業更短的時間間隔反覆取得影像的觀測模式，用於追蹤對流、颱風眼牆或其他快速演變天氣系統的細部變化；常見於氣象衛星快速更新觀測。'
    },
    'rapid interval scan': {
        'traditional_chinese': '快速間隔掃描',
        'definition_cht': '指以縮短重訪週期的方式重複執行掃描的觀測策略，使儀器能在較短時間內再次量測同一區域；常用於氣象衛星或雷達對劇烈天氣的密集監測。'
    },
    'rare gases': {
        'traditional_chinese': '稀有氣體',
        'definition_cht': '傳統上指化學性質極不活潑的元素氣體，即今常稱的惰性氣體或 noble gases，包括氦、氖、氬、氪、氙與氡等。'
    },
    'rare optical phenomenon': {
        'traditional_chinese': '罕見大氣光象',
        'definition_cht': '指在特殊日照幾何、冰晶取向、雲滴分布或大氣折射條件下才偶爾出現的大氣光學現象，例如較少見的暈象、弧光或其他短暫光學結構。'
    },
    'RAREP': {
        'traditional_chinese': 'RAREP',
        'definition_cht': '氣象文獻中的縮寫條目之一；本批次可取得的公開對照來源不足以可靠確認其固定全稱，故保留原縮寫，實際意義應依原始報文體系、碼表或使用語境判定。'
    },
    'RASAPH': {
        'traditional_chinese': 'RASAPH',
        'definition_cht': '氣象文獻中的縮寫條目之一；目前可交叉取得的公開資料不足以穩定確認其標準展開，故保留原縮寫，實際意義應以原始來源、代碼表或專業語境為準。'
    },
    'RASS': {
        'traditional_chinese': '無線電聲探測系統',
        'definition_cht': 'radio acoustic sounding system 的縮寫，利用聲波波前造成的空氣密度擾動反射電磁波，以量測不同高度的音速，進而推估邊界層中的虛溫或氣溫垂直分布。'
    },
    'rate coefficient': {
        'traditional_chinese': '反應速率係數',
        'definition_cht': '在化學動力學中，指速率方程式中的比例係數，用以連結反應速率與各反應物濃度；其數值通常受溫度、壓力與反應機制影響。'
    },
    'rate constants': {
        'traditional_chinese': '速率常數',
        'definition_cht': '化學動力學中各反應步驟所對應的常數，出現在速率定律中以描述反應進行快慢；對特定反應機制而言，其值常隨溫度改變，並可用阿瑞尼士關係表示。'
    },
    'rate of accretion': {
        'traditional_chinese': '增積率',
        'definition_cht': '指物質因碰撞、附著、凝結、凍附或沉積而累積增長的速率；在氣象上可指雲滴、冰或霜於物體表面或粒子上的增積快慢。'
    },
    'rate-of-climb indicator': {
        'traditional_chinese': '升降率指示器',
        'definition_cht': '航空儀表之一，用於指示飛機爬升或下降的垂直速度；亦稱垂直速度指示器（VSI），通常依靜壓變化推算上升或下降率。'
    },
    'rating curve': {
        'traditional_chinese': '率定曲線',
        'definition_cht': '在水文學中，指某測站水位（stage）與流量（discharge）之間的經驗關係曲線，用以依觀測水位推估河川或渠道流量。'
    },
    'rating flume': {
        'traditional_chinese': '率定量水槽',
        'definition_cht': '為量測或率定渠道流量而設計的標準化量水槽；藉由已知幾何形狀與水位－流量關係，可由水位觀測推算通過流量。'
    },
    'rational method': {
        'traditional_chinese': '理性法',
        'definition_cht': '小流域設計洪峰估算的經典水文方法，假設當降雨延時等於集流時間時可形成最大逕流，並以 C i A 的關係式估算尖峰流量，其中 C 為逕流係數、i 為降雨強度、A 為流域面積。'
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
