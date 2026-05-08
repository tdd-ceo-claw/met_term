import json
from pathlib import Path

updates = {
    'hair hygrometer': {
        'traditional_chinese': '毛髮濕度計',
        'definition_cht': '利用人髮或其他脫脂毛髮會隨相對濕度改變而伸縮的特性，將其長度或張力變化轉換為濕度讀值的濕度計。'
    },
    'halcyon days': {
        'traditional_chinese': '太平日',
        'definition_cht': '原指冬至前後一段風浪平靜、天氣安穩的時期；在氣象語境中常借指連續的平靜晴和天氣。'
    },
    'half-arc angle': {
        'traditional_chinese': '半弧角',
        'definition_cht': '大氣光學中用於描述暈弧幾何位置的角度量，通常指弧形光象相對其中心或光源方向所對應的半角。'
    },
    'half-life': {
        'traditional_chinese': '半衰期',
        'definition_cht': '某物理量、化學物質或放射性核種經過一定時間後衰減至原值一半所需的時間；在大氣化學中亦常用來表示污染物或示蹤物的有效移除時間尺度。'
    },
    'half-order closure': {
        'traditional_chinese': '半階閉合',
        'definition_cht': '亂流參數化中的閉合理論，僅對部分低階統計量作預報，並以經驗公式表示較高階項；在邊界層模式中常指介於一階閉合與二階閉合之間的閉合方式。'
    },
    'half-power points': {
        'traditional_chinese': '半功率點',
        'definition_cht': '頻率響應曲線上功率降為峰值一半的位置，對應振幅約為最大值的 1/√2，常用來界定濾波器、共振峰或雷達波束的 3 dB 頻寬。'
    },
    'Hall effect': {
        'traditional_chinese': '霍爾效應',
        'definition_cht': '導體或半導體通有電流並置於垂直磁場中時，會在橫向產生電位差的現象；常用於磁場量測與霍爾感測器。'
    },
    'Hallett-mossop process': {
        'traditional_chinese': '哈利特－莫索普過程',
        'definition_cht': '雲中霰化增長時產生次生冰晶的機制之一；當過冷水滴在冰粒表面凍結並濺裂時，可釋放大量細小冰晶，進而增加雲中的冰相粒子數。'
    },
    'Halmahera Eddy': {
        'traditional_chinese': '哈馬黑拉渦流',
        'definition_cht': '位於印尼哈馬黑拉島附近海域的中尺度海洋渦旋系統，會調制北赤道逆流與印尼貫穿流周邊的水團輸送、熱鹽分布與區域海氣作用。'
    },
    'halny wiatr': {
        'traditional_chinese': '哈爾尼風',
        'definition_cht': '出現在波蘭南部與喀爾巴阡山塔特拉山區的焚風型強風，越山下沉時增溫增乾，常伴隨陣風增強與山區災害。'
    },
    'halo': {
        'traditional_chinese': '暈',
        'definition_cht': '日光或月光經高空冰晶折射、反射後，在光源周圍形成的環狀或弧狀大氣光學現象。'
    },
    'halo of 22°': {
        'traditional_chinese': '22°暈',
        'definition_cht': '最常見的暈象之一，為環繞太陽或月亮、視半徑約 22 度的光環，主要由六角形冰晶對光線折射所形成。'
    },
    'halo of 46°': {
        'traditional_chinese': '46°暈',
        'definition_cht': '視半徑約 46 度、較 22°暈少見且通常較暗淡的暈象，主要由六角冰晶中不同入射與出射面組合的折射所產生。'
    },
    'halocarbons': {
        'traditional_chinese': '鹵代烴',
        'definition_cht': '分子中含有一個或多個鹵素原子取代氫原子的有機碳氫化合物總稱；部分化合物可作為溫室氣體或平流層臭氧消耗物質。'
    },
    'halocline': {
        'traditional_chinese': '鹽躍層',
        'definition_cht': '海洋、河口或湖泊水體中鹽度隨深度快速變化的層次，常與密度分層、垂直混合及聲學傳播特性密切相關。'
    },
    'halogens': {
        'traditional_chinese': '鹵素',
        'definition_cht': '元素週期表第 17 族元素的總稱，包括氟、氯、溴、碘等；在大氣化學中，其活性化合物可參與臭氧破壞與氧化反應。'
    },
    'halons': {
        'traditional_chinese': '哈龍',
        'definition_cht': '含溴為主的鹵代烴滅火劑，曾廣泛用於消防系統；因其對平流層臭氧具強烈破壞作用，已受《蒙特婁議定書》嚴格管制。'
    },
    'hanging dam': {
        'traditional_chinese': '懸掛冰壩',
        'definition_cht': '河川結冰期間，細碎冰晶（frazil ice）在既有冰蓋下方持續堆積形成的冰體，會縮減河道過水斷面並抬升水位。'
    },
    'hanging glacier': {
        'traditional_chinese': '懸冰川',
        'definition_cht': '附著於冰蝕谷側壁或陡峭山坡上的冰川，冰體通常未直接延伸至谷底主冰川，常藉由冰崩或雪崩向下輸送冰雪。'
    },
    'hanning': {
        'traditional_chinese': '漢寧平滑',
        'definition_cht': '利用 Hann（Hanning）窗對資料序列進行加權平滑或加窗處理的方法，可抑制頻譜旁瓣並降低高頻雜訊對分析結果的影響。'
    },
}

paths = [
    Path('/home/node/.openclaw/workspace/met_term/data/h_terms_all_cht.json'),
    Path('/home/node/.openclaw/workspace/met_term/data/glossary_all_cht.json'),
]

for path in paths:
    data = json.loads(path.read_text(encoding='utf-8'))
    changed = 0
    for row in data:
        term = row.get('english')
        if term in updates:
            for k, v in updates[term].items():
                if row.get(k) != v:
                    row[k] = v
                    changed += 1
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(path.name, 'updated_fields', changed)
