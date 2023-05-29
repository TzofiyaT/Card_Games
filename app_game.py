from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, LoginForm
from flask_login import LoginManager, login_required, login_user, logout_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
import hashlib
from sqlTrueGame import *
from game_class import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

login_manager = LoginManager()
login_manager.init_app(app)

FILE_NAME = "score.db"
create_sql_file(FILE_NAME)
conn = sqlite3.connect(FILE_NAME, check_same_thread=False)
conn.commit()

games = ["True_Or_False", "Pocker", "Hok", "Kare Kupe"]
choose = ["put", "open_pile"]

the_play = Game()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)


@app.route("/")
@app.route("/login", methods=['POST', 'GET'])
def login():
    form = LoginForm()
    users = User.query.all()
    if form.validate_on_submit():
        if request.method == 'POST':
            hashed_password = hashlib.sha256(form.password.data.encode()).hexdigest()
            # user = db.session.query(User).filter_by(username=form.email.data, password=hashed_password).first()
            for user in users:
                if user.email == form.email.data and user.password == hashed_password:
                    login_user(user)
                    flash('You have been logged in!', 'success')
                    return redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form, user_login=True)


@login_manager.unauthorized_handler     # In unauthorized_handler we have a callback URL
def unauthorized_callback():            # In call back url we can specify where we want to
    flash('You have to login!', 'warning')
    return redirect(url_for('login'))  # redirect the user in my case it is login page!


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/logout", methods=['POST', 'GET'])
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    users = User.query.all()
    if form.validate_on_submit():
        if request.method == 'POST':
            for user in users:
                if user.email == form.email.data:
                    flash(f'Account uncreated for {form.username.data}! Please try with another email', 'warning')
                    return render_template('signup.html', title='Signup', form=form)
            with app.app_context():
                hashed_password = hashlib.sha256(form.password.data.encode()).hexdigest()
                new_user = User(username=form.username.data, password=hashed_password, email=form.email.data)
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('home'))
    return render_template('signup.html', title='Signup', form=form, user_login=True)


@app.route("/home")
@login_required
def home():
    return render_template('home.html', games=games)


@app.route('/True_Or_False', methods=['POST', 'GET'])
def true():
    the_play.deck.restart()
    numbers = ["2 players", "3 players", "4 players"]
    if request.method == 'POST':
        selected_option = request.form.get("players")
        player = 1
        for num in numbers:
            player += 1
            if num == selected_option:
                return redirect(url_for('account_players', num=player))
    return render_template('True_Or_False.html', title='True Or False', numbers=numbers)


@app.route('/two_players/<num>', methods=['POST', 'GET'])
def account_players(num):
    players = ["player 1", "player 2", "player 3", "player 4"]
    players_list = []
    for n in range(int(num)):
        players_list.append(players[n])
    if request.method == 'POST':
        selected_option = request.form.getlist("player")
        for name in selected_option:
            the_play.add_player(name)
        the_play.start(10)
        return redirect(url_for('show_hand'))
    return render_template('account_players.html', players=players_list)


@app.route('/show_hand', methods=['POST', 'GET'])
def show_hand():
    if the_play.winn():
        return redirect(url_for('show_winner'))
    the_play.next_player()
    deal = True
    if not the_play.check_deal():
        deal = False
    names_of_cards = the_play.names_of_cards(the_play.the_player.cards_hand)
    last = the_play.card_said
    return render_template('show_hand.html', deal=deal, cards=names_of_cards, choose=choose, last=last,
                           player=the_play.the_player.name)


@app.route('/take', methods=['POST', 'GET'])
def take():
    the_play.take_card_from_deal(the_play.the_player)
    return redirect(url_for('show_hand'))


@app.route('/put', methods=['GET', 'POST'])
def put():
    names_of_cards = the_play.names_of_cards(the_play.the_player.cards_hand)
    tell = the_play.list_to_choose_the_card_to_say()
    last = the_play.names_of_cards([the_play.last_card])[0]
    if request.method == 'POST':
        selected_option = request.form.get("option")
        selected_option2 = request.form.get("option2")
        if not selected_option or not selected_option2:
            flash(f'Choose card!', 'warning')
            return render_template('put.html', cards=names_of_cards, last=last,
                                   player=the_play.the_player.name, tell=tell)
        idx_card = names_of_cards.index(selected_option)
        idx_say = tell.index(selected_option2)
        the_play.put_card_to_pile(the_play.the_player, idx_card, idx_say)
        return redirect(url_for('show_hand'))
    return render_template('put.html', cards=names_of_cards, last=last,
                           player=the_play.the_player.name, tell=tell)


@app.route('/open_pile', methods=['POST', 'GET'])
def open_pile():
    pile_card = the_play.names_of_cards([the_play.deck.open_card()])
    idx = the_play.players.index(the_play.the_player)
    last_card = the_play.card_said
    if idx == 0:
        idx = len(the_play.players)
    t_o_f = the_play.say_false(the_play.players[idx-1], the_play.the_player)
    if t_o_f:
        player = the_play.the_player.name
    else:
        player = the_play.players[idx-1].name
    return render_template('open_pile.html', pile_card=pile_card[0],
                           last_card=last_card, player=player, tof=t_o_f)


@app.route('/show_winner', methods=['POST', 'GET'])
def show_winner():
    name_winner = the_play.winner.name
    return render_template('show_winner.html', winner=name_winner)


if __name__ == '__main__':
    # # create the tables
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True)

    # data = list(read_from_sql_file(FILE_NAME, "player_name"))
    #     players = []
    #     for i in range(4):
    #         players.append(data[i][0])
    # the_play = TrueOrFalse(players, 4)
    # the_play.start(10)
    # list_to_choose = the_play.game.list_to_choose_the_card_to_say()
    # play(the_play.game.players[0].cards_hand,list_to_choose)
