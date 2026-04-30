import json
from pathlib import Path
s_path=Path('/home/node/.openclaw/workspace/met_term/data/s_terms_all_cht.json')
g_path=Path('/home/node/.openclaw/workspace/met_term/data/glossary_all_cht.json')
s_arr=json.loads(s_path.read_text())
g_arr=json.loads(g_path.read_text())
s_map={row['english']:row for row in s_arr}
count=0
for row in g_arr:
    eng=row.get('english')
    if eng in s_map:
        src=s_map[eng]
        if row.get('traditional_chinese')!=src.get('traditional_chinese') or row.get('definition_cht')!=src.get('definition_cht'):
            row['traditional_chinese']=src.get('traditional_chinese')
            row['definition_cht']=src.get('definition_cht')
            count+=1
g_path.write_text(json.dumps(g_arr, ensure_ascii=False, indent=2))
print('synced',count)
