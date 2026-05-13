import json
from pathlib import Path

base = Path('/home/node/.openclaw/workspace/met_term/data')
updates = {
    'longwave radiation': {
        'traditional_chinese': '長波輻射',
        'definition_cht': '通常指波長較長的熱紅外輻射，主要由地表、大氣與雲體依其溫度向外放射；在地球輻射收支中常區分為向上與向下長波輻射，並與太陽短波輻射相對。'
    },
    'loo': {
        'traditional_chinese': '盧風',
        'definition_cht': '印度北部與巴基斯坦平原地區夏季常見的地方熱風，通常自西方或西北方吹來，具有高溫、乾燥、陣風強且常夾帶沙塵的特性；多見於 5 至 6 月，易引發熱傷害。'
    },
    'Loofah': {
        'traditional_chinese': '「絲瓜絡」偏振濁度計',
        'definition_cht': '第二次世界大戰期間的英方名稱，指一種極化式雲霧散射觀測儀（polar nephelometer）；用於藉由散射特性判別雲霧中水滴與冰晶等粒子性質，並非植物絲瓜絡本義。'
    },
    'lookup table': {
        'traditional_chinese': '查找表',
        'definition_cht': '以預先建立的對照關係，將某一整數值或代碼快速映射為另一數值、色階或參數的資料表；在衛星影像、雷達顯示與數值產品處理中，常用於像素值轉換與顯示設定。'
    },
    'looming': {
        'traditional_chinese': '上現蜃景',
        'definition_cht': '一種由大氣折射造成的視覺現象，當近地層折射率隨高度變化時，遠方物體會顯得被抬升、拉高或懸浮於實際位置之上；常見於海面或冷暖空氣分層明顯時。'
    },
    'loop antenna': {
        'traditional_chinese': '環形天線',
        'definition_cht': '由閉合導體迴路構成、用以接收或發射無線電波的天線；在無線電測向、雷電電波觀測及部分氣象通訊接收中，可利用其方向性與感應特性辨識訊號來源。'
    },
    'Loop Current': {
        'traditional_chinese': '迴圈洋流',
        'definition_cht': '墨西哥灣內的重要暖流系統，暖水自尤卡坦海峽北上進入灣內後轉向東南，經佛羅里達海峽流出並接續為佛羅里達洋流；其流速快、延伸深，且會影響海洋熱含量與颶風增強條件。'
    },
    'loop rating': {
        'traditional_chinese': '迴圈率定曲線',
        'definition_cht': '在河川水位—流量關係中，因洪水漲落過程存在遲滯效應，使同一水位於漲水期對應流量高於退水期，因而形成封閉或近封閉迴圈的率定曲線。'
    },
    'looping': {
        'traditional_chinese': '循環播放',
        'definition_cht': '指將連續時序的雷達、衛星或其他觀測影像反覆播放成動畫，以便判讀系統移動、發展與演變趨勢的顯示方式。'
    },
    'Los Angeles (photochemical) smog': {
        'traditional_chinese': '洛杉磯型（光化學）煙霧',
        'definition_cht': '由氮氧化物與揮發性有機物在強日照下發生光化學反應所形成的污染型態，特徵為臭氧濃度高、能見度差並常伴隨刺激性氧化物；多見於盆地或谷地型大都市，與倫敦型含硫煙霧相對。'
    },
    'Loschmidt\'s number': {
        'traditional_chinese': '洛施密特數',
        'definition_cht': '指標準溫度與壓力下理想氣體的單位體積粒子數，即氣體的數密度；傳統上可表述為每升約 2.687 × 10^22 個分子（或每立方公分約 2.687 × 10^19 個分子）。'
    },
    'Love wave': {
        'traditional_chinese': '勒夫波',
        'definition_cht': '一種地震表面波，質點運動以水平剪切為主，方向垂直於波的傳播方向且幾乎不含垂直位移；常沿近地表低速層傳播，對地震動破壞評估具有重要意義。'
    },
    'low': {
        'traditional_chinese': '低壓區',
        'definition_cht': '氣象上指某地氣壓低於周圍地區的區域或系統，常簡稱為 low；在近地面分析中常對應氣旋性環流、輻合上升與較易出現雲雨或不穩定天氣的環境。'
    },
    'low frequency': {
        'traditional_chinese': '低頻',
        'definition_cht': '在無線電頻帶分類中指 low frequency（LF），頻率約為 30 至 300 kHz；在氣象通信、導航與電波傳播討論中，常用以描述此頻段訊號及其傳播特性。'
    },
    'low index': {
        'traditional_chinese': '低指數型環流',
        'definition_cht': '指較低的 zonal index（緯向指數）狀態，代表中緯度西風分量偏弱、南北向擾動較明顯，常對應較振幅化的波動、槽脊發展與經向交換較強的天氣型態。'
    },
    'Low Rate Information Transmission': {
        'traditional_chinese': '低速率資訊傳輸',
        'definition_cht': '縮寫為 LRIT，指 GOES、Meteosat、MTSAT 等環境衛星所使用的數位資料播送服務與國際傳輸標準；用以傳送氣象影像、圖表與其他環境資訊，並取代較舊的類比 WEFAX 廣播系統。'
    },
    'low water': {
        'traditional_chinese': '低潮位',
        'definition_cht': '在一個潮汐週期中所達到的最低水位，通稱低潮；常用於潮汐觀測、港灣作業、海岸工程與海圖基準相關討論。'
    },
    'low-flow channel': {
        'traditional_chinese': '低流量河槽',
        'definition_cht': '河川或渠道在枯水、平水或其他低流量條件下實際被水流占據的主槽部分；常為較深且較窄的槽道，對低流量輸送、生態棲地與河工設計具有重要意義。'
    },
    'low-level jet': {
        'traditional_chinese': '低空噴流',
        'definition_cht': '位於邊界層上方或對流層低層的狹長強風帶，常出現在夜間或特定地形與壓力配置下；其對水氣輸送、對流觸發、風切、污染擴散與風能評估都很重要。'
    },
    'Low-reference signal': {
        'traditional_chinese': '低參考訊號',
        'definition_cht': '此條目在標準氣象參考資料中的獨立用法較少見；就字面而言，通常指作為比較、校準或檢測基準之低強度參考訊號，可能見於遙測、通訊或儀器訊號處理語境，實際定義仍需依具體系統文件判定。'
    },
}

for name in ['l_terms_all_cht.json', 'glossary_all_cht.json']:
    path = base / name
    data = json.loads(path.read_text())
    count = 0
    for row in data:
        key = row.get('english')
        if key in updates:
            row.update(updates[key])
            count += 1
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    print(name, count)
