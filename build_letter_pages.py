import json
import re
from pathlib import Path
from urllib.parse import quote

REPO = Path('/home/node/.openclaw/workspace/met_term')
DATA_DIR = REPO / 'data'
LETTERS_DIR = REPO / 'letters'
LETTERS_DIR.mkdir(exist_ok=True)
BUILD_DATE = '2026-04-29'
SITE_TITLE = '氣象辭典'
SITE_SUBTITLE = '青絲白髮一瞬間，年華老去向誰言'
SITE_DESC = '本網頁內容為實驗性質，網頁整體風格為科技文青溫暖風格。'
AMS_WIKI_BASE = 'https://glossary.ametsoc.org/wiki/'


def load_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def dump_json(path: Path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')


def letters_available():
    letters = []
    for p in sorted(DATA_DIR.glob('*_terms_all_cht.json')):
        if p.name == 'glossary_all_cht.json':
            continue
        letter = p.name[0].lower()
        if letter.isalpha():
            letters.append(letter)
    return sorted(set(letters))


def normalize_spaces(text: str) -> str:
    return re.sub(r'\s+', ' ', (text or '').strip())


def build_source_url(term: str) -> str:
    normalized = normalize_spaces(term).replace(' ', '_')
    return AMS_WIKI_BASE + quote(normalized, safe='_-(),')


def normalize_row(row: dict) -> dict:
    english = normalize_spaces(row.get('english', ''))
    traditional_chinese = normalize_spaces(row.get('traditional_chinese', ''))
    definition_cht = normalize_spaces(row.get('definition_cht', ''))
    source_url = row.get('source_url') or build_source_url(english)
    return {
        'english': english,
        'traditional_chinese': traditional_chinese,
        'definition_cht': definition_cht,
        'source_url': source_url,
    }


def common_head() -> str:
    return '''<style>
:root{--bg:#09111f;--panel:#101b2d;--line:#2a4a73;--cyan:#7fd6ff;--gold:#d5a86c;--warm:#d98b73;--warm2:#f0c7a6;--text:#eaf2ff;--muted:#9db0c9;}
*{box-sizing:border-box} html{scroll-behavior:smooth} body{margin:0;font-family:"Noto Serif TC","PingFang TC","Microsoft JhengHei",serif;background:radial-gradient(circle at top,#24466d 0%,#15131d 44%,#0d0b12 100%);color:var(--text);} a{color:inherit;text-decoration:none}
.header,.wrap,.footer{max-width:1320px;margin:0 auto;padding-left:24px;padding-right:24px} .header{padding-top:44px;padding-bottom:22px;display:grid;grid-template-columns:minmax(0,1fr) auto;gap:24px;align-items:start}
.header-text{min-width:0}.header-art{justify-self:end;align-self:start}.header-art img{width:clamp(120px,13vw,180px);height:auto;display:block;border-radius:18px;box-shadow:0 10px 28px rgba(0,0,0,.28);border:1px solid rgba(242,210,177,.28)} .kicker{color:var(--gold);letter-spacing:.18em;font-size:12px;text-transform:uppercase;margin-bottom:12px} h1{margin:0;font-size:44px;line-height:1.15} .sub{margin-top:14px;color:var(--muted);max-width:980px;line-height:1.8}
.card{background:linear-gradient(180deg,rgba(24,31,48,.92),rgba(22,16,25,.96));border:1px solid rgba(127,214,255,.2);border-radius:24px;overflow:hidden;box-shadow:0 18px 50px rgba(0,0,0,.35)} .hero-band{height:8px;background:linear-gradient(90deg,var(--gold),var(--warm),var(--cyan),var(--warm2))}
.letter-nav{display:flex;flex-wrap:wrap;gap:10px;padding:18px}.letter-nav a,.letter-nav button{display:inline-block;padding:8px 12px;border-radius:999px;border:1px solid rgba(127,214,255,.18);background:linear-gradient(180deg, rgba(213,168,108,.12), rgba(217,139,115,.09));color:#eed7a6}.letter-nav .active{outline:2px solid rgba(127,214,255,.4);color:#fff}
.controls{display:grid;grid-template-columns:minmax(0,1.6fr) .8fr auto auto auto;gap:12px;padding:18px;align-items:center} input,select,button{border-radius:14px;border:1px solid rgba(127,214,255,.2);background:#161828;color:var(--text);padding:12px 14px;font-size:15px} button{cursor:pointer} button:hover{background:#2a2230}
.stats{display:flex;gap:10px;flex-wrap:wrap;padding:0 18px 12px} .badge{display:inline-block;padding:6px 10px;border:1px solid rgba(201,169,106,.35);border-radius:999px;color:#eed7a6;background:linear-gradient(180deg, rgba(213,168,108,.12), rgba(217,139,115,.09))}
.table-wrap{overflow:auto;padding:18px} table{width:100%;border-collapse:collapse;min-width:980px;table-layout:fixed} thead th{text-align:left;padding:16px;background:linear-gradient(180deg,rgba(213,168,108,.18),rgba(217,139,115,.12),rgba(127,214,255,.08));border-bottom:1px solid rgba(127,214,255,.25);position:sticky;top:0} tbody td{padding:16px;border-bottom:1px solid rgba(127,214,255,.12);vertical-align:top;line-height:1.8;word-break:break-word} tbody tr:nth-child(odd){background:rgba(255,255,255,.02)} tbody tr:hover{background:linear-gradient(90deg, rgba(127,214,255,.08), rgba(217,139,115,.08))} td:nth-child(1){font-weight:700;color:var(--cyan);width:23%} td:nth-child(2){color:#f2d2b1;width:18%} td:nth-child(3){width:59%}
.pagination{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:0 18px 22px;flex-wrap:wrap} .pager{display:flex;gap:10px;align-items:center;flex-wrap:wrap} .page-indicator{color:var(--muted)} .footer{padding-top:20px;padding-bottom:56px;color:#a69592;font-size:14px} .note{padding:0 18px 18px;color:var(--muted);line-height:1.8} .loading{padding:18px;color:var(--warm2)} .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:14px;padding:18px}.grid a{padding:16px;border-radius:18px;border:1px solid rgba(127,214,255,.14);background:rgba(255,255,255,.03)} .grid a strong{display:block;color:var(--cyan);font-size:22px;margin-bottom:8px}
.source-link{display:inline-flex;align-items:center;gap:6px;margin-left:10px;padding:2px 9px;border-radius:999px;border:1px solid rgba(127,214,255,.2);font-size:13px;line-height:1.4;color:#eed7a6;background:linear-gradient(180deg, rgba(127,214,255,.12), rgba(217,139,115,.08))}.source-link:hover{color:#fff;border-color:rgba(127,214,255,.42)}
@media (max-width:900px){.header{grid-template-columns:1fr}.header-art{justify-self:start}.controls{grid-template-columns:1fr 1fr 1fr;} .controls input{grid-column:1/-1}}
</style>'''


def nav_links(letters: list[str], active: str, href_builder) -> str:
    parts = []
    for letter in letters:
        cls = ' class="active"' if letter == active else ''
        parts.append(f'<a{cls} href="{href_builder(letter)}">{letter.upper()}</a>')
    return ''.join(parts)


def app_script(data_path: str, cache_key: str) -> str:
    return f'''<script>
const DATA_PATH = {json.dumps(data_path)};
const DATA_CACHE_KEY = {json.dumps(cache_key)};
let glossaryData=[]; let filtered=[]; let searchIndex=[]; let currentPage=1; let pageSize=50; let filterTimer=null;
const body=document.getElementById('tableBody');
const matchCount=document.getElementById('matchCount');
const pageIndicator=document.getElementById('pageIndicator');
const searchInput=document.getElementById('searchInput');
const pageSizeSelect=document.getElementById('pageSize');
function escapeHtml(s){{return String(s ?? '').replace(/[&<>"']/g,m=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[m]));}}
function renderDefinition(row){{
  const definition = escapeHtml(row.definition_cht || '');
  const sourceUrl = escapeHtml(row.source_url || '');
  if(!sourceUrl) return definition;
  return `${{definition}}<a class="source-link" href="${{sourceUrl}}" target="_blank" rel="noopener noreferrer">參考來源</a>`;
}}
function buildSearchIndex(){{
  searchIndex = glossaryData.map(row => (`${{row.english || ''}}\n${{row.traditional_chinese || ''}}\n${{row.definition_cht || ''}}`).toLowerCase());
}}
function render(){{
  const totalPages=Math.max(1,Math.ceil(filtered.length/pageSize));
  if(currentPage>totalPages) currentPage=totalPages;
  const start=(currentPage-1)*pageSize;
  const pageRows=filtered.slice(start,start+pageSize);
  body.innerHTML=pageRows.length
    ? pageRows.map(r=>`<tr><td>${{escapeHtml(r.english)}}</td><td>${{escapeHtml(r.traditional_chinese)}}</td><td>${{renderDefinition(r)}}</td></tr>`).join('')
    : '<tr><td colspan="3" class="loading">查無符合條件的術語。</td></tr>';
  matchCount.textContent=`目前顯示：${{filtered.length}} 筆`;
  pageIndicator.textContent=`第 ${{currentPage}} 頁 / 共 ${{totalPages}} 頁`;
}}
function applyFilterNow(){{
  const q=searchInput.value.trim().toLowerCase();
  if(!q){{ filtered=[...glossaryData]; currentPage=1; render(); return; }}
  const matched=[];
  for(let i=0;i<glossaryData.length;i++){{
    if(searchIndex[i] && searchIndex[i].includes(q)) matched.push(glossaryData[i]);
  }}
  filtered=matched;
  currentPage=1;
  render();
}}
function scheduleFilter(){{ clearTimeout(filterTimer); filterTimer=setTimeout(applyFilterNow, 120); }}
function persistCache(text){{ try{{ localStorage.setItem(DATA_CACHE_KEY, text); }}catch(_e){{ }} }}
function readCache(){{ try{{ return localStorage.getItem(DATA_CACHE_KEY); }}catch(_e){{ return null; }} }}
function setData(data){{ glossaryData=Array.isArray(data)?data:[]; buildSearchIndex(); filtered=[...glossaryData]; render(); }}
async function loadData(){{
  const cached = readCache();
  if(cached){{
    try{{
      setData(JSON.parse(cached));
      matchCount.textContent=`目前顯示：${{filtered.length}} 筆（快取）`;
    }}catch(_e){{ }}
  }}
  try{{
    const response = await fetch(DATA_PATH, {{cache:'force-cache'}});
    const text = await response.text();
    persistCache(text);
    setData(JSON.parse(text));
  }}catch(err){{
    if(!glossaryData.length){{
      body.innerHTML='<tr><td colspan="3" class="loading">資料載入失敗，請稍後再試。</td></tr>';
      matchCount.textContent='載入失敗';
    }}
    console.error(err);
  }}
}}
searchInput.addEventListener('input', scheduleFilter);
pageSizeSelect.addEventListener('change',()=>{{pageSize=Number(pageSizeSelect.value); currentPage=1; render();}});
document.getElementById('resetBtn').addEventListener('click',()=>{{searchInput.value=''; applyFilterNow();}});
document.getElementById('prevBtn').addEventListener('click',()=>{{if(currentPage>1){{currentPage--; render();}}}});
document.getElementById('nextBtn').addEventListener('click',()=>{{const totalPages=Math.max(1,Math.ceil(filtered.length/pageSize)); if(currentPage<totalPages){{currentPage++; render();}}}});
document.getElementById('firstBtn').addEventListener('click',()=>{{currentPage=1; render();}});
document.getElementById('lastBtn').addEventListener('click',()=>{{currentPage=Math.max(1,Math.ceil(filtered.length/pageSize)); render();}});
loadData();
</script>'''


def build_index_html(letters: list[str], counts: dict[str, int]) -> str:
    grid = ''.join(
        f'<a href="letters/{letter}.html"><strong>{letter.upper()}</strong><span>{counts[letter]} 筆術語</span></a>'
        for letter in letters
    )
    return f'''<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>{SITE_TITLE}｜{SITE_SUBTITLE}</title>{common_head()}</head><body>
<div class="header"><div class="header-text"><div class="kicker">MET TERM · 氣象術語整理</div><h1>{SITE_TITLE}<br><span style="font-size:26px;font-weight:500;color:#f2d2b1;letter-spacing:.04em">{SITE_SUBTITLE}</span></h1><div class="sub">{SITE_DESC}</div></div><div class="header-art"><img src="cloud_claw.png" alt="cloud claw"></div></div>
<div class="wrap"><div class="card"><div class="hero-band"></div><div class="letter-nav"><a class="active" href="index.html">首頁</a><a href="all.html">全部</a>{''.join(f'<a href="letters/{l}.html">{l.upper()}</a>' for l in letters)}</div><div class="grid">{grid}</div><div class="note">首頁維持字母入口架構，避免一次載入全站 9,431 筆資料；若進入單字母頁，只會讀取該字母 JSON，搜尋與翻頁會更輕、更穩定。</div></div></div><div class="footer">Built for met_term · {BUILD_DATE} · Editor: CEO CLAW</div></body></html>'''


def build_table_page(title: str, dataset_label: str, total_count: int, note: str, nav_prefix: str, active_top: str, letters: list[str], data_path: str, cache_key: str, cloud_path: str, search_placeholder: str) -> str:
    top_home_cls = ' class="active"' if active_top == 'home' else ''
    top_all_cls = ' class="active"' if active_top == 'all' else ''
    href_builder = (lambda letter: f'letters/{letter}.html') if nav_prefix == '' else (lambda letter: f'{letter}.html')
    letter_nav = nav_links(letters, active_top if len(active_top) == 1 else '', href_builder=href_builder)
    return f'''<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>{SITE_TITLE}｜{title}</title>{common_head()}</head><body><div class="header"><div class="header-text"><div class="kicker">MET TERM · 氣象術語整理</div><h1>{SITE_TITLE}<br><span style="font-size:26px;font-weight:500;color:#f2d2b1;letter-spacing:.04em">{SITE_SUBTITLE}</span></h1><div class="sub">{SITE_DESC}</div></div><div class="header-art"><img src="{cloud_path}" alt="cloud claw"></div></div><div class="wrap"><div class="card"><div class="hero-band"></div><div class="letter-nav"><a{top_home_cls} href="{nav_prefix}index.html">首頁</a><a{top_all_cls} href="{nav_prefix}all.html">全部</a>{letter_nav}</div><div class="controls"><input id="searchInput" type="text" placeholder="{search_placeholder}"><select id="pageSize"><option value="20">每頁 20 筆</option><option value="50" selected>每頁 50 筆</option><option value="100">每頁 100 筆</option></select><button id="resetBtn">清除搜尋</button><button id="prevBtn">上一頁</button><button id="nextBtn">下一頁</button></div><div class="stats"><span class="badge">資料集：{dataset_label}</span><span class="badge">整合術語總數：{total_count}</span><span class="badge" id="matchCount">載入中…</span></div><div class="table-wrap"><table><thead><tr><th>English term</th><th>繁體中文</th><th>名詞解釋</th></tr></thead><tbody id="tableBody"><tr><td colspan="3" class="loading">正在載入術語資料…</td></tr></tbody></table></div><div class="pagination"><div class="page-indicator" id="pageIndicator">第 1 頁 / 共 1 頁</div><div class="pager"><button id="firstBtn">第一頁</button><button id="lastBtn">最後一頁</button></div></div><div class="note">{note}</div></div></div><div class="footer">Built for met_term · {BUILD_DATE} · Editor: CEO CLAW</div>{app_script(data_path, cache_key)}</body></html>'''


def main():
    letters = letters_available()
    counts = {}
    all_rows = []

    for letter in letters:
        path = DATA_DIR / f'{letter}_terms_all_cht.json'
        rows = [normalize_row(row) for row in load_json(path)]
        counts[letter] = len(rows)
        all_rows.extend(rows)
        dump_json(path, rows)

    dump_json(DATA_DIR / 'glossary_all_cht.json', all_rows)
    dump_json(DATA_DIR / 'glossary_manifest.json', {
        'build_date': BUILD_DATE,
        'total_terms': len(all_rows),
        'letters': [
            {'letter': letter, 'count': counts[letter], 'data_path': f'data/{letter}_terms_all_cht.json'}
            for letter in letters
        ],
    })

    (REPO / 'index.html').write_text(build_index_html(letters, counts), encoding='utf-8')
    (REPO / 'all.html').write_text(
        build_table_page(
            title='全部術語',
            dataset_label='全部',
            total_count=len(all_rows),
            note='全部頁面保留給需要全站檢索的人使用；本站現在在瀏覽端預先建立搜尋索引、加入輸入防抖，並使用 localStorage 快取已下載 JSON，以減輕 9,431 筆資料的再次開啟與搜尋負擔。',
            nav_prefix='',
            active_top='all',
            letters=letters,
            data_path='data/glossary_all_cht.json',
            cache_key=f'met_term:data:all:{BUILD_DATE}:{len(all_rows)}',
            cloud_path='cloud_claw.png',
            search_placeholder='搜尋英文、繁中或解釋',
        ),
        encoding='utf-8',
    )

    for letter in letters:
        (LETTERS_DIR / f'{letter}.html').write_text(
            build_table_page(
                title=f'{letter.upper()} 字術語',
                dataset_label=letter.upper(),
                total_count=counts[letter],
                note=f'此頁只載入 {letter.upper()} 字術語 JSON，並在瀏覽端建立一次性搜尋索引；定義後方附上可另開新分頁的「參考來源」連結，指向對應的 AMS Glossary 詞條網址。',
                nav_prefix='../',
                active_top=letter,
                letters=letters,
                data_path=f'../data/{letter}_terms_all_cht.json',
                cache_key=f'met_term:data:{letter}:{BUILD_DATE}:{counts[letter]}',
                cloud_path='../cloud_claw.png',
                search_placeholder=f'搜尋 {letter.upper()} 字術語的英文、繁中或解釋',
            ),
            encoding='utf-8',
        )


if __name__ == '__main__':
    main()
