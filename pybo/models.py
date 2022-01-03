from pybo import db




'''
Question, Answer 모델 변경하기 다대다 관계
하나의 질문에 여러명 추천, 한 명이 여러개의 질문에 추천
'''
#다대다 관계
question_voter = db.Table(
    'question_voter',
    db.Column('user_id',db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('question_id', db.Integer, db.ForeignKey('question.id',ondelete='CASCADE' ), primary_key=True)
)


answer_voter = db.Table(
    'answer_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id',ondelete='CASCADE'), primary_key=True),
    db.Column('answer_id',db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), primary_key=True)
)






# 작성자
# user_id필드는 User모델 데이터의 id값을 Question 모델에 포함시키기 위한 것이다.
# user 필드는 Question 모델에서 User 모델을 참조하기 위한 필드이다. db.relationship 함수로 필드를 추가함
# question.user.username 처럼 Question 모델 객체 question을 통해 User 모델 데이터를 추가했다.
# db.relationship 함수의 backref 매개변수는 User 모델 데이터를 통해 Question 모델데이터 참조를 위함, 질문을 여러개 작성했을 때
# 나중에 자신이 작성한 질문을 user.question_set으로 참조할 수 있음

'''
필드의 기본값은 default와 server_default를 사용해서 설정할수 있다. 
그런데 server_default와 default에는 어떤 차이가 있을까? 
server_default를 사용하면 flask db upgrade 명령을 수행할 때 필드를 갖고 있지 않던 기존 데이터에도 기본값이 저장된다. 
하지만 default는 새로 생성되는 데이터에만 기본값을 생성해 준다. 
따라서 현재처럼 "없던 필드를 만들어야 하는 상황"에서는 default 대신 server_default를 사용해야 한다.

nullable=True, server_default='1' 첫 지정 후 다시 nullable=False 설정, server_default 삭제
기본값을 먼저 지정후 not nullable 설정해줘야 됨
'''
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False) #nullable=False는 널을 허용하지 않음
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('question_set'))
    modify_date = db.Column(db.DateTime(),nullable=True)
    #secondary속성이 존재하고, voter가 다대다관계이고 question_voter 테이블 참조함
    voter = db.relationship('User', secondary=question_voter, backref=db.backref('question_voter_set'))
    



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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user=db.relationship('User', backref=db.backref('answer_set'))
    modify_date = db.Column(db.DateTime(), nullable=True)
    voter = db.relationship('User',secondary=answer_voter,backref=db.backref('answer_voter_set'))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)



class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=True)
    user = db.relationship('User', backref=db.backref('comment_set'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    modify_date = db.Column(db.DateTime)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id',ondelete='CASCADE'), nullable=True)
    question = db.relationship('Question',backref=db.backref('comment_set'))
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id',ondelete='CASCADE'),nullable=True)
    answer = db.relationship('Answer',backref=db.backref('comment_set'))


