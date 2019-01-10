import json
from trello import TrelloClient
import random
from flask import Flask, render_template
import requests

# My TRELLO API KEYs
from keys import TRELLO_APP_KEY, TRELLO_USER_TOKEN, TRELLO_API_SECRET

# My POCKET API KEYs
from keys import CONSUMER_KEY, ACCESS_TOKEN

client_trello = TrelloClient(
	api_key=TRELLO_APP_KEY,
	api_secret=TRELLO_API_SECRET,
	token=TRELLO_USER_TOKEN,
	token_secret='your-oauth-token-secret'
)

app = Flask(__name__)


def get_random_pocket():
	""" Get a Random Pocket post """

	# # Retrieve request_token
	# r2 = requests.get('https://getpocket.com/v3/oauth/request?consumer_key=' + consumer_key + '&redirect_uri=MyPocket123:authorizationFinished')
	# code = r2.content
	# request_token = str(code).split("=")[1].strip("'")
	# print("request_token: ", request_token)
	#
	# # Authorization de lapp a mon compte
	# headers = {
	# 	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
	# }
	#
	# r = requests.get('https://getpocket.com/auth/authorize?request_token=' + request_token + '&redirect_uri=www.google.fr', headers=headers, allow_redirects=True)
	# print("status_code:", r.status_code, " for ", r.url)
	# code = subprocess.call(["C:\Program Files (x86)\Google\Chrome\Application\chrome.exe", r.url])
	#
	# # get access token
	# r3 = requests.get('https://getpocket.com/v3/oauth/authorize?consumer_key=' + consumer_key + '&code=' + request_token, allow_redirects=True)
	# code = r3.content
	# print("+++", code)
	# access_token = str(code).split("=")[1].split("&")[0]
	# print("access_token", access_token)

	# Get all data
	r4 = requests.get('https://getpocket.com/v3/get?consumer_key=' + CONSUMER_KEY + '&access_token=' + ACCESS_TOKEN)
	code = r4.content

	# loads json data
	loaded_json = json.loads(code)

	# random saved post
	list_saved = [k for k in loaded_json["list"].keys()]
	random_saved_key = random.choice(list_saved)

	return loaded_json["list"][random_saved_key]['given_url']


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


@app.route("/")
def index():
	# Get Random Trello Card :
	random_card = get_random_trello_card()

	# Get Random Pocket informations:
	pocket_url = get_random_pocket()

	# render a template with random_card details
	return render_template("index.html", random_card=random_card, pocket_url=pocket_url)


if __name__ == '__main__':
	app.config['ENV'] = "development"
	app.run(debug=True)
