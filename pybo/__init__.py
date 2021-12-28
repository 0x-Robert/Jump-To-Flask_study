from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


import config

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    #ORM
    db.init_app(app)
    migrate.init_app(app,db)
    from . import models


    #블루 프린트
    from .views import main_views, question_views, answer_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)



    return app




# db 초기화는 flask db init
# 명령어	설명
# flask db migrate	모델을 새로 생성하거나 변경할 때 사용 (실행하면 작업파일이 생성된다.)
# flask db upgrade	모델의 변경 내용을 실제 데이터베이스에 적용할 때 사용 (위에서 생성된 작업파일을 실행하여 데이터베이스를 변경한다.)
# 이 밖에도 여러 명령이 있지만 특별한 경우가 아니라면 이 2가지 명령어를 주로 사용할 것이다. 명령어 종류를 확인하고 싶다면 명령 프롬프트에서 flask db 명령을 입력하자.
