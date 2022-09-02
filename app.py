from pickle import FALSE
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user, user_accessed
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from email import message
from urllib import response
from flask import Flask, render_template, jsonify, request, redirect, url_for

from flask_cors import CORS
from chat import searching
from sqlalchemy import true
import subprocess

subprocess.call("chat.py", shell=True) 
app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/pfa'
app.config['SECRET_KEY'] = 'thisisasecretkey'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(20), nullable=False, unique=True)
    prenom = db.Column(db.String(20), nullable=False, unique=True)
    telephone = db.Column(db.Integer, nullable=False, unique=True)
    adresse = db.Column(db.String(20), nullable=False, unique=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

class Compte(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, nullable=False, unique=True)
    solde = db.Column(db.String(20), nullable=False, unique=True)
    date_d_ouverture = db.Column(db.String(20), nullable=False, unique=True)
   
class Transaction(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    id_compte = db.Column(db.Integer, nullable=False, unique=True)
    id_dest = db.Column(db.Integer, nullable=False, unique=True)
    solde = db.Column(db.String(20), nullable=False, unique=True)
    date_transaction = db.Column(db.String(20), nullable=False, unique=True)


class RegisterForm(FlaskForm):
    nom = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Nom"})
    prenom = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Prenom"})
    telephone = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Telephone"})
    adresse = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Adresse"})
  
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    
    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[ InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')
    
data=[]
from function import news1, news2, news3

@app.route('/')
def index():
    list=news1()
    list2=news2()
    list3=news3()
    return render_template('index.html',value1=list[0].text,value2=list[1].text,value3=list2[0].text,value4=list2[1].text,value5=list3[0].text,value6=list3[1].text)
import json
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.password == form.password.data:
                login_user(user)
                id_user=User.query.filter_by(username=user.username).first()
                Solde=Compte.query.filter_by(id_user=id_user.id).first()
                transfer=Transaction.query.filter_by(id=id_user.id).first()
                destinataire_trans=User.query.filter_by(id=transfer.id_dest).first()
                data={"username": user.username,"password" : user.password,"solde" : Solde.solde,"transfer_amount":transfer.solde,"transfer_destinataire":destinataire_trans.username,"transfer_date":str(transfer.date_transaction)}
                with open("user.json", "w") as out_file:
                    json.dump(data, out_file, indent = 6,separators=(',',': '))
                return render_template('dashboard.html', user = user)
            else :
                print("no")
    return render_template('login.html', form=form)

print(data)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    list=news1()
    list2=news2()
    list3=news3()
    return render_template('dashboard.html',value1=list[0].text,value2=list[1].text,value3=list2[0].text,value4=list2[1].text,value5=list3[0].text,value6=list3[1].text)
@app.route('/', methods=['GET', 'POST'])
@login_required
def logout():
    list=news1()
    list2=news2()
    list3=news3()
    return render_template('index.html',value1=list[0].text,value2=list[1].text,value3=list2[0].text,value4=list2[1].text,value5=list3[0].text,value6=list3[1].text)

@ app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
      #  hashed_password = bcrypt.generate_password_hash(form.password.data)
        hashed_password = form.password.data
        new_user = User(
            nom=form.nom.data,
            prenom=form.prenom.data,
            telephone=form.telephone.data,
            adresse=form.adresse.data,
            username=form.username.data,
            password=hashed_password
            )
  
        db.session.add(new_user)
        db.session.commit()

        user = User.query.filter_by(username=form.username.data).first()

        new_compte = Compte(
           id_user = user.id,

        )
        return redirect(url_for('login'))

    return render_template('register.html', form=form)
from flask_login import current_user

def your_route():
    return current_user.is_authenticated
x=False
@app.post('/predict')
def predict():
    import subprocess
    your_route()
    if current_user.is_authenticated:
        x=True
    else:
        x=False
    subprocess.call("chat.py", shell=True)
    from function import Gsearch
    while True:
        text=request.get_json().get("message")
        response=searching(text,x)
        message ={"answer":response}
        return jsonify(message)
if __name__ == "__main__":
    app.run(debug=True, port=5000)