from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SelectField,SubmitField
from wtforms.validators import InputRequired, Length, EqualTo
from flask_ckeditor import CKEditorField

class RegisterForm(FlaskForm):
    firstname = StringField(label="Firstname",validators=[InputRequired()], render_kw={"placeholder":"First Name"})
    lastname = StringField(label="Lastname",render_kw={"placeholder":"Last Name"})
    username = StringField(label="Username",validators=[InputRequired(), Length(min=8,max=20)], render_kw={"placeholder":"Username"})
    password = PasswordField(label="Password",validators=[InputRequired(), Length(min=8, max=20),EqualTo("checkpassword",message="Password Do not Match!!!Try Again")], render_kw={"placeholder": "Password"})
    checkpassword = PasswordField(label="Confirm Password",validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Check Password"})
    submit =  SubmitField("Register")

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=8,max=20)], render_kw={"placeholder":"Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit =  SubmitField("Login")

class AddorEditDeckForm(FlaskForm):
    deckname = StringField(label="Deck Name",validators=[InputRequired()], render_kw={"placeholder":"Deck Name"})
    submit =  SubmitField("Add deck")

class AddCardForm(FlaskForm):
    question = StringField(label="Question",validators=[InputRequired()], render_kw={"placeholder":"question"})
    answer = CKEditorField(label="Answer",validators=[InputRequired()], render_kw={"placeholder":"answer"})
    submit =  SubmitField("Add/Edit Card")

class ReviewCardForm(FlaskForm):
    rate = SelectField(u'Rate the Card!!!', choices=[(15, 'Easy'), (10, 'Medium'), (5, 'Hard')],render_kw={"placeholder":"Rating"})
    submit =  SubmitField("Submit Review")
