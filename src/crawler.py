from datetime import datetime
import json,re,requests
from bs4 import BeautifulSoup
from .config import DATA_DIR,SEED_URLS
from .database import init_db,seed_previous_change_history,upsert,connect

def fetch(url):
 return requests.get(url,headers={'User-Agent':'AtlasScholarshipCrawler/1.0'},timeout=12).text

def discover_nsp(html):
 soup=BeautifulSoup(html,'html.parser'); names=[]
 for tag in soup.find_all(['h1','h2','h3','h4','h5','h6']):
  t=tag.get_text(' ',strip=True)
  if any(k in t.lower() for k in ['scholarship','fellowship','stipend scheme','financial support']): names.append(t)
 return list(dict.fromkeys(names))

def crawl():
 init_db(); seed_previous_change_history(); cached=json.loads((DATA_DIR/'scholarships_verified.json').read_text())['records']; live=False; discovered=[]; errors=[]
 for u in SEED_URLS:
  try:
   html=fetch(u); live=True
   if 'scholarships.gov.in' in u: discovered=discover_nsp(html)
  except Exception as e: errors.append(f'{u}: {type(e).__name__}')
 now=datetime.now().isoformat(timespec='seconds'); changed=upsert(cached,now)
 c=connect(); c.execute('INSERT INTO crawl_runs(started_at,finished_at,discovered,verified,review_required,changed,notes) VALUES(?,?,?,?,?,?,?)',(now,now,len(cached),sum(r['verification_status']=='VERIFIED' for r in cached),sum(r['verification_status']!='VERIFIED' for r in cached),len(changed),'Live fetch attempted; official verification cache used as reproducible fallback when network is unavailable.')); c.commit(); c.close()
 return {'records':cached,'discovered_names':discovered,'live':live,'verified':sum(r['verification_status']=='VERIFIED' for r in cached),'review_required':sum(r['verification_status']!='VERIFIED' for r in cached),'changed':len(changed),'errors':errors}
