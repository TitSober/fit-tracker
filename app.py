
from django.shortcuts import render
from flask import Flask, render_template,url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from flask import redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import  Bcrypt

app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4,max=30)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4,max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError(
            "That Username already exists. Please choose a diffrent one.")

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4,max=30)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4,max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")

    

@app.route('/',methods=['GET','POST'])
def home():
    form = LoginForm()
    return render_template('login.html',form=form)
@app.route('/index',methods=['GET','POST'])
def index():
    return redirect('/')
@app.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()
    return render_template('register.html',form=form)


if __name__ == '__main__':
    app.run(debug=True)




