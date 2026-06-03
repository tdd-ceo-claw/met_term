import json
from pathlib import Path

updates = {
    'yagi antenna': {
        'traditional_chinese': '八木天線',
        'definition_cht': '指由一個受激元件、反射器與一個以上導向器組成的高指向性天線，能將電磁波能量集中於前向，具較高增益，常用於雷達、無線電通訊與大氣遙測系統。'
    },
    'Yagi-Uda antenna': {
        'traditional_chinese': '八木－宇田天線',
        'definition_cht': '由不同長度與間距的偶極元件構成之定向天線陣列，典型配置包括受激元件、反射器與多個導向器；「八木天線」通常即指此類天線，常見於雷達與遙測設備。'
    },
    'yalca': {
        'traditional_chinese': '雅爾卡雪暴',
        'definition_cht': '秘魯北部安地斯山口一帶對強烈雪暴的地方名稱，通常指伴隨陣性強風的劇烈降雪事件，對山區通行與安全影響顯著。'
    },
    'yamase': {
        'traditional_chinese': '山背風',
        'definition_cht': '日本東北地方夏季常見的冷濕偏東北至東風，源自鄂霍次克海高壓並掠過冷海面，常帶來低溫、雲、雨、霧及冷夏災害。'
    },
    'Yanai wave': {
        'traditional_chinese': '柳井波',
        'definition_cht': '又稱混合羅斯貝－重力波，為赤道波的一類，兼具羅斯貝波與重力波特性，可在熱帶大氣與海洋中沿赤道傳播，常用於描述赤道擾動與季內變異。'
    },
    'Yaw': {
        'traditional_chinese': '偏航',
        'definition_cht': '指飛行器、天線或其他剛體繞垂直軸的旋轉，使其朝向向左或向右改變；在航空與雷達作業中常用以描述方位偏轉。'
    },
    'year': {
        'traditional_chinese': '年',
        'definition_cht': '以地球繞太陽公轉週期或曆法制度為基準的時間單位；在氣候統計、水文平衡與年際變率分析中，年尺度是整理與比較長期觀測資料的基本時間單位。'
    },
    'Yellow Sea Warm Current': {
        'traditional_chinese': '黃海暖流',
        'definition_cht': '冬季沿黃海海槽向北侵入的暖鹽海流，將東海與黑潮系較暖海水輸送至黃海及渤海鄰近海域，對區域熱鹽結構、冷水團分布與海氣交互作用具有重要影響。'
    },
    'yellow snow': {
        'traditional_chinese': '黃雪',
        'definition_cht': '指雪面因松柏類花粉而呈金黃或黃色的現象；廣義上亦可指沙塵、細砂等黃褐色微粒沉降於雪面所造成的黃色外觀。'
    },
    'yellow wind': {
        'traditional_chinese': '黃風',
        'definition_cht': '東亞，尤指華北一帶冬季常見的強烈冷乾西風，挾帶沙漠黃塵而行，可造成揚沙、能見度下降與空氣品質惡化。'
    },
    'youg': {
        'traditional_chinese': '尤格熱風',
        'definition_cht': '地中海地區夏季天氣不穩定時出現的炎熱地方風名稱，通常指伴隨悶熱與天氣轉趨不穩的暖熱氣流。'
    },
    'young ice': {
        'traditional_chinese': '幼冰',
        'definition_cht': '介於尼拉斯（nilas）與一年冰之間的海冰發育階段，厚度通常約 10 至 30 公分，仍具有一定彈性與變形性，可再細分為灰冰與灰白冰。'
    },
    'Younger Dryas': {
        'traditional_chinese': '新仙女木期',
        'definition_cht': '末次冰消期晚期一次顯著且相對短暫的急遽回冷事件，約發生於距今 12,900 至 11,700 年前，常用於古氣候研究以探討突變氣候、海洋環流調整與環境響應。'
    },
    'Z time': {
        'traditional_chinese': '祖魯時間',
        'definition_cht': '以零時區為基準的時間表示法，實務上通常等同於 UTC；因 NATO 音標字母以 Z（Zulu）代表零經度時區，故廣泛用於航空、航海與氣象作業。'
    },
    "Z''–''R'' relation": {
        'traditional_chinese': '雷達反射率—降雨率關係',
        'definition_cht': '指雷達反射率因子 Z 與降雨率 R 之間的經驗或理論換算關係，常寫為 Z = aR^b，用於依天氣雷達回波定量估算降雨強度。'
    },
    'Z0': {
        'traditional_chinese': '粗糙度長度',
        'definition_cht': '又稱空氣動力粗糙度長度；在近地層對數風速剖面中，指將平均風速向下外推至零時所對應的理論高度，用以表徵地表粗糙特性。'
    },
    'Zanzibar Current': {
        'traditional_chinese': '桑吉巴洋流',
        'definition_cht': '印度洋西部沿東非海岸自南向北長年流動的西岸邊界流，約自南緯 10 度附近北上；其位置與強度受季風環流影響，並可與索馬利洋流交會。'
    },
    'zastrugi': {
        'traditional_chinese': '風蝕雪脊',
        'definition_cht': '指積雪表面受強風侵蝕與再堆積後形成的狹長、堅硬雪脊或溝槽地形，常見於極區與高山風強區，走向多與盛行風大致平行。'
    },
    'Zeeman effect': {
        'traditional_chinese': '塞曼效應',
        'definition_cht': '指原子或分子光譜線在外加磁場作用下分裂為兩個或多個頻率略異分量的現象，可用於診斷磁場強度、方向與介質性質。'
    },
    'Zeldovich mechanism': {
        'traditional_chinese': '澤爾多維奇機制',
        'definition_cht': '描述高溫條件下氮與氧反應生成熱力型氮氧化物（thermal NOx）的主要化學機制，常用於燃燒、空氣污染與大氣化學研究。'
    },
}

review_notes = {
    'yagi antenna': {'checks': ['https://glossary.ametsoc.org/wiki/Yagi-uda_antenna', 'https://en.wikipedia.org/wiki/Yagi%E2%80%93Uda_antenna'], 'changed': True},
    'Yagi-Uda antenna': {'checks': ['https://glossary.ametsoc.org/wiki/Yagi-uda_antenna', 'https://www.radartutorial.eu/06.antennas/Yagi%20Antenna.en.html'], 'changed': True},
    'yalca': {'checks': ['https://glossary.ametsoc.org/wiki/Yalca', 'https://encyclopedia2.thefreedictionary.com/yalca'], 'changed': True},
    'yamase': {'checks': ['https://glossary.ametsoc.org/wiki/Yamase', 'https://www.jstage.jst.go.jp/article/jmsj1965/75/6/75_6_1053/_article/-char/en'], 'changed': True},
    'Yanai wave': {'checks': ['https://en.wikipedia.org/wiki/Equatorial_wave', 'https://agupubs.onlinelibrary.wiley.com/doi/full/10.1002/jgrc.20121'], 'changed': True},
    'Yaw': {'checks': ['https://en.wikipedia.org/wiki/Aircraft_principal_axes', 'https://www.grc.nasa.gov/www/k-12/VirtualAero/BottleRocket/airplane/yaw.html'], 'changed': True},
    'year': {'checks': ['https://science.nasa.gov/learn/basics-of-space-flight/chapter2-1/', 'https://spaceplace.nasa.gov/years-on-other-planets/en/'], 'changed': True},
    'Yellow Sea Warm Current': {'checks': ['https://www.sciencedirect.com/science/article/abs/pii/S100160580860133X', 'https://www.frontiersin.org/journals/marine-science/articles/10.3389/fmars.2021.767850/full'], 'changed': True},
    'yellow snow': {'checks': ['https://glossary.ametsoc.org/wiki/Yellow_snow', 'https://www.ajc.com/pulse/what-is-yellow-snow-pollution-is-a-common-explanation/U7CKE5ZAGZDBXNLFUU7HG5BROA/'], 'changed': True},
    'yellow wind': {'checks': ['https://glossary.ametsoc.org/wiki/Yellow_wind', 'https://en.wikipedia.org/wiki/Asian_Dust'], 'changed': True},
    'youg': {'checks': ['https://glossary.ametsoc.org/wiki/Youg', 'https://encyclopedia2.thefreedictionary.com/youg'], 'changed': True},
    'young ice': {'checks': ['https://wmo.int/topics/sea-ice', 'https://nsidc.org/learn/parts-cryosphere/sea-ice/science-sea-ice'], 'changed': True},
    'Younger Dryas': {'checks': ['https://www.britannica.com/science/Younger-Dryas-climate-interval', 'https://www.ncdc.noaa.gov/abrupt-climate-change/The%20Younger%20Dryas'], 'changed': True},
    'Z time': {'checks': ['https://www.timeanddate.com/time/zones/z', 'https://www.aopa.org/news-and-media/all-news/2020/march/02/training-tip-its-about-time'], 'changed': True},
    "Z''–''R'' relation": {'checks': ['https://www.weather.gov/tae/research-zrpaper', 'https://www.hindawi.com/journals/amete/2018/8202031/'], 'changed': True},
    'Z0': {'checks': ['https://glossary.ametsoc.org/wiki/Aerodynamic_roughness_length', 'http://www.webmet.com/met_monitoring/663.html'], 'changed': True},
    'Zanzibar Current': {'checks': ['https://glossary.ametsoc.org/wiki/Zanzibar_current', 'https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2011JC007417'], 'changed': True},
    'zastrugi': {'checks': ['https://en.wikipedia.org/wiki/Sastrugi', 'https://www.thefreedictionary.com/zastrugi'], 'changed': True},
    'Zeeman effect': {'checks': ['https://www.britannica.com/science/Zeeman-effect', 'https://en.wikipedia.org/wiki/Zeeman_effect'], 'changed': True},
    'Zeldovich mechanism': {'checks': ['https://en.wikipedia.org/wiki/Zeldovich_mechanism', 'https://taylorandfrancis.com/knowledge/Engineering_and_technology/Chemical_engineering/Zeldovich_mechanism/'], 'changed': True},
}


def apply_updates(path_str):
    path = Path(path_str)
    rows = json.loads(path.read_text(encoding='utf-8'))
    changed = False
    for row in rows:
        english = row['english']
        if english in updates:
            new = updates[english]
            if row.get('traditional_chinese') != new['traditional_chinese'] or row.get('definition_cht') != new['definition_cht']:
                row['traditional_chinese'] = new['traditional_chinese']
                row['definition_cht'] = new['definition_cht']
                changed = True
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return changed

apply_updates('data/y_terms_all_cht.json')
apply_updates('data/z_terms_all_cht.json')
apply_updates('data/glossary_all_cht.json')
Path('tmp_yz_000_019_review_notes.json').write_text(json.dumps(review_notes, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('updated y/z batch 000-019 and glossary_all_cht.json')
