from src.crawler import crawl
r=crawl(); print('ATLAS SCHOLARSHIP INTELLIGENCE'); print('Discovered records:',len(r['records'])); print('Verified:',r['verified']); print('Review required:',r['review_required']); print('Change records:',r['changed']); print('Live fetch:',r['live']); print('Errors:',r['errors'])
