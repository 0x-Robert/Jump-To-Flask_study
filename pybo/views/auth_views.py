from flask import Blueprint, url_for,render_template,flash, request
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import UserCreateForm
from pybo.models import User

#회원가입,로그인,로그아웃 구현을 위함

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/signup', methods=('GET','POST'))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User(username=form.username.data,
                        password=generate_password_hash(form.password1.data)
                        email=form.email.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            #flash는 필드 자체 오류가 아닌 프로그램 논리 오류를 발생시키는 함수이다.
            flash('이미 존재하는 사용자입니다.')

    return render_template('auth/signup.html', form=form)

