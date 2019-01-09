from trello import TrelloClient
import random
from flask import Flask, render_template
import requests
import json
import subprocess

# My API KEY
from keys import TRELLO_APP_KEY, TRELLO_USER_TOKEN, API_SECRET

client = TrelloClient(
	api_key=TRELLO_APP_KEY,
	api_secret=API_SECRET,
	token=TRELLO_USER_TOKEN,
	token_secret='your-oauth-token-secret'
)

app = Flask(__name__)


def get_pocket():

	# Retrieve request_token
	r2 = requests.get('https://getpocket.com/v3/oauth/request?consumer_key=83185-696ae1741f775407425ba954&redirect_uri=MyPocket123:authorizationFinished')
	code = r2.content
	request_token = str(code).split("=")[1].strip("'")
	#print("request_token: ", request_token)

	# Authorization de lapp a mon compte
	r = requests.get('https://getpocket.com/auth/authorize?request_token=' + request_token + '&redirect_uri=MyPocket123:authorizationFinished')
	#print(r.url)
#	code = subprocess.call(["C:\Program Files (x86)\Google\Chrome\Application\chrome.exe", r.url])

	# get access token
	r3 = requests.get('https://getpocket.com/v3/oauth/authorize?consumer_key=83185-696ae1741f775407425ba954&code=' + request_token)
	code = r3.content
	access_token = str(code).split("=")[1].split("&")[0]
#	print("access_token", access_token)

	# Get all data
	r4 = requests.get('https://getpocket.com/v3/get?consumer_key=83185-696ae1741f775407425ba954&access_token=' + access_token)
	code = r4.content
#	print(">>>", code)

	# loads json data
	loaded_json = json.loads(code)
#	print(loaded_json["list"]['2341781570']['given_url'])

	# random saved post
	list_saved = [k for k in loaded_json["list"].keys()]
	random_saved_key = random.choice(list_saved)
#	print(">>>>>>", random_saved_key)

	return loaded_json["list"][random_saved_key]['given_url']


@app.route("/")
def index():
	# list trello boards
	lst_boards = client.list_boards()

	# list of the TODOS Boards
	todos_board = lst_boards[1]
	lst_brd_lists = todos_board.list_lists()

	# list cards of TODOS board
	todos_lst_cards = lst_brd_lists[0]
	lst_cards = todos_lst_cards.list_cards()

	# Generate a random card of the list
	random_card = random.choice(lst_cards)

	# Get Pocket informations:
	pocket_url = get_pocket()

	# render a template with random_card details
	return render_template("index.html", random_card=random_card, pocket_url=pocket_url)


if __name__ == '__main__':

	app.config['ENV'] = "development"
	app.run(debug=True)
