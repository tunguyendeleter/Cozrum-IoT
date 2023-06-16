import os
from dotenv import load_dotenv

load_dotenv()
secret_key=os.environ.get('KEY')
SQLACHA=os.environ.get('database_url')
SQL_track=True
