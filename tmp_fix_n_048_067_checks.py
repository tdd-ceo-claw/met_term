import json, re, urllib.request
from pathlib import Path
UA='Mozilla/5.0'
repl={
'negative isothermal vorticity advection':['https://en.wikipedia.org/api/rest_v1/page/summary/Vorticity','https://en.wikipedia.org/api/rest_v1/page/summary/Advection'],
'nemere':['https://www.erdely7csodaja.ro/en/nemere-mountain-and-balvanyos-resort/','https://en.wikipedia.org/api/rest_v1/page/summary/Local_wind'],
'neper':['https://en.wikipedia.org/api/rest_v1/page/summary/Neper','https://www.merriam-webster.com/dictionary/neper'],
'nephanalysis':['https://en.wikipedia.org/api/rest_v1/page/summary/Nephanalysis','https://en.wikipedia.org/api/rest_v1/page/summary/Cloud'],
'nephcurve':['https://en.wikipedia.org/api/rest_v1/page/summary/Turbidity','https://en.wikipedia.org/api/rest_v1/page/summary/Nephelometry'],
'nephelometer':['https://en.wikipedia.org/api/rest_v1/page/summary/Nephelometer','https://www.merriam-webster.com/dictionary/nephelometer'],
'nephology':['https://en.wikipedia.org/api/rest_v1/page/summary/Nephology','https://www.merriam-webster.com/dictionary/nephology'],
'nephometer':['https://en.wikipedia.org/api/rest_v1/page/summary/Cloud','https://en.wikipedia.org/api/rest_v1/page/summary/Cloud_base'],
'nested grids':['https://en.wikipedia.org/api/rest_v1/page/summary/Numerical_weather_prediction','https://www2.mmm.ucar.edu/wrf/users/wrf_users_guide/build/html/namelist_variables.html'],
'net balance':['https://en.wikipedia.org/api/rest_v1/page/summary/Glacier_mass_balance','https://en.wikipedia.org/api/rest_v1/page/summary/Mass_balance'],
'net pyranometer':['https://en.wikipedia.org/api/rest_v1/page/summary/Net_radiometer','https://en.wikipedia.org/api/rest_v1/page/summary/Pyranometer'],
'net pyrgeometer':['https://en.wikipedia.org/api/rest_v1/page/summary/Net_radiometer','https://en.wikipedia.org/api/rest_v1/page/summary/Pyrgeometer']
}

def fetch(u):
    try:
        req=urllib.request.Request(u,headers={'User-Agent':UA})
        with urllib.request.urlopen(req,timeout=25) as r:
            raw=r.read(4000).decode('utf-8','ignore')
        txt=re.sub(r'<[^>]+>',' ',raw)
        txt=re.sub(r'\s+',' ',txt).strip()
        return {'url':u,'ok':True,'snippet':txt[:320]}
    except Exception as e:
        return {'url':u,'ok':False,'error':str(e)}

path=Path('tmp_n_048_067_checks.json')
arr=json.loads(path.read_text(encoding='utf-8'))
for row in arr:
    eng=row['english']
    if eng in repl:
        row['checks']=[fetch(u) for u in repl[eng]]
path.write_text(json.dumps(arr,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('fixed checks')
