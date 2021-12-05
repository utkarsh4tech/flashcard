from flask_restful import reqparse

# creating a parser for adding new user , method=POST
user_parser=reqparse.RequestParser()
user_parser.add_argument("firstname")
user_parser.add_argument("lastname")
user_parser.add_argument("username")
user_parser.add_argument("password")

# creating a parser for editing user , method=PUT
update_user_parser=reqparse.RequestParser()
update_user_parser.add_argument("firstname")
update_user_parser.add_argument("lastname")
update_user_parser.add_argument("password")

# creating a parser for Deck , method=POST
deck_parser=reqparse.RequestParser()
deck_parser.add_argument("deck_id")
deck_parser.add_argument("deck_name")
deck_parser.add_argument("owner_userid")

# creating a parser for Deck , method=PUT
update_deck_parser=reqparse.RequestParser()
update_deck_parser.add_argument("deck_name")

# creating a parser for Card , method=PUT
card_parser=reqparse.RequestParser()
card_parser.add_argument("question")
card_parser.add_argument("answer")

# creating a parser for Card , method=POST
post_card_parser=reqparse.RequestParser()
post_card_parser.add_argument("question")
post_card_parser.add_argument("answer")
post_card_parser.add_argument("deckid")