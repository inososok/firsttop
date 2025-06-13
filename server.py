import json

from flask import Flask, render_template, redirect, request, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from data import db_session
from data.users import User
from data.scores import Scores
from data.games import Game
from data.investments import Investment
from data.investuser import InvestUser

from forms.login import LoginForm
from forms.register import RegisterForm

chance = 0
app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'
db_session.global_init("db/mydatabase.db")
login_manager = LoginManager()
login_manager.init_app(app)
def delayed_command():
    time.sleep(2)
    chance = random(0,1)
    cost = cost * random(0,100) // 100
def main():
    thread = threading.Thread(target=delayed_command, args=(3, "Выполнить команду"))
    thread.start()
    @login_manager.user_loader
    def load_user(user_id):
        db_sess = db_session.create_session()
        return db_sess.query(User).get(user_id)
    
    
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect("/")
    
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.email == form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect("/")
            return render_template('login.html',
                                   message="Неправильный логин или пароль",
                                   form=form)
        return render_template('login.html', form=form)
    
    
    @app.route("/")
    def index():
        return render_template("index.html")
    
    
    @app.route("/game1", methods=['GET', 'POST'])
    def play():
        if request.method == 'GET':
            return render_template('game1.html')
        elif request.method == 'POST':
            # счет
            score = int(request.form.get('data', 0))
            db_sess = db_session.create_session()
            gameid = db_sess.query(Game).filter(Game.title == "Flappy Coin").first()
            if gameid:
                sc = db_sess.query(Scores).filter(Scores.userid == current_user.id,
                                                  Scores.gamesid == gameid.id).first()
                if sc:
                    sc.bestscore = max(score, sc.bestscore)
                    db_sess.commit()
                else:
                    new_score = Scores(userid=current_user.id, gamesid=gameid.id,
                                       bestscore=score)
                    db_sess.add(new_score)
                    db_sess.commit()
            user = db_sess.query(User).filter(User.id == current_user.id).first()
            user.coins = user.coins + score
            db_sess.commit()
            return 'ok'
    
    
    @app.route('/shop')
    def invest():
        return render_template('shop.html')
    
    
    @app.route('/shop/investment/<int:id>')
    def buy(id):
        db_sess = db_session.create_session()
        inst = db_sess.query(Investment).filter(Investment.id == id).first()
        if inst:
            sc = db_sess.query(InvestUser).filter(InvestUser.userid == current_user.id,
                                                  InvestUser.investmentsid == inst.id).first()
            if sc:
                sc.amount = sc.amount + 1
                db_sess.commit()
            else:
                new_score = InvestUser(userid=current_user.id, investmentsid=inst.id,
                                       amount=1)
                db_sess.add(new_score)
                db_sess.commit()
        return render_template('shop.html')
    
    
    @app.route('/register', methods=['GET', 'POST'])
    def reqister():
        form = RegisterForm()
        if form.validate_on_submit():
            if form.password.data != form.password_repeat.data:
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Пароли не совпадают")
            db_sess = db_session.create_session()
            if db_sess.query(User).filter(User.email == form.email.data).first():
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Такой пользователь уже есть")
            user = User(
                surname=form.surname.data,
                name=form.name.data,
                email=form.email.data
            )
            user.set_password(form.password.data)
            db_sess.add(user)
            db_sess.commit()
            return redirect('/login')
        return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
