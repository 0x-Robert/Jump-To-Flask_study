from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class QuestionForm(FlaskForm):
    subject = StringField('제목', validators=[DataRequired('제목은 필수입력 항목입니다.')])
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])

class AnswerForm(FlaskForm):
    content = TextAreaField('내용',  validators=[DataRequired('내용은 필수 입력 항목입니다.')])


class UserCreateForm(FlaskForm):
    #username은 검증조건
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    #password1 과 password2 는 패스워드 일치하는지 확인하기위함
    password1 = PasswordField('비밀번호', validators=[
        DataRequired(),EqualTo('password2', '비밀번호가 일치하지 않습니다.') ])
    password2 = PasswordField('비밀번호 확인', validators=[DataRequired()])
    #Email은 해당 형식이 이메일 형식과 같은지 체크
    email = EmailField('이메일', validators=[DataRequired(),Email()])


class UserLoginForm(FlaskForm):
    username=StringField('사용자이름',validators=[DataRequired(), Length(min=3,max=25)])
    password=PasswordField('비밀번호',validators=[DataRequired()])
