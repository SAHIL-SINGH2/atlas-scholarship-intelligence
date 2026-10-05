import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.change_detection import compare,classify_status
DATA=Path(__file__).resolve().parents[1]/'data/scholarships_verified.json'
def test_20_records(): assert len(json.loads(DATA.read_text())['records'])>=20
def test_3_source_types(): assert len({r['source_type'] for r in json.loads(DATA.read_text())['records']})>=3
def test_10_verified_95():
 rs=json.loads(DATA.read_text())['records']; assert sum(r['confidence']>=95 for r in rs)>=10 and all(r['confidence']>=95 for r in rs if r['verification_status']=='VERIFIED')
def test_no_blank_evidence(): assert all(r['evidence'] and r['official_source_url'] for r in json.loads(DATA.read_text())['records'])
def test_change_detection(): assert any(x['field']=='closing_date' for x in compare({'closing_date':'30-09-2026'},{'closing_date':'31-10-2026'}))
def test_expired():
 from datetime import date
 assert classify_status('30-09-2026',date(2026,10,5))=='EXPIRED'
def test_change_fixtures():
 p=json.loads((Path(__file__).resolve().parents[1]/'data/previous_snapshots.json').read_text()); assert p['national-means-cum-merit-scholarship']['closing_date']=='30-09-2026' and p['financial-assistance-for-education-to-the-wards-of-beedi-cine-iomc-lsdm-workers-pre-matric']['closing_date']=='31-08-2026'
