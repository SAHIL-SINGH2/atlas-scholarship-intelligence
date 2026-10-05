def compare(old,new):
 return [{'field':f,'old_value':old.get(f),'new_value':new.get(f)} for f in ['amount','eligibility','opening_date','closing_date','current_status','official_source_url','application_url'] if old.get(f)!=new.get(f)]
def classify_status(closing_date,today):
 from datetime import datetime
 if not closing_date or closing_date=='Not specified': return 'REVIEW_REQUIRED'
 d=datetime.strptime(closing_date,'%d-%m-%Y').date()
 if d<today:return 'EXPIRED'
 if (d-today).days<=14:return 'EXPIRING_SOON'
 return 'ACTIVE'
