from pybo import db

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False) #nullable=False는 널을 허용하지 않음



class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #question_id 속성은 질문 모델과 연결하려고 추가했고 이런 경우 Foreign key를 사용해야한다. question.id는 question테이블의 id값을 의미한다
    #ondelete에 지정한 값은 삭제 연동설정이다. 즉 답변 모델의 question_id 속성은 질문 모델의 id 속성과 연결되며 질문을 삭제하면 답변도 같이 삭제된다.
    question_id=db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    #답변 모델에서 질문모델을 참조하기 위해 추가됐다. 예를 들어 답변 모델 객체에서 질문 모델 객체의 제목을 참조하려면 answer.question.subject 처럼 할 수 있다.
    #이렇게 하려면 속성 추가시 db.relationship을 사용해야 한다.
    #db.relationship에서 첫번째 값은 참조할 모델명이고, 두번 째 backref에 지정한 값은 역참조 설정이다. 역참조란 질문에서 답변을 거꾸로 참조하는 것을 의미한다.

    question=db.relationship('Question',backref=db.backref('answer_set'))
    content = db.Column(db.Text(), nullable=False)
    create_date=db.Column(db.DateTime(), nullable=False)


