from trello import TrelloClient
import random

# My API KEY
from keys import TRELLO_APP_KEY, TRELLO_USER_TOKEN, API_SECRET

client = TrelloClient(
	api_key=TRELLO_APP_KEY,
	api_secret=API_SECRET,
	token=TRELLO_USER_TOKEN,
	token_secret='your-oauth-token-secret'
)

if __name__ == '__main__':
	# list trello boards
	lst_boards = client.list_boards()
	print(lst_boards)

	# list of the TODOS Boards
	todos_boards = lst_boards[1]
	lst_brd_lists = todos_boards.list_lists()
	print(lst_brd_lists)

	# list cards of TODOS board
	To_dos_lst_cards = lst_brd_lists[0]
	lst_cards = To_dos_lst_cards.list_cards()
	print(lst_cards)

	# Random card of the list
	random_card = random.choice(lst_cards)
	print("-->", random_card.name)
