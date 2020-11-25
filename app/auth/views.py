from flask import render_template, redirect, url_for
from . import auth 
from ..models import User
from .forms import LoginForm, RegistrationForm
    # ChangePasswordForm, PasswordResetRequestForm, PasswordResetForm, ChangeEmailForm
from .. import db


@auth.route("/login")
def login():

    return render_template('auth/login.html')



@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data.lower(),
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()


        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


