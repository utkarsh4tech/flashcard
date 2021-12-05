from flask import render_template, flash, redirect
from flask import current_app as app
from flask.helpers import url_for
from flask_login import login_required, login_user, logout_user, current_user
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash

from application.models import *
from application.form import *


@app.route("/", methods=['GET','POST'])
def home():
    return render_template("index.html")

@app.route("/about", methods=['GET','POST'])
def about():
    return render_template("about.html")

@app.route("/dashboard", methods=['GET','POST'])
@login_required
def dashboard():
    decks=None
    decks=Deck.query.filter_by(owner_userid=current_user.get_id()).all()
    return render_template("dashboard.html",decks=decks)

@app.route("/add_deck/<currentUserId>",methods=['GET','POST'])
@login_required
def add_deck(currentUserId):
    form = AddorEditDeckForm()
    deck=None
    if form.validate_on_submit():
        deck_name=form.deckname.data
        deck=Deck.query.filter_by(deck_name = deck_name , owner_userid = int(currentUserId)).first()
        if deck==None:
            deck=Deck(deck_name = deck_name , owner_userid = int(currentUserId), last_reviewed=datetime.now().strftime('%d-%m-%Y %H:%M') , deck_score=0)
            db.session.add(deck)
            db.session.commit()
            flash("Deck has been added successfully!!!")
            return redirect(url_for("dashboard"))
        else:
            flash("Deck already exists!!!")
    return render_template("add_edit_deck.html",form=form,form_title="Add")

@app.route("/edit_deck/<deckid>",methods=['GET','POST'])
@login_required
def edit_deck(deckid):
    form = AddorEditDeckForm()
    deck=None
    if form.validate_on_submit():
        deck=Deck.query.filter_by(deck_id=int(deckid)).first()
        anotherdeck=Deck.query.filter_by(deck_name=form.deckname.data).first()
        if anotherdeck is None:
            deck.deck_name=form.deckname.data
            db.session.commit()
            return redirect(url_for('dashboard'))
        else:
            flash("Similar Deck Present")
    return render_template("add_edit_deck.html",form_title="Edit",form=form)

@app.route("/delete_deck/<deckid>",methods=['GET','POST'])
@login_required
def delete_deck(deckid):
    deck=Deck.query.filter_by(deck_id=int(deckid)).first()
    if len(deck.cards)==0:
        db.session.delete(deck)
        db.session.commit()
        flash("Deck Deleted!!!")
        return redirect(url_for("dashboard"))
    else:
        flash("Deck has cards, delete them first!!")
        return redirect(url_for("dashboard"))

@app.route("/add_card/<deckid>",methods=['GET','POST'])
@login_required
def add_card(deckid):
    question,answer=None,None
    card=None
    form=AddCardForm()
    if form.validate_on_submit():
        question , answer = form.question.data , form.answer.data
        card=Card(question  = question , answer = answer , deck_id = deckid , card_score= 0, last_reviewed = datetime.now().strftime('%d-%m-%Y %H:%M'))
        db.session.add(card)
        db.session.commit()
        return redirect(url_for("view_cards",deckid=deckid))
    return render_template("add_edit_card.html",form=form,formtitle="Add")

@app.route("/view_cards/<deckid>",methods=['GET','POST'])
@login_required
def view_cards(deckid):
    cards=None
    cards=Card.query.filter_by(deck_id=deckid)
    return render_template("card.html",cards=cards,deckid=deckid)

@app.route("/delete_card/<cardid>/<deckid>",methods=['GET','POST'])
@login_required
def delete_card(cardid,deckid):    
    card=Card.query.filter_by(id=int(cardid)).first()
    Card.query.filter_by(id=int(cardid)).delete()
    deck=Deck.query.filter_by(deck_id=deckid).first()
    deck.deck_score-=card.card_score
    db.session.commit()
    flash("Card Deleted!!!")
    return redirect(url_for("view_cards",deckid=int(deckid)))

@app.route("/edit_card/<cardid>",methods=['GET','POST'])
@login_required
def edit_card(cardid): 
    card=None
    form=AddCardForm()
    if form.validate_on_submit():
        card=Card.query.filter_by(id=int(cardid)).first()
        card.question,card.answer = form.question.data,form.answer.data
        db.session.commit()
        return redirect(url_for("view_cards",deckid=card.deck_id))
    return render_template("add_edit_card.html",form=form,formtitle="Edit")
    

@app.route("/review_card/<cardid>",methods=['GET','POST'])
@login_required
def review_card(cardid):
    form=ReviewCardForm()
    card=Card.query.filter_by(id=int(cardid)).first()
    if form.validate_on_submit():
        rating=form.rate.data
        card.card_score=int(rating)
        card.last_reviewed= datetime.now().strftime('%d-%m-%Y %H:%M')
        deckid=card.deck_id
        deck=Deck.query.filter_by(deck_id=deckid).first()
        cards=deck.cards
        deckscore=0
        for card in cards: 
            deckscore+=card.card_score
        deck.deck_score=deckscore
        deck.last_reviewed= datetime.now().strftime('%d-%m-%Y %H:%M')
        db.session.commit()
        return redirect(url_for("view_cards",deckid=int(card.deck_id)))

    return render_template("reviewcard.html",form=form,card=card)

@app.route("/logout", methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    flash("You have been logout!! Login Again to use.")
    return redirect(url_for("login"))

@app.route("/login", methods=['GET','POST'])
def login():
    username=None
    password=None
    form = LoginForm()
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        # clearing the form
        form.username.data=""
        form.password.data=""
        userqueried = User.query.filter_by(user_name=username).first()
        if userqueried:
            if check_password_hash(userqueried.hashed_password,password):
                login_user(userqueried)
                return redirect(url_for("dashboard"))
            else:
                flash("Wrong Password!!!")
        else:
            flash("User doesn't exists!!! Please register")

    return render_template("login.html",form=form)

@app.route("/register", methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        first_name=form.firstname.data
        last_name=form.lastname.data
        user=User.query.filter_by(user_name=form.username.data).first()
        if user==None:
            u=User(user_name = form.username.data, hashed_password = generate_password_hash(form.password.data),firstname = form.firstname.data, lastname = form.lastname.data )
            db.session.add(u)
            db.session.commit()
            # clearing the form
            form.username.data=""
            form.password.data=""
            form.firstname.data=""
            form.lastname.data=""
            form.checkpassword.data=""
            flash("User Added successfully!!")
            return redirect(url_for("login"))
        else: 
            flash("Username already exists!!")
            return redirect(url_for("register"))
    return render_template("register.html",form=form)
    
@app.errorhandler(404)
def pagenotfound(e):
    return render_template("404.html"),404
