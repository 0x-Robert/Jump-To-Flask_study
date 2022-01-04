from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flasktext.markdown import Markdown

import config

#플라스크 ORM에서 정상적으로 사용하기위해 sqlite 디비에서 사용하는 인덱스 등의제약조건 이름은 MetaDATA클래스를 사용해서 정의를 해줘야한다.
naming_convention={
    "ix" : "ix_%(column_0_label)s",
    "uq" : "uq_%(table_name)s_%(column_0_name)s",
    "ck" : "ck_%(table_name)s_%(column_0_name)s",
    "fk" : "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk" : "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()



def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    #Mark down
    Markdown(app,extensions=['n12br','fenced_code'])

    #ORM
    db.init_app(app)

    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app,db)
    from . import models


    #블루 프린트
    from .views import main_views, question_views, answer_views, auth_views,comment_views , vote_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(comment_views.bp)
    app.register_blueprint(vote_views.bp)


    #필터
    from .filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime

    return app




# db 초기화는 flask db init
# 명령어	설명
# flask db migrate	모델을 새로 생성하거나 변경할 때 사용 (실행하면 작업파일이 생성된다.)
# flask db upgrade	모델의 변경 내용을 실제 데이터베이스에 적용할 때 사용 (위에서 생성된 작업파일을 실행하여 데이터베이스를 변경한다.)
# 이 밖에도 여러 명령이 있지만 특별한 경우가 아니라면 이 2가지 명령어를 주로 사용할 것이다. 명령어 종류를 확인하고 싶다면 명령 프롬프트에서 flask db 명령을 입력하자.
