from datetime import datetime
from flask import Blueprint, render_template, request, url_for,g, flash
from werkzeug.utils import redirect
from .. import db
from ..forms import QuestionForm, AnswerForm
from pybo.models import Question ,Answer, User

from pybo.views.auth_views import login_required

bp = Blueprint('question', __name__ , url_prefix='/question')


@bp.route('/list/')
def _list():
    #입력 파라미터
    page = request.args.get('page', type=int, default=1) #페이지
    kw = request.args.get('kw', type=str, default='')

    #조회

    question_list = Question.query.order_by(Question.create_date.desc())
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(Answer.question_id, Answer.content, User.username) \
            .join(User, Answer.user_id == User.id).subquery()
        question_list = question_list\
            .join(User)\
            .outerjoin(sub_query, sub_query.c.question_id == Question.id) \
            .filter(Question.subject.ilike(search) | #질문제목
                    Question.content.ilike(search) | #질문내용
                    User.username.ilike(search)    | # 질문작성자 
                    sub_query.c.content.ilike(search) | # 답변내용 
                    sub_query.c.username.ilike(search)  # 답변작성자
                    )\
            .distinct()
    #페이징
    question_list = question_list.paginate(page, per_page=10)
    return render_template('question/question_list.html', question_list=question_list, page=page, kw=kw)


@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm()
    question=Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html',question=question,form=form)



@bp.route('/create/', methods=('GET','POST'))
@login_required
def create():
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit():
        question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now(),user=g.user)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('question/question_form.html',form=form)





@bp.route('/modify/<int:question_id>',methods=('GET','POST'))
@login_required
def modify(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('수정권한이 없습니다.')
        return redirect(url_for('question.detail', question_id=question_id))
    if request.method == 'POST': #POST 요청
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question)
            question.modify_date = datetime.now() #수정일시 저장
            db.session.commit()
            return redirect(url_for('question.detail', question_id=question_id))
    else: #GET요청
        form = QuestionForm(obj=question)
    return render_template('question/question_form.html',form=form)


@bp.route('/delete/<int:question_id>')
@login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('삭제 권한이 없습니다.')
        return redirect(url_for('question.detail', question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question._list'))



'''
서브쿼리 연습함 flask shell 이용

Python 3.7.4 (tags/v3.7.4:e09359112e, Jul  8 2019, 19:29:22) [MSC v.1916 32 bit (Intel)] on win32
App: pybo [development]
Instance: C:\Users\smart\PycharmProjects\myproject\instance
>>> from pybo.models import Question, Answer
>>> Question.query.count()
302
>>> Answer.query.count()
8
>>> Question.query.join(Answer).count()
8
>>> print(Question.query.outerjoin(Answer).count()
... )
304
>>>
>>> print(Question.query.outerjoin(Answer).distinct().count())
302
>>> Question.query.outerjoin(Answer).filter(
...      Question.content.ilike('%파이썬%')
...
...      |Answer.content.ilike('%파이썬%')).distinct().count()



'''