from flask import Blueprint, url_for,render_template,flash, request,session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect


from pybo import db
from pybo.forms import UserCreateForm,UserLoginForm
from pybo.models import User

import functools

#회원가입,로그인,로그아웃 구현을 위함

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/signup', methods=('GET','POST'))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User(username=form.username.data,
                        password=generate_password_hash(form.password1.data),
                        email=form.email.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            #flash는 필드 자체 오류가 아닌 프로그램 논리 오류를 발생시키는 함수이다.
            flash('이미 존재하는 사용자입니다.')

    return render_template('auth/signup.html', form=form)



@bp.route('/login/', methods=('GET','POST'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            error = '존재하지 않는 사용자입니다.'
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('main.index'))
        flash(error)
    return render_template('auth/login.html',form=form)


#@bp.before_app_request 애너테이션은 라우트함수보다 먼저 실행된다. 앞으로 load_logged_in_user 함수는 모든 라우트 함수보다 먼저 실행될 것이다., 플라스크에서 먼저 실행됨
#g는 플라스크가 제공하는 컨텍스트 변수이다. 이 변수는 request 변수와 마찬가지로 요청->응답 과정에서 유효하다.
#session 변수에 user_id 값이 있으면 디비에서 이를 조회하여 g.user에 저장한다.
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    print("user_id : ",user_id)

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)
    print("g.user : ",g.user)
    print("g : ",g)

@bp.route('/logout/')
def logout():
    #세션의 모든 값을 삭제함
    print("session",session)
    session.clear()
    return redirect(url_for('main.index'))


#로그아웃 상태에서 질문또는 답변등록하면 에러가 뜬다 이걸 로그인 페이지로 리다이렉트 하기위해 데코레이터 함수를 생성했다.
'''
데코레이터 함수는 기존 함수를 감싸는 방식으로 간단히 만들 수 있음
다른 함수에 @login_required 에너테이션을 지정하면 login_required 데코레이터 함수가 먼저 실행된다.
login_required 함수는 g.user가 있는지 조사하고 없으면 로그인 URL로 있으면 원래함수를 그대로 실행한다.

'''
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
