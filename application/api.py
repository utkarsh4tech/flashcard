from flask_restful import Resource
from werkzeug.security import generate_password_hash
from datetime import datetime

from application.database import db
from application.models import User,Deck,Card
from application.validation import ValidationError
from application.parser import user_parser,update_user_parser,deck_parser,update_deck_parser,card_parser,post_card_parser

# RESTful API for USER
class UserApi(Resource):

    def get(self,username):
        user=User.query.filter_by(user_name=username).first()
        if user:
            return {"userid": user.user_id,
                    "username": user.user_name,
                    "firstname":user.firstname,
                    "lastname":user.lastname},200
        else:
            raise ValidationError(404,"UVE1006","Such user does not exist")

    def put(self,username):
        user=User.query.filter_by(user_name=username).first()
        if user is None:
            raise ValidationError(404,"UVE1006","Such user does not exist")
        else:
            args=update_user_parser.parse_args()
            firstname,lastname,password=args.get("firstname",None),args.get("lastname",None),args.get("password",None)
            if firstname is None:
                raise ValidationError(404,"UVE1001","Firstname is  required")
            elif password is None:
                raise ValidationError(404,"UVE1003","Password is required")
            elif len(password)<8 or len(password)>20:
                raise ValidationError(404,"UVE1005","Password must be between 8 to 20 characters")
            else:            
                user.firstname,user.lastname,user.password=firstname,lastname,generate_password_hash(password)
                db.session.commit()
                return {"new_fname":firstname,
                        "new_lname":lastname},200

    def delete(self,username):
        user=User.query.filter_by(user_name=username).first()
        if user is None:
            raise ValidationError(404,"UVE1006","Such user does not exist")
        elif len(user.decks)>0:
            raise ValidationError(404,"UVE1007","User has decks,Delete them first!")
        else:
            db.session.delete(user)
            db.session.commit()
            return {"deleteduser_id":user.user_id,
                    "deleteduser_fname":user.firstname,
                    "deleteduser_lname":user.lastname,
                    "deleteduser_username":user.user_name},200

    def post(self):
        args=user_parser.parse_args()
        firstname,lastname,username,password=args.get("firstname",None),args.get("lastname",None),args.get("username",None),args.get("password",None)
        if firstname is None:
            raise ValidationError(404,"UVE1001","Firstname is  required")
        elif username is None:
            raise ValidationError(404,"UVE1002","Username is  required")
        elif password is None:
            raise ValidationError(404,"UVE1003","Password is required")
        elif User.query.filter_by(user_name=username).first() is not None:
            raise ValidationError(404,"UVE1004","Username already exists")
        elif len(password)<8 or len(password)>20:
            raise ValidationError(404,"UVE1005","Password must be between 8 to 20 characters")
        else:
            newuser=User(user_name = username, hashed_password = generate_password_hash(password),firstname = firstname, lastname = lastname )
            db.session.add(newuser)
            db.session.commit()
            return {"newuserid":newuser.user_id,
                    "newuser_fname":newuser.firstname,
                    "newuser_lname":newuser.lastname,
                    "newuser_username":newuser.user_name,
                    "message":"New User Added Successfully"},200
                
# RESTful API for DECK
class DeckApi(Resource):
    
    def get(self,deckid):
        deck=Deck.query.filter_by(deck_id=deckid).first()
        if deck is None:
            raise ValidationError(404,"DVE1006","Deck does not exist")
        else:
            return {"deck_id":deck.deck_id,
                    "deck_name":deck.deck_name,
                    "owner_userid":deck.owner_userid,
                    "last_reviewed": deck.last_reviewed,
                    "deck_score":deck.deck_score},200

    def put(self,deckid):
        deck=Deck.query.filter_by(deck_id=deckid).first()
        if deck is None:
            raise ValidationError(404,"DVE1006","Deck does not exist")
        args=update_deck_parser.parse_args()
        deckname=args.get("deck_name",None)
        if deckname is None:
            raise ValidationError(404,"DVE1003","Deckname is required")
        else:
            deck.deck_name=deckname
            db.session.commit()
            return {"deck_id":deck.deck_id,
                    "updateddeck_name":deck.deck_name,
                    "owner_userid":deck.owner_userid,
                    "last_reviewed": deck.last_reviewed,
                    "deck_score":deck.deck_score},200

    def delete(self,deckid):
        deck=Deck.query.filter_by(deck_id=deckid).first()
        if deck is None:
            raise ValidationError(404,"DVE1006","Deck does not exist")
        elif len(deck.cards)>0:
            raise ValidationError(404,"DVE1007","Deck has cards , delete them first")
        else:
            db.session.delete(deck)
            db.session.commit()
            return {"deck_id":deck.deck_id,
                    "deck_name":deck.deck_name,
                    "owner_userid":deck.owner_userid,
                    "last_reviewed": deck.last_reviewed,
                    "deck_score":deck.deck_score},200

    def post(self):
        args=deck_parser.parse_args()
        deckid,deckname,ownerid=args.get("deck_id",None),args.get("deck_name",None),args.get("owner_userid",None)
        deck=Deck.query.filter_by(deck_id=deckid).first()
        ownerDoesNotExists=User.query.filter_by(user_id=ownerid).first() is None
        if deck is not None:
            raise ValidationError(404,"DVE1001","Deck id is duplicate")
        elif deckid is None:
            raise ValidationError(404,"DVE1002","Deckid is required")
        elif deckname is None:
            raise ValidationError(404,"DVE1003","Deckname is required")
        elif ownerid is None:
            raise ValidationError(404,"DVE1004","Ownerid is needed")
        elif ownerDoesNotExists:
            raise ValidationError(404,"DVE1005","Ownerid is not Valid")
        else:
            newDeck=Deck(deck_id=deckid,deck_name=deckname,owner_userid=ownerid,last_reviewed= datetime.now(),deck_score=0)
            db.session.add(newDeck)
            db.session.commit()
            return {"deck_id":newDeck.deck_id,
                    "deck_name":newDeck.deck_name,
                    "owner_userid":newDeck.owner_userid,
                    "last_reviewed": newDeck.last_reviewed,
                    "deck_score":newDeck.deck_score},200

# RESTful API for CARD
class CardApi(Resource):

    def get(self,cardid):
        card=Card.query.filter_by(id=cardid).first()
        if card is None:
            raise ValidationError(404,"CVE1001","Card does not exist")
        else :
            return {"cardid": card.id,
                    "question":card.question,
                    "answer":card.answer,
                    "cardscore":card.card_score,
                    "parent_deckid":card.deck_id,
                    "last reviewed":card.last_reviewed},200

    def put(self,cardid):
        card=Card.query.filter_by(id=cardid).first()
        if card is None:
            raise ValidationError(404,"CVE1001","Card does not exist")
        else:
            args=card_parser.parse_args()
            question,answer=args.get("question",None),args.get("answer",None)
            if question is None:
                raise ValidationError(404,"CVE1002","question is required")
            elif answer is None:
                raise ValidationError(404,"CVE1003","answer is required")
            elif question==card.question:
                raise ValidationError(404,"CVE1004","Question is same as previous")
            elif answer==card.answer:
                raise ValidationError(404,"CVE1005","Answer is same as previous")
            else:
                card.question,card.answer=question,answer
                db.session.commit()
                return {"cardid": card.id,
                    "updated question":card.question,
                    "updated answer":card.answer,
                    "cardscore":card.card_score,
                    "parent_deckid":card.deck_id,
                    "last reviewed":card.last_reviewed},200

    def delete(self,cardid):
        card=Card.query.filter_by(id=cardid).first()
        if card is None:
            raise ValidationError(404,"CVE1001","Card does not exist")
        else:
            db.session.delete(card)
            db.session.commit()
            return {"deleted cardid": card.id,
                    "question":card.question,
                    "answer":card.answer,
                    "deleted cardscore":card.card_score,
                    "parent_deckid":card.deck_id,
                    "last reviewed":card.last_reviewed},200

    def post(self):
        args=post_card_parser.parse_args()
        question,answer,deckid=args.get("question",None),args.get("answer",None),args.get("deckid",None)
        if question is None:
            raise ValidationError(404,"CVE1002","question is required")
        elif answer is None:
            raise ValidationError(404,"CVE1003","answer is required")
        elif deckid is None:
            raise ValidationError(404,"CVE1004","deckid is required")
        elif Deck.query.filter_by(deck_id=deckid).first() is None:
            raise ValidationError(404,"CVE1005","Deck does not exist")
        else:
            card=Card(question=question,answer=answer,card_score=0,last_reviewed= datetime.now(),deck_id=deckid)
            db.session.add(card)
            db.session.commit()
            return {"created cardid": card.id,
                    "question":card.question,
                    "answer":card.answer,
                    "cardscore":card.card_score,
                    "parent_deckid":card.deck_id,
                    "last reviewed":card.last_reviewed},200