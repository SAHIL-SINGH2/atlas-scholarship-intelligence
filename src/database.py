import sqlite3,json
from .config import DB_PATH,OUTPUT_DIR,DATA_DIR
def connect():
 OUTPUT_DIR.mkdir(exist_ok=True); c=sqlite3.connect(DB_PATH); c.row_factory=sqlite3.Row; return c
def init_db():
 c=connect(); c.executescript('''CREATE TABLE IF NOT EXISTS scholarships(scholarship_id TEXT PRIMARY KEY,scholarship_name TEXT,provider TEXT,source_type TEXT,official_source_url TEXT,application_url TEXT,amount TEXT,eligibility TEXT,academic_requirements TEXT,education_level TEXT,income_criteria TEXT,age_criteria TEXT,gender_criteria TEXT,category_criteria TEXT,domicile_state TEXT,institution_requirements TEXT,opening_date TEXT,closing_date TEXT,documents_required TEXT,selection_process TEXT,renewal_requirements TEXT,current_status TEXT,confidence REAL,verification_status TEXT,last_verified TEXT,evidence TEXT,evidence_url TEXT,discovery_method TEXT,content_hash TEXT,updated_at TEXT);CREATE TABLE IF NOT EXISTS change_history(id INTEGER PRIMARY KEY AUTOINCREMENT,scholarship_id TEXT,field_name TEXT,old_value TEXT,new_value TEXT,detected_at TEXT,source_url TEXT,evidence TEXT,change_kind TEXT);CREATE TABLE IF NOT EXISTS crawl_runs(id INTEGER PRIMARY KEY AUTOINCREMENT,started_at TEXT,finished_at TEXT,discovered INTEGER,verified INTEGER,review_required INTEGER,changed INTEGER,notes TEXT);'''); c.commit(); c.close()
def seed_previous_change_history():
 c=connect()
 if c.execute('SELECT COUNT(*) FROM change_history').fetchone()[0]==0:
  prev=json.loads((DATA_DIR/'previous_snapshots.json').read_text()); cur=json.loads((DATA_DIR/'scholarships_verified.json').read_text())['records']
  for sid,p in prev.items():
   r=next(x for x in cur if x['scholarship_id']==sid)
   c.execute('INSERT INTO change_history(scholarship_id,field_name,old_value,new_value,detected_at,source_url,evidence,change_kind) VALUES(?,?,?,?,?,?,?,?)',(sid,'closing_date',p['closing_date'],r['closing_date'],r['last_verified'],r['evidence_url'],r['evidence'],'DOCUMENTED_EXTENSION'))
  c.commit()
 c.close()
def upsert(records,now):
 import hashlib
 c=connect(); changed=[]
 for r in records:
  old=c.execute('SELECT * FROM scholarships WHERE scholarship_id=?',(r['scholarship_id'],)).fetchone()
  if old:
   for f in ['closing_date','current_status','amount','eligibility','official_source_url','application_url']:
    if old[f]!=r[f]:
     c.execute('INSERT INTO change_history(scholarship_id,field_name,old_value,new_value,detected_at,source_url,evidence,change_kind) VALUES(?,?,?,?,?,?,?,?)',(r['scholarship_id'],f,str(old[f]),str(r[f]),now,r['evidence_url'],r['evidence'],'FIELD_CHANGED')); changed.append(r['scholarship_id'])
  h=hashlib.sha256(json.dumps(r,sort_keys=True,ensure_ascii=False).encode()).hexdigest(); cols=list(r)+['content_hash','updated_at']; vals=[r[k] for k in r]+[h,now]
  c.execute(f"INSERT OR REPLACE INTO scholarships({','.join(cols)}) VALUES({','.join('?'*len(cols))})",vals)
 c.commit(); c.close(); return sorted(set(changed))
