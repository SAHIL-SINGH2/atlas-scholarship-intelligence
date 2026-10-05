from urllib.parse import urlparse
def calculate_confidence(r):
 s=0
 h=urlparse(r['official_source_url']).netloc.lower()
 if h.endswith('.gov.in') or h.endswith('.ac.in') or 'reliancefoundation.org' in h:s+=25
 if r.get('application_url'):s+=15
 if r.get('scholarship_name') and r.get('provider'):s+=10
 if r.get('evidence'):s+=15
 if r.get('last_verified'):s+=10
 if r.get('closing_date') not in ('','Not specified',None):s+=10
 if r.get('current_status') in ('ACTIVE','EXPIRED'):s+=5
 if r.get('source_type'):s+=5
 return min(s,100)
def verify(r):
 r['confidence']=calculate_confidence(r); r['verification_status']='VERIFIED' if r['confidence']>=95 else 'REVIEW_REQUIRED'; return r
