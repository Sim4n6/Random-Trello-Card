from trello import TrelloClient
import random
from flask import Flask, render_template

# My API KEY
from keys import TRELLO_APP_KEY, TRELLO_USER_TOKEN, API_SECRET

client = TrelloClient(
	api_key=TRELLO_APP_KEY,
	api_secret=API_SECRET,
	token=TRELLO_USER_TOKEN,
	token_secret='your-oauth-token-secret'
)

app = Flask(__name__)


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

	# render a template with random_card details
	return render_template("index.html", random_card=random_card)


if __name__ == '__main__':

	app.config['ENV'] = "development"
	app.run(debug=True)
