import json
from pathlib import Path

updates = {
    'Solar angle': {
        'traditional_chinese': '太陽角',
        'definition_cht': '指描述太陽相對於地平面、天頂、方位或受照表面幾何位置關係的各種角度量，例如太陽高度角、方位角、入射角與天頂角等，常用於日照分析、輻射計算與太陽能應用。'
    },
    'solar atmospheric tide': {
        'traditional_chinese': '太陽大氣潮汐',
        'definition_cht': '指由太陽週期性加熱大氣，尤其是臭氧對紫外線吸收與對流層潛熱釋放所激發的全球尺度週期性大氣振盪；其主要週期常為日潮與半日潮，是大氣潮汐的重要組成。'
    },
    'solar aureole': {
        'traditional_chinese': '太陽暈光',
        'definition_cht': '指圍繞太陽視盤周圍、由大氣中氣膠、薄雲或細小水滴／冰晶前向散射形成的亮區或模糊光暈，常用於輻射傳輸、天空亮度分布與氣膠性質分析。'
    },
    'Solar Backscatter Ultraviolet Radiometer': {
        'traditional_chinese': '太陽後向散射紫外輻射計',
        'definition_cht': '指衛星搭載的紫外遙測儀器，利用量測地球大氣與地表對太陽紫外輻射的後向散射訊號，反演總臭氧量、臭氧垂直分布及相關痕量氣體資訊；常簡稱 SBUV。'
    },
    'solar climate': {
        'traditional_chinese': '日照氣候',
        'definition_cht': '指某地區太陽輻射、日照時數、太陽高度與季節性受照條件所構成的長期平均日照環境，常用於氣候描述、建築設計、農業與太陽能資源評估。'
    },
    'Solar cycle': {
        'traditional_chinese': '太陽活動週期',
        'definition_cht': '指太陽黑子數、耀斑、日冕活動與磁場強度等太陽活動隨時間呈現的週期性變化，典型主週期約為 11 年，而完整磁極反轉週期約為 22 年。'
    },
    'solar day': {
        'traditional_chinese': '太陽日',
        'definition_cht': '指同一地點相對於太陽連續兩次上中天或連續兩次太陽子午通過之間的時間間隔，即以太陽為基準的日長；在地球上其平均值約為 24 小時。'
    },
    'Solar flux': {
        'traditional_chinese': '太陽通量',
        'definition_cht': '指單位面積在單位時間內所接收到的太陽輻射能量通率；在太空天氣領域亦常特指以 10.7 公分波段表示的太陽射電通量，用作表徵太陽活動強度的指標。'
    },
    'Solar Imaging Suite': {
        'traditional_chinese': '太陽成像套件',
        'definition_cht': '指用於太陽觀測的一組成像儀器或整合式酬載，通常以多波段紫外、極紫外或 X 射線影像監測太陽盤面與日冕結構、耀斑與活動區演變，以支援太空天氣監測。'
    },
    'solar infrared': {
        'traditional_chinese': '太陽紅外輻射',
        'definition_cht': '指太陽發射光譜中位於紅外波段的電磁輻射成分，是地表與大氣吸收太陽能的重要部分，常用於輻射收支、遙測與熱環境分析。'
    },
    'Solar proton event': {
        'traditional_chinese': '太陽質子事件',
        'definition_cht': '指太陽耀斑或日冕物質拋射相關震波加速大量高能質子與其他帶電粒子，使其在行星際空間快速增強的事件；可干擾太空器、通訊與高緯航空輻射環境。'
    },
    'solar radiation': {
        'traditional_chinese': '太陽輻射',
        'definition_cht': '指太陽所發射並傳播至地球的大部分短波電磁輻射，包含紫外、可見光與近紅外成分，是驅動地球天氣、氣候與地表能量交換的主要能量來源。'
    },
    'solar radiation observation': {
        'traditional_chinese': '太陽輻射觀測',
        'definition_cht': '指對直達、散射及全球太陽輻射之強度、光譜特性與時間變化所進行的量測與記錄，用以支援氣候監測、輻射收支分析、農業氣象及太陽能資源評估。'
    },
    'solar radio emission': {
        'traditional_chinese': '太陽射電輻射',
        'definition_cht': '指太陽在無線電波段所發射的電磁輻射，來源可包括寧靜太陽背景、黑子區、耀斑與日冕爆發活動；其變化是監測太陽活動與太空天氣的重要訊號。'
    },
    'solar signal': {
        'traditional_chinese': '太陽訊號',
        'definition_cht': '指可歸因於太陽輻射或太陽活動變化的可辨識訊號或變動成分，常見於氣候、電離層、地球物理或遙測時間序列分析中，用以表示太陽強迫的影響。'
    },
    'solar spectrum': {
        'traditional_chinese': '太陽光譜',
        'definition_cht': '指太陽輻射在各波長上的能量分布，涵蓋紫外、可見光與紅外等波段；其形狀近似黑體輻射，但疊加了由太陽大氣吸收形成的多種譜線結構。'
    },
    'solar tide': {
        'traditional_chinese': '太陽潮汐',
        'definition_cht': '指由太陽引潮力所造成的海洋、固體地球或大氣潮汐分量；就海洋潮汐而言，其作用通常弱於月球潮汐，但會與月潮疊加影響潮位變化。'
    },
    'Solar wind': {
        'traditional_chinese': '太陽風',
        'definition_cht': '指自太陽日冕持續向外流出的高溫電漿流，主要由電子、質子與少量重離子組成，會充滿日球層並與地球磁層交互作用，進而影響太空天氣。'
    },
    'Solar X-ray Imager': {
        'traditional_chinese': '太陽 X 射線成像儀',
        'definition_cht': '指用於觀測太陽軟 X 射線輻射的太空成像儀器，可監測日冕高溫結構、活動區與耀斑發展，常應用於即時太空天氣監測與預警。'
    },
    'solar zenith angle': {
        'traditional_chinese': '太陽天頂角',
        'definition_cht': '指觀測地點天頂方向與太陽中心方向之間的夾角，等於 90° 減去太陽高度角；為描述太陽入射幾何、輻射傳輸與遙測反演的重要參數。'
    }
}

for rel in ['data/s_terms_all_cht.json', 'data/glossary_all_cht.json']:
    path = Path(rel)
    data = json.loads(path.read_text())
    changed = 0
    for row in data:
        if row['english'] in updates:
            row.update(updates[row['english']])
            changed += 1
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    print(rel, changed)
