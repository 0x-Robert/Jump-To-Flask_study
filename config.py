import os

BASE_DIR = os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI='sqlite:///{}'.format(os.path.join(BASE_DIR,'pybo.db'))
SQLALCHEMY_TRACK_MODIFICATIONS=False
#Flask-WTF를 사용하려면 플라스크 환경변수 SECRET_KEY가 필요함 SECRET_KEY는 CSRF(cross-site request forgery)라는 웹사이트 취약점 공격을 방지하는 데 사용된다.
#CSRF는 사용자의 요청을 위조하는 웹사이트 공격기법인데 SECRET_KEY를 기반으로 생성되는 CSRF토큰은 폼으로 전송된 데이터가 실제 웹페이지에서 작성된 데이터인지
#판단해주는 가늠자 역활을 함 , 실제 운영환경에서는 dev키는 쓰면 안됨
#SECRET_KEY="dev"
SECRET_KEY=b'\x9f}\xe7\x85\xee\xcc\r.2g\xa8\xf0?\xd0\t\xd9'
