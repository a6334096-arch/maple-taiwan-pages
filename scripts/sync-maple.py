"""Copy validated public records; never infer or write foliage observations."""
import json, os, sys, urllib.request
from pathlib import Path
from datetime import datetime
ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://maple-taiwan-responsive.a6334096.chatgpt.site'
def fetch(name):
    req = urllib.request.Request(ORIGIN+'/'+name, headers={'User-Agent':'Mozilla/5.0 MapleDataSync/1.0','Accept':'application/json','Cache-Control':'no-cache'})
    with urllib.request.urlopen(req,timeout=45) as r:
        if 'json' not in r.headers.get('Content-Type',''): raise ValueError('Non-JSON response')
        raw=r.read(2_000_001)
        if len(raw)>2_000_000: raise ValueError('Response too large')
        value=json.loads(raw)
    if not isinstance(value,dict) or value.get('storage_error') or value.get('_storage_error'): raise ValueError('Source storage unavailable')
    return value

def validate(seasons, payload, ids):
    foliage=payload.get('foliage')
    if not isinstance(foliage,dict): raise ValueError('Missing foliage records')
    for ident in ids:
        s=seasons.get(ident)
        if not isinstance(s,dict): raise ValueError('Missing seasonal record: '+ident)
        if s.get('months') is not None and (not isinstance(s['months'],list) or any(type(m)!=int or not 1<=m<=12 for m in s['months'])): raise ValueError('Invalid months: '+ident)
        if ident not in foliage: raise ValueError('Missing foliage id: '+ident)
        f=foliage[ident]
        if f is None: continue
        if not isinstance(f,dict) or type(f.get('status'))!=int or f['status'] not in range(4): raise ValueError('Invalid foliage status: '+ident)
        for key in ['summary','scope','source','source_url','reported_at']:
            if not isinstance(f.get(key),str) or not f[key].strip(): raise ValueError('Missing foliage evidence: '+ident)
        if not f['source_url'].startswith('https://'): raise ValueError('Invalid evidence URL')
        datetime.strptime(f['reported_at'],'%Y-%m-%d')
        if f.get('observed_on'): datetime.strptime(f['observed_on'],'%Y-%m-%d')
    return {k:v for k,v in seasons.items() if k in ids or k=='_sync'}, {**payload,'foliage':{k:foliage[k] for k in ids}}

def main():
    ids={p['id'] for p in json.loads((ROOT/'places.json').read_text())}
    # Read and validate both before touching either local file. Failure keeps old data.
    seasons,foliage=validate(fetch('seasons.json'),fetch('foliage.json'),ids)
    staged=[]
    for name,value in [('seasons.json',seasons),('foliage.json',foliage)]:
        old=json.loads((ROOT/name).read_text())
        if old!=value:
            temp=ROOT/(name+'.pending')
            temp.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
            staged.append((temp,ROOT/name))
    for temp,target in staged: os.replace(temp,target)
    print('Validated',len(ids),'places; changed files:',len(staged))
if __name__=='__main__':
    try: main()
    except Exception as e:
        print('Sync failed; existing data retained:',e,file=sys.stderr)
        sys.exit(1)
