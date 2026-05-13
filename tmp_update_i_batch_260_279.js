const fs = require('fs');
const updates = {
  'International Geomagnetic Reference Field': {
    traditional_chinese: '國際地磁參考場',
    definition_cht: '由國際地磁與高空物理學協會（IAGA）定期發布的地球主磁場及其長期變化之標準數學模型，主要以全球觀測站、測量調查與衛星資料建立，廣泛用於地磁研究、資料比對與歷史磁場重建。'
  },
  'international index numbers': {
    traditional_chinese: '國際指數編號',
    definition_cht: '依國際通用規範編製的指數代號或編號系統，用以標示特定觀測、分類、等級或統計指標；其確切內容須依所屬學科與標準文件而定。'
  },
  'International Pyrheliometric Scale': {
    traditional_chinese: '國際直接日射量表',
    definition_cht: '供直接日射（太陽直達輻射）觀測儀器校準與比對使用的國際輻射基準尺度，用以統一各地日射量測結果。'
  },
  'International Satellite Cloud Climatology Project': {
    traditional_chinese: '國際衛星雲氣候計畫',
    definition_cht: '世界氣候研究計畫（WCRP）早期的重要國際合作計畫，利用多顆氣象衛星的輻射觀測資料建立全球雲分布、雲性質及其日變化、季節變化與年際變化的長期資料集，以支援輻射收支與水循環研究。'
  },
  'international standard atmosphere': {
    traditional_chinese: '國際標準大氣',
    definition_cht: '以假設的大氣垂直溫度、壓力、密度等平均結構所建立的標準大氣模式，供航空、儀器校準、彈道、遙測與工程計算作共同參考。'
  },
  'international synoptic code': {
    traditional_chinese: '國際綜觀天氣電碼',
    definition_cht: '世界氣象組織所採用、用於國際交換綜觀氣象觀測與分析資料的標準化電碼系統，涵蓋地面、高空及相關氣象報文編碼。'
  },
  'international synoptic surface observation code': {
    traditional_chinese: '國際地面綜觀觀測電碼',
    definition_cht: '國際綜觀天氣電碼中用於地面氣象站綜觀觀測報告的標準編碼格式，常指 SYNOP 類報文，用以交換氣壓、氣溫、風、雲、天氣現象等資料。'
  },
  'International System of Units': {
    traditional_chinese: '國際單位制',
    definition_cht: '國際通用的現代公制單位系統，簡稱 SI，以秒、公尺、公斤、安培、開爾文、莫耳與燭光等基本單位為核心，供科學、工程與日常量測統一使用。'
  },
  'International Table calorie': {
    traditional_chinese: '國際表卡路里',
    definition_cht: '歷史上使用的一種卡路里定義，依國際表換算採定值 1 cal = 4.1868 J；現今能量單位通常改用焦耳。'
  },
  'International Units': {
    traditional_chinese: '國際單位',
    definition_cht: '以生物活性或效價為基準所定義的計量單位，常用於維生素、荷爾蒙、疫苗及其他生物製劑；不同物質的國際單位彼此不可直接以質量換算。'
  },
  'interplanetary dust': {
    traditional_chinese: '行星際塵埃',
    definition_cht: '分布於太陽系行星際空間中的微小固體粒子，主要來自彗星、 小行星碰撞碎屑與少量星際塵，會造成黃道光並影響太空環境觀測。'
  },
  'Interplanetary magnetic field': {
    traditional_chinese: '行星際磁場',
    definition_cht: '由太陽磁場隨太陽風向外攜帶並充滿太陽系空間所形成的磁場，又稱日球磁場；其結構常呈帕克螺旋，對地磁擾動與太空天氣具有重要影響。'
  },
  'interpluvial': {
    traditional_chinese: '間雨期的',
    definition_cht: '指兩個多雨期或洪雨期之間較乾燥的時段，常用於古氣候或地質文獻中，與 pluvial（雨期、濕潤期）相對。'
  },
  'interpolation': {
    traditional_chinese: '內插',
    definition_cht: '依據已知資料點，在其範圍內推估中間未知值的方法；廣泛用於氣象分析、數值模式、網格化資料與時間序列處理。'
  },
  'interpulse period': {
    traditional_chinese: '脈衝間隔',
    definition_cht: '在脈衝系統中，相鄰兩個發射脈衝之間的時間間隔；雷達中常用以決定脈衝重複頻率及可無模糊量測的最大距離。'
  },
  'interrupted stream': {
    traditional_chinese: '斷續河流',
    definition_cht: '沿河道有些河段流動中斷、消失或轉入地下，之後又在下游重新出露的河流；常見於乾旱區、喀斯特地形或強入滲河床。'
  },
  'interstadial': {
    traditional_chinese: '間冰段',
    definition_cht: '冰期內兩個較冷的冰段（stadial）之間相對較暖的短暫氣候階段，其暖化程度與持續時間通常小於完整的間冰期。'
  },
  'interstellar dust': {
    traditional_chinese: '星際塵埃',
    definition_cht: '分布於恆星際空間中的微細固體粒子，主要由矽酸鹽、碳質物與冰質成分構成，能吸收、散射與再輻射電磁波，並參與分子雲與恆星形成過程。'
  },
  'interstice': {
    traditional_chinese: '空隙',
    definition_cht: '指物體、顆粒、晶體或結構之間的細小間隙或孔隙；在地球科學中可用於描述土壤、岩石、雪冰或顆粒介質中的孔隙空間。'
  },
  'intertropical convergence zone': {
    traditional_chinese: '熱帶輻合帶',
    definition_cht: '位於赤道附近、東北與東南信風匯聚的帶狀低壓與對流活躍區，常伴隨旺盛雲雨與雷暴，其位置會隨季節南北移動。'
  }
};

for (const file of ['data/i_terms_all_cht.json', 'data/glossary_all_cht.json']) {
  const data = JSON.parse(fs.readFileSync(file, 'utf8'));
  for (const row of data) {
    if (updates[row.english]) Object.assign(row, updates[row.english]);
  }
  fs.writeFileSync(file, JSON.stringify(data, null, 2) + '\n');
}
console.log('updated', Object.keys(updates).length, 'terms');
