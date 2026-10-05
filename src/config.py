from pathlib import Path
BASE_DIR=Path(__file__).resolve().parents[1]
DATA_DIR=BASE_DIR/'data'; OUTPUT_DIR=BASE_DIR/'output'; DB_PATH=OUTPUT_DIR/'atlas.db'
SEED_URLS=['https://scholarships.gov.in/All-Scholarships','https://acad.iitb.ac.in/academics/scholarship','https://www.scholarships.reliancefoundation.org/']
