from config.default import *
from logging.config import dictConfig

SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
        user='dbmasteruser',
        pw='yongyong417',
        url='localhost',
        db='flask_pybo')


#SQL_ALCHEMY_DATABASE_URI='sqlite:///{}'.format(os.path.join(BASE_DIR,'pybo.db'))
SQLALCHEMY_TRACK_MODIFICATIONS=False
# SECRET_KEY=b'Zb3\x81\xdb\xf1\xd9\xd7-Knb\x8eB\xa5\x18'
SECRET_KEY=b'\x9f}\xe7\x85\xee\xcc\r.2g\xa8\xf0?\xd0\t\xd9'



# python -c "import os; print(os.urandom(16))" 명령을 입력하면 무작위로 16자리 바이트 문자열이 출력된다

dictConfig({
     'version':1,
     'formatters': {
         'default' : {
             'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
             }
         },
     'handlers':{
         'file': {
             'level': 'INFO',
             'class' : 'logging.handlers.RotatingFileHandler',
             'filename' : os.path.join(BASE_DIR, 'logs/myproject.log'),
             'maxBytes' : 1024 * 1024 * 5, #MB
             'backupCount' : 5,
             'formatter': 'default',
             },
         },
     'root':{
         'level' : 'INFO',
         'handlers': ['file']
         }
     })

