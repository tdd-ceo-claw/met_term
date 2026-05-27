const fs = require('fs');

const updates = {
  'warm front': {
    traditional_chinese: '暖鋒',
    definition_cht: '暖氣團向冷氣團推進時，其前緣形成的鋒面；因暖空氣密度較小，通常沿鋒面緩坡爬升於冷空氣之上，常伴隨層狀雲系、持續性降水與氣溫逐步上升。'
  },
  'warm high': {
    traditional_chinese: '暖高壓',
    definition_cht: '以暖心熱力結構為主的高壓系統，即高壓中心附近的氣柱平均溫度高於周圍環境；常見於副熱帶高壓等深厚反氣旋系統，且通常隨高度增強。'
  },
  'warm low': {
    traditional_chinese: '暖低壓',
    definition_cht: '以暖心熱力結構為主的低壓系統，即低壓中心附近的氣柱平均溫度高於周圍環境；典型例子包括熱帶氣旋，此類系統常在低層輻合與深對流作用下維持。'
  },
  'warm occluded front': {
    traditional_chinese: '暖式囚錮鋒面',
    definition_cht: '囚錮鋒的一種類型，形成時後方冷鋒後側的空氣較前方暖鋒前側空氣溫暖，因此冷鋒後方空氣只抬升較暖空氣，而未能楔入最前方較冷空氣之下；其近地面結構與暖鋒較為相似。'
  },
  'warm occlusion': {
    traditional_chinese: '暖式囚錮',
    definition_cht: '指形成暖式囚錮鋒的囚錮過程或其結果；當冷鋒追上暖鋒時，若後方空氣不如前方冷空氣冷，則較暖空氣被抬升至地面冷空氣之上，形成近似暖鋒特徵的囚錮結構。'
  },
  'warm pool': {
    traditional_chinese: '暖池',
    definition_cht: '海洋表層大範圍高海溫水域，通常指熱帶西太平洋與鄰近海域的高溫水團；其強烈海氣熱通量與深對流活動對季風、沃克環流與聖嬰－南方振盪具有重要影響。'
  },
  'Warm rain': {
    traditional_chinese: '暖雨',
    definition_cht: '在整個降水形成過程中皆處於高於冰點環境、主要不經冰相轉換而生成的雨；其形成仰賴暖雲內雲滴的碰撞、併合與持續增長。'
  },
  'Warm rain process': {
    traditional_chinese: '暖雨過程',
    definition_cht: '暖雲中雲滴在高於 0°C 的環境下，先由凝結成長，再經碰撞併合逐漸形成雨滴的雲微物理過程；為熱帶海洋與低緯對流降水的重要機制。'
  },
  'warm ridge': {
    traditional_chinese: '暖脊',
    definition_cht: '溫度場或厚度場中，暖空氣向外延伸而形成的脊狀區域；常用於等溫線、等厚線或海表溫度分析，以表示相對高溫軸的伸展。'
  },
  'warm sector': {
    traditional_chinese: '暖區',
    definition_cht: '中緯度氣旋近地面結構中，位於暖鋒之後與冷鋒之前、由暖氣團占據的扇形區域；其內常有較高溫、較高濕與較強南向分量風，並是對流不穩定能量累積的重要區域。'
  },
  'warm tongue': {
    traditional_chinese: '暖舌',
    definition_cht: '溫度場中暖空氣或暖水體呈狹長舌狀向外伸展的區域，可見於海表溫度、等熵面或鋒區分析，常反映平流輸送或局地環流作用。'
  },
  'warm wave': {
    traditional_chinese: '暖波',
    definition_cht: '使某地氣溫在一段時間內顯著高於常態的暖異常波動或暖期；在現代用法中多屬 heat wave 的較舊或較廣義表述，強調暖空氣持續影響所造成的升溫現象。'
  },
  'warm-core rings': {
    traditional_chinese: '暖心環流渦',
    definition_cht: '由邊界洋流脫離主流後形成、核心水體較周圍海水溫暖的中尺度渦旋或環流環；在北大西洋常見於墨西哥灣流脫落之暖心環，對熱鹽輸送、生態分布與海氣交換具重要影響。'
  },
  'warm-front wave': {
    traditional_chinese: '暖鋒波',
    definition_cht: '暖鋒上發生的波狀擾動或初生氣旋性彎曲，常表現為鋒面局部起伏與低壓發展，是鋒生成與溫帶氣旋演變中的一種中小尺度擾動。'
  },
  'warm-front-type occlusion': {
    traditional_chinese: '暖鋒型囚錮',
    definition_cht: '囚錮鋒的一種分類，指囚錮後的近地面結構與天氣分布較接近暖鋒；本質上即暖式囚錮，常見於暖鋒前方近地面空氣比冷鋒後方空氣更冷的情況。'
  },
  'warm-type occlusion': {
    traditional_chinese: '暖式囚錮',
    definition_cht: '囚錮鋒的暖型結構稱呼，表示冷鋒追上暖鋒後，後方空氣未冷到足以楔入前方冷空氣之下，因而形成近似暖鋒特性的囚錮帶。'
  },
  'warning': {
    traditional_chinese: '警報',
    definition_cht: '氣象或水文機關對已發生、即將發生或高度可能發生之危險天氣、水文或環境事件所發布的正式警示資訊；其急迫性通常高於 watch，目的在促使受影響區域立即採取防災行動。'
  },
  'warning stage': {
    traditional_chinese: '警戒水位',
    definition_cht: '河川、湖泊或其他水體的水位達到須開始發布洪水警報或採取防災應變行動的基準水位；其設定依測站位置、地形與歷史淹水影響而定。'
  },
  'Wasatch winds': {
    traditional_chinese: '瓦薩奇風',
    definition_cht: '美國猶他州瓦薩奇山區附近的地方風名稱，通常指受山地地形、坡降流或峽谷風效應影響的強勁局地風；可伴隨突增陣風、氣溫變化與下坡增暖乾燥效應。'
  },
  'Washoe zephyr': {
    traditional_chinese: '瓦肖西風',
    definition_cht: '美國內華達州西部、內華達山脈東側夏季常見的日變化局地風，通常於午後至傍晚自西至西南方增強並轉為陣風性強風；常夾帶沙塵，對當地火災天氣與空氣品質具有影響。'
  }
};

const notes = {
  'warm front': { checks: ['https://glossary.ametsoc.org/wiki/warm_front','https://en.wikipedia.org/wiki/Warm_front'], changed: true },
  'warm high': { checks: ['https://glossary.ametsoc.org/wiki/warm_high','https://glossary.ametsoc.org/wiki/cold-core_high'], changed: true },
  'warm low': { checks: ['https://glossary.ametsoc.org/wiki/warm_low','https://glossary.ametsoc.org/wiki/cold-core_low'], changed: true },
  'warm occluded front': { checks: ['https://glossary.ametsoc.org/wiki/warm_occluded_front','https://en.wikipedia.org/wiki/Occluded_front'], changed: true },
  'warm occlusion': { checks: ['https://glossary.ametsoc.org/wiki/warm_occlusion','https://en.wikipedia.org/wiki/Occluded_front'], changed: true },
  'warm pool': { checks: ['https://glossary.ametsoc.org/wiki/warm_pool','https://en.wikipedia.org/wiki/Warm_pool'], changed: true },
  'Warm rain': { checks: ['https://glossary.ametsoc.org/wiki/warm_rain','https://en.wikipedia.org/wiki/Rain#Warm_rain_process'], changed: true },
  'Warm rain process': { checks: ['https://glossary.ametsoc.org/wiki/Warm_rain_process','https://en.wikipedia.org/wiki/Rain#Warm_rain_process'], changed: true },
  'warm ridge': { checks: ['https://glossary.ametsoc.org/wiki/warm_ridge','https://glossary.ametsoc.org/wiki/ridge'], changed: true },
  'warm sector': { checks: ['https://glossary.ametsoc.org/wiki/warm_sector','https://en.wikipedia.org/wiki/Mid-latitude_cyclone#Structure'], changed: true },
  'warm tongue': { checks: ['https://glossary.ametsoc.org/wiki/warm_tongue','https://glossary.ametsoc.org/wiki/cold_tongue'], changed: true },
  'warm wave': { checks: ['https://glossary.ametsoc.org/wiki/warm_wave','https://en.wikipedia.org/wiki/Heat_wave'], changed: true },
  'warm-core rings': { checks: ['https://glossary.ametsoc.org/wiki/warm-core_rings','https://en.wikipedia.org/wiki/Warm-core_ring'], changed: true },
  'warm-front wave': { checks: ['https://glossary.ametsoc.org/wiki/warm-front_wave','https://glossary.ametsoc.org/wiki/frontal_wave'], changed: true },
  'warm-front-type occlusion': { checks: ['https://glossary.ametsoc.org/wiki/warm-front-type_occlusion','https://en.wikipedia.org/wiki/Occluded_front'], changed: true },
  'warm-type occlusion': { checks: ['https://glossary.ametsoc.org/wiki/warm-type_occlusion','https://en.wikipedia.org/wiki/Occluded_front'], changed: true },
  'warning': { checks: ['https://glossary.ametsoc.org/wiki/warning','https://www.weather.gov/lwx/warningsdefined'], changed: true },
  'warning stage': { checks: ['https://glossary.ametsoc.org/wiki/warning_stage','https://www.weather.gov/aprfc/terminology'], changed: true },
  'Wasatch winds': { checks: ['https://glossary.ametsoc.org/wiki/Wasatch_winds','https://en.wikipedia.org/wiki/Wasatch'], changed: true },
  'Washoe zephyr': { checks: ['https://glossary.ametsoc.org/wiki/Washoe_zephyr','https://en.wikipedia.org/wiki/Washoe_Zephyr'], changed: true }
};

for (const file of ['w_terms_all_cht.json', 'glossary_all_cht.json']) {
  const path = `/home/node/.openclaw/workspace/met_term/data/${file}`;
  const data = JSON.parse(fs.readFileSync(path, 'utf8'));
  let changed = 0;
  for (const row of data) {
    if (updates[row.english]) {
      Object.assign(row, updates[row.english]);
      changed++;
    }
  }
  fs.writeFileSync(path, JSON.stringify(data, null, 2) + '\n');
  console.log(file, changed);
}

fs.writeFileSync('/home/node/.openclaw/workspace/met_term/tmp_w_200_219_review_notes.json', JSON.stringify(notes, null, 2) + '\n');
console.log('notes', Object.keys(notes).length);
