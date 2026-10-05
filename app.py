import streamlit as st,sqlite3
from pathlib import Path
from src.crawler import crawl
from src.database import init_db,seed_previous_change_history,connect
st.set_page_config(page_title='Atlas Scholarship Intelligence',page_icon='🎓',layout='wide')
st.markdown('''<style>.hero{padding:24px;border-radius:18px;background:linear-gradient(135deg,#10182f,#172554);border:1px solid #29375f}.muted{color:#94a3b8;font-size:13px}</style>''',unsafe_allow_html=True)
init_db();seed_previous_change_history()
st.markdown('<div class="hero"><h1>🎓 Atlas Scholarship Intelligence</h1><div class="muted">Trust-first crawler • primary-source verification • evidence ledger • change detection</div></div>',unsafe_allow_html=True)
with st.sidebar:
 st.header('Crawler Controls')
 if st.button('▶ Run crawler',use_container_width=True):
  with st.spinner('Discovering and reconciling scholarship sources...'): st.session_state['run']=crawl()
  st.success('Crawl completed')
 st.caption('Free stack: Python · Requests · BeautifulSoup · SQLite · Streamlit')
 st.caption('If a live source is unreachable, the app uses the packaged primary-source verification cache and never invents values.')
c=connect(); rows=c.execute('SELECT * FROM scholarships ORDER BY confidence DESC,scholarship_name').fetchall(); changes=c.execute('SELECT * FROM change_history ORDER BY detected_at DESC').fetchall(); c.close()
total=len(rows); ver=sum(r['verification_status']=='VERIFIED' for r in rows); rev=total-ver; act=sum(r['current_status']=='ACTIVE' for r in rows); exp=sum(r['current_status']=='EXPIRED' for r in rows); avg=sum(r['confidence'] for r in rows)/total if total else 0
cols=st.columns(6)
for col,label,val in zip(cols,['Total discovered','Verified','Review required','Active','Expired','Avg confidence'],[total,ver,rev,act,exp,f'{avg:.1f}%']):col.metric(label,val)
st.subheader('Scholarship repository'); q=st.text_input('Search by scholarship, provider, category or source type')
view=[r for r in rows if q.lower() in ' '.join(str(r[k]) for k in ['scholarship_name','provider','source_type','eligibility','current_status']).lower()]
st.dataframe([{'Scholarship':r['scholarship_name'],'Provider':r['provider'],'Source':r['source_type'],'Deadline':r['closing_date'],'Status':r['current_status'],'Verification':r['verification_status'],'Confidence':f"{r['confidence']:.0f}%"} for r in view],use_container_width=True,hide_index=True)
st.subheader('Scholarship details')
if view:
 sel=st.selectbox('Select record',[r['scholarship_name'] for r in view]); r=next(x for x in view if x['scholarship_name']==sel)
 st.markdown(f'### {r["scholarship_name"]}'); a,b,d=st.columns(3); a.write('**Provider**');a.write(r['provider']);b.write('**Status**');b.write(r['current_status']);d.write('**Confidence**');d.write(f"{r['confidence']:.0f}%")
 for k,label in [('amount','Amount'),('eligibility','Eligibility'),('academic_requirements','Academic requirements'),('education_level','Education level'),('income_criteria','Income criteria'),('category_criteria','Category'),('opening_date','Opening date'),('closing_date','Closing date'),('documents_required','Documents'),('selection_process','Selection process'),('renewal_requirements','Renewal')]:st.write(f'**{label}:**',r[k])
 st.info('Why this score: deterministic evidence rule; official source + retained route + identity + evidence + verification timestamp + deadline/status/source classification. No LLM-generated confidence.')
 st.write('**Evidence:**',r['evidence']); st.write('**Last verified:**',r['last_verified']); st.link_button('Official source',r['official_source_url']); st.link_button('Application / portal',r['application_url'])
st.subheader('Change detection'); st.caption('Two documented 2026 deadline extensions are retained instead of overwritten.')
st.dataframe([{'Scholarship':next((r['scholarship_name'] for r in rows if r['scholarship_id']==x['scholarship_id']),x['scholarship_id']),'Field':x['field_name'],'Old':x['old_value'],'New':x['new_value'],'Detected':x['detected_at'],'Kind':x['change_kind']} for x in changes],use_container_width=True,hide_index=True)
st.subheader('Verification policy'); st.write('VERIFIED requires confidence ≥95%. Missing facts are recorded as Not specified rather than guessed. Aggregators are never treated as authoritative.')
