from wtforms import Form, StringField, PasswordField, validators, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Optional

class SignupForm(Form):

    name= StringField('Name', validators=[DataRequired(message=('Enter your name'))])

    email=StringField('E-mail',validators=[Length(min=6,message=('Please enter a valid e-mail address.')),
                               Email(message=('Please enter a valid e-mail address')),
                               DataRequired(message=('Please enter a valid e-mail address'))])

    password=PasswordField('Password',validators=[DataRequired(message=('Please enter a password')),
                                      Length(min=6,message=('Please enter a strong password')),
                                      EqualTo('confirm',message=('Passwords must match'))])

    confirm= PasswordField('Please confirm your password')

    website= StringField('Website', validators=[Optional()])

    submit= SubmitField('Register')


class LoginForm(Form):

    email= StringField('E-mail',validators=[DataRequired('Please enter a valid e-mail address.'),
                                           Email('Please enter a valid e-mail address')])
    
    password= PasswordField('Password',validators=[DataRequired('Please enter your password')])

    submit= SubmitField('Log In')