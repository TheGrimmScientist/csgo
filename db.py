import postgres
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Game(db.model):
	game_id = db.Column(db.Integer, primary_key=True)
	map_name = db.Column(db.String(80), unique=False, nullable=False)
	team_a_player_1 = db.Column(db.Integer, ForeignKey("User.user_id"), unique=False, nullable=False)
	team_a_player_2 = db.Column(db.Integer, ForeignKey("User.user_id"), unique=False, nullable=False)
	team_a_player_3 = db.Column(db.Integer, ForeignKey("User.user_id"), unique=False, nullable=False)
	team_a_player_4 = db.Column(db.Integer, ForeignKey("User.user_id"), unique=False, nullable=False)
	team_a_player_5 = db.Column(db.Integer, ForeignKey("User.user_id"), unique=False, nullable=False)
	team_b_player_1 = db.Column(db.Integer, ForeignKey("User.user_id"), unique=False, nullable=False)
	team_b_player_2 = db.Column(db.Integer, ForeignKey("User.user_id"), unique=False, nullable=False)
	team_b_player_3 = db.Column(db.Integer, ForeignKey("User.user_id"), unique=False, nullable=False)
	team_b_player_4 = db.Column(db.Integer, ForeignKey("User.user_id"), unique=False, nullable=False)
	team_b_player_5 = db.Column(db.Integer, ForeignKey("User.user_id"), unique=False, nullable=False)


class UserGame(db.model):
	game_id = db.Column(db.Integer, ForeignKey("Match.user_id"), unique=False, nullable=False, primary_key=True)
	user_id = db.Column(db.Integer, ForeignKey("Game.game_id"), unique=False, nullable=False, primary_key=True)
	frags = db.Column(db.Integer, unique=False, nullable=False)
	assists = db.Column(db.Integer, unique=False, nullable=False)
	deaths = db.Column(db.Integer, unique=False, nullable=False)
	bomb_plants = db.Column(db.Integer, unique=False, nullable=False)


class User(db.model):
	user_id = db.Column(db.Integer, primary_key=True)
	user_name = db.Column(db.String(80), nullable=False, unique=False)
	age = db.Column(db.Integer, unique=False, nullable=False)
	gender = db.Column(db.Bool, unique=False)
	location = db.Column(db.String(80), unique=False, nullable=False)
	paid_flag = db.Column(db.Bool, unique=False, nullable=False)


class UserLog(db.model):
	user_id = db.Column(db.Integer, ForeignKey("User.user_id"), primary_key=True)
	date = db.Column(db.DateTime, nullable=False, primary_key=True)
	rank = db.Column(db.String(3), unique=False, nullable=False)

