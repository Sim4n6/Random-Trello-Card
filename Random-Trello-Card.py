import json
from trello import TrelloClient
import random
from flask import Flask, render_template, request
import requests
import os

# My TRELLO API KEYs
TRELLO_APP_KEY = os.environ['TRELLO_APP_KEY'] # OK

TRELLO_USER_TOKEN = os.environ['TRELLO_USER_TOKEN']
TRELLO_API_SECRET = os.environ['TRELLO_API_SECRET']

client_trello = TrelloClient(
	api_key=TRELLO_APP_KEY,
	api_secret=TRELLO_API_SECRET,
	token=TRELLO_USER_TOKEN,
	token_secret='your-oauth-token-secret'
)

app = Flask(__name__)


def get_random_trello_card():
	""" Get a random card from Trello : Board (TODOS) --> LIST (0)"""

	# list trello boards
	lst_boards = client_trello.list_boards()

	# list of the TODOS Boards
	todos_board = lst_boards[1]
	lst_brd_lists = todos_board.list_lists()

	# list cards of TODOS board
	todos_lst_cards = lst_brd_lists[0]
	lst_cards = todos_lst_cards.list_cards()

	# Generate a random card of the list
	random_card = random.choice(lst_cards)

	return random_card


@app.route("/random")
def random():
	"""  Render an html page containing the link to the random card from to-do list """

	# Get Random Trello Card :
	random_card = get_random_trello_card()

	# render a template with random_card details
	return render_template("random_card.html", random_card=random_card)


@app.route("/")
@app.route("/index")
def index():

	api = dict()
	api["name"] = "Connect button"
	api["url"] = "https://trello.com/1/authorize?expiration=never&name=RandomCard&scope=read&return_url=https://random-trello-card.herokuapp.com/return_url&response_type=token&key=" + TRELLO_APP_KEY
	return render_template("index.html", api=api)


@app.route("/return_url", methods=['POST', 'GET'])
def returned_token():

	print("--->", request.method)
	return random()


if __name__ == '__main__':
	app.config['ENV'] = "development"
	app.run(debug=True)
