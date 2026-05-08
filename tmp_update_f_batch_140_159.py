import json
from pathlib import Path

repo = Path('/home/node/.openclaw/workspace/met_term')
letter_path = repo / 'data' / 'f_terms_all_cht.json'
all_path = repo / 'data' / 'glossary_all_cht.json'

updates = {
    'floeberg': {
        'traditional_chinese': '巨型浮冰片',
        'definition_cht': '尺度極大的浮冰片，外形可近似小型冰山，但本質仍屬海冰或棚冰碎塊，而非由陸源冰川崩解形成的冰山。'
    },
    'flood': {
        'traditional_chinese': '洪水',
        'definition_cht': '河川、湖泊、蓄水體、潮水或地表逕流之水量超出正常容納範圍，致使原本乾燥地區遭受淹沒的現象。'
    },
    'flood channel': {
        'traditional_chinese': '洪道；行洪通道',
        'definition_cht': '供洪水宣洩、分洪或導流的天然或人工水道，用以將洪流導離主河道、聚落或重要設施，降低淹水風險。'
    },
    'flood current': {
        'traditional_chinese': '漲潮流',
        'definition_cht': '潮汐循環中伴隨潮位上升而向岸、向河口內部或向上游流動的水流階段，與退潮流相對；著重描述水平流動而非潮位高低。'
    },
    'flood forecast': {
        'traditional_chinese': '洪水預報',
        'definition_cht': '依據降雨、上游流量、土壤濕度、融雪或潮位等資料，預測未來河川水位、流量、到達時間或可能淹水情形的作業成果。'
    },
    'flood forecasting': {
        'traditional_chinese': '洪水預報作業',
        'definition_cht': '整合水文氣象觀測、模式計算、警戒判釋與資訊發布程序，以預測洪水發生時間、強度、演變及影響範圍的系統性作業。'
    },
    'flood frequency distribution': {
        'traditional_chinese': '洪水頻率分布',
        'definition_cht': '表示不同規模洪峰流量、洪量或水位在長期紀錄中出現機率或超越機率的統計分布，用於洪水頻率分析與重現期推估。'
    },
    'flood interval': {
        'traditional_chinese': '洪水重現間隔',
        'definition_cht': '指某一規模洪水在統計上平均再度出現的時間間隔，常用以表述特定洪水事件的重現期；不代表該洪水只會依固定週期發生。'
    },
    'Flood irrigation': {
        'traditional_chinese': '漫灌',
        'definition_cht': '一種地表灌溉方式，將灌溉水引入田面或畦田，使其藉重力自然鋪展、蓄積或緩流滲入土壤。'
    },
    'flood marks': {
        'traditional_chinese': '洪痕',
        'definition_cht': '洪水過後留在建築物、樹木、河岸或其他地物上的水位痕跡，可作為重建洪峰高度、淹水深度與洪水範圍的重要依據。'
    },
    'flood mitigation': {
        'traditional_chinese': '減洪措施',
        'definition_cht': '為降低洪水風險、災害影響與暴露脆弱度而採取的工程及非工程對策，如滯洪、分洪、預警、土地使用管理與建築防護等。'
    },
    'flood plain': {
        'traditional_chinese': '洪氾平原',
        'definition_cht': '位於河道相鄰低地、曾於歷史洪水期間受河水淹漫的河谷地帶；多由長期沖積作用形成，土壤肥沃但具洪災暴露。'
    },
    'flood proofing': {
        'traditional_chinese': '建物防洪化',
        'definition_cht': '透過抬升、封堵、設置擋水設施、改善排水或調整建築配置與用途等措施，降低建築物及設施遭受洪水損害的作法。'
    },
    'flood routing': {
        'traditional_chinese': '洪水演算',
        'definition_cht': '推算洪波沿河道或通過水庫、渠道等系統時，其時間、波形與振幅如何逐步變化的水文與水力計算程序。'
    },
    'flood stage': {
        'traditional_chinese': '洪水位；警戒洪水位',
        'definition_cht': '某測站事先訂定的水位基準；當水位升至此值以上時，開始對生命、財產或交通等造成危害，並常作為發布洪水警報的重要門檻。'
    },
    'flood strength': {
        'traditional_chinese': '漲潮流強度',
        'definition_cht': '指漲潮流在特定地點的流速或流勢強弱，用以描述潮水向岸或向上游推進時的水流強度。'
    },
    'flood tide': {
        'traditional_chinese': '漲潮',
        'definition_cht': '潮位自低潮逐漸上升至高潮的潮汐階段；著重描述海面高度變化，與著重水平流動的漲潮流不同。'
    },
    'flood warning': {
        'traditional_chinese': '洪水警報',
        'definition_cht': '表示洪水已經發生、即將發生或迫近的正式警示，提醒民眾與相關單位立即採取防災或避難行動。'
    },
    'flood watch': {
        'traditional_chinese': '洪水注意報',
        'definition_cht': '表示未來一段時間內具備發生洪水的有利條件，雖不代表洪水必然發生，但應提高警覺並預作準備。'
    },
    'flood wave': {
        'traditional_chinese': '洪波',
        'definition_cht': '因降雨、融雪、潰壩或水庫放流等引起的河川流量或水位上升過程，其特徵包括流量增至洪峰後再逐漸消退的完整波動。'
    }
}

def apply_updates(path):
    arr = json.loads(path.read_text(encoding='utf-8'))
    changed = 0
    for row in arr:
        key = row.get('english')
        if key in updates:
            for k, v in updates[key].items():
                if row.get(k) != v:
                    row[k] = v
                    changed += 1
    path.write_text(json.dumps(arr, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return changed

c1 = apply_updates(letter_path)
c2 = apply_updates(all_path)
print({'letter_changes': c1, 'all_changes': c2})
