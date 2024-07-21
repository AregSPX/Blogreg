#form - հարց ու պատասխանի դաշտ
#flask_wtf - ֆորմերի ստեղծման ֆլասկի լուծումը


from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User




class RegistrationForm(FlaskForm):                      #ֆլասկը թ․է․տ․ html-ից ծանոթ form-երը արտահայտել Python-ի կլասերի միջոցով
    
    username = StringField('Username',                                  #Username վերնագրով դաշտի ստեղծում, StringField կլասի օրինակ
        validators=[DataRequired(), Length(min = 2, max = 20)])         #DataRequired - դաշտը պետք է դատարկ չլինի, Length - պատասխանի երկարության միջակայք
    
    email = StringField('Email', validators=[DataRequired(), Email()])  #Email() - ստուգում է որ մուտքագրված լինի վալիդ email 

    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])  #EqualTo - ստուգում է որ մուտքագրված լինի նույնը բանը ինչ password փոփին համխանող դաշտում
    
    
    submit = SubmitField('Sign Up')   #SubmitField - 'Sign Up' վերնագրով ամփոփիչ կոճակ

    
    
    #ներքոնշյալ 2 ֆունկցիաները լռելյայն գործում են ֆորմի մեջ, դրանք հատուկ կանչել պետք չէ
    def validate_username(self, username):  #ֆունկցիայով username անունը ստուգում ենք որ չկրկնվի

        user = User.query.filter_by(username = username.data).first()   #եթե username-ը կա բազայում, user-ը None չի լինի և նրան կտրվի հենց այդ համխանող մարդու արժը

        if user:    #եթե user-ը None չի (անունը արդեն զբաղված է)

            raise ValidationError('That username is taken. Please choose a different one.')     # էս սխալը ցուցադրել
        
    def validate_email(self, email):  #ֆունկցիայով email անունը ստուգում ենք որ չկրկնվի

        user = User.query.filter_by(email = email.data).first()   #եթե email-ը կա բազայում, user-ը None չի լինի և նրան կտրվի հենց այդ համխանող մարդու արժը

        if user:    #եթե user-ը None չի (անունը արդեն զբաղված է)

            raise ValidationError('That email is taken. Please choose a different one.')     # էս սխալը ցուցադրել


class LoginForm(FlaskForm):     #սա արդեն login ֆորմն է որը մեծ մասով կրկնում է register-ը           
       
    email = StringField('Email', validators=[DataRequired(), Email()])  #Email() - ստուգում է որ մուտքագրված լինի վալիդ email 

    password = PasswordField('Password', validators=[DataRequired()])

    remember = BooleanField('Remember Me')  #BooleanField - 'Remember Me' վերնագրով պտիչկա
    
    submit = SubmitField('Login')   

class UpdateAccountForm(FlaskForm):           # օգտատիրոջ մականվան և էլփոստի փոփոխության ֆորմ
    
    username = StringField('Username',                                  #Username վերնագրով դաշտի ստեղծում, StringField կլասի օրինակ
        validators=[DataRequired(), Length(min = 2, max = 20)])         #DataRequired - դաշտը պետք է դատարկ չլինի, Length - պատասխանի երկարության միջակայք
    
    email = StringField('Email', validators=[DataRequired(), Email()])  #Email() - ստուգում է որ մուտքագրված լինի վալիդ email 

    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    
    submit = SubmitField('Update')   #SubmitField - 'Sign Up' վերնագրով ամփոփիչ կոճակ



    #ներքոնշյալ 2 ֆունկցիաները լռելյայն գործում են ֆորմի մեջ, դրանք հատուկ կանչել պետք չէ
    def validate_username(self, username):  #ֆունկցիայով username անունը ստուգում ենք որ չկրկնվի
        if username.data != current_user.username:  #տվյալները թարմացնելու ժամանակ ստուգումը կլինի միայն այն դեպքում, եթե օգտատերը չի գրել նույն անունն ու email-ը (դա հատուկ, վալիդ դեպք է)
            user = User.query.filter_by(username = username.data).first()   #եթե username-ը կա բազայում, user-ը None չի լինի և նրան կտրվի հենց այդ համխանող մարդու արժը

            if user:    #եթե user-ը None չի (անունը արդեն զբաղված է)

                raise ValidationError('That username is taken. Please choose a different one.')     # էս սխալը ցուցադրել
            
    def validate_email(self, email):  #ֆունկցիայով email անունը ստուգում ենք որ չկրկնվի
        if email.data != current_user.email:  #տվյալները թարմացնելու ժամանակ ստուգումը կլինի միայն այն դեպքում, եթե օգտատերը չի գրել նույն անունն ու email-ը (դա հատուկ, վալիդ դեպք է)
            user = User.query.filter_by(email = email.data).first()   #եթե email-ը կա բազայում, user-ը None չի լինի և նրան կտրվի հենց այդ համխանող մարդու արժը

            if user:    #եթե user-ը None չի (անունը արդեն զբաղված է)

                raise ValidationError('That email is taken. Please choose a different one.')     # էս սխալը ցուցադրել



class RequestResetForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Email()])      #Email() - ստուգում է որ մուտքագրված լինի վալիդ email 

    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):  #ֆունկցիայով email անունը ստուգում ենք որ չկրկնվի, այդ email - ը պետք է ոչ մեկի կողմից զբաղված չլինի
        
        user = User.query.filter_by(email = email.data).first()   #եթե email-ը կա բազայում, user-ը None չի լինի և նրան կտրվի հենց այդ համխանող մարդու արժը

        if user is None:    #եթե user-ը None է (ֆորմի մեջ լրացված էլփոստով օգտատեր գոյություն չունի)

            raise ValidationError('There is no account with that email. You must register first.')     # էս սխալը ցուցադրել
            


class ResetPasswordForm(FlaskForm):

    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])  #EqualTo - ստուգում է որ մուտքագրված լինի նույնը բանը ինչ password փոփին համխանող դաշտում

    submit = SubmitField('Reset Password')