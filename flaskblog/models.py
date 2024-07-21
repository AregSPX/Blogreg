from datetime import datetime
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app     # since we no longer have app variable to import, we use flask's built in alternative to refer to the current app we work with
from flaskblog import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader      #login լինելուց գտնում/վերադարձնում է (load-է անում) համխան մարդու համարը բազայից 
def load_user(user_id):
    return User.query.get(int(user_id))

#we can seperate our database structure into classes (those classes are called models), infact each class here is a table on its own
class User(db.Model, UserMixin):   #այսպիսով մենք կլասերի միջոցով սահմանում ենք db-ի մատրակերպերը (tables), այս տողի վրա օգտատերը բնութագրող կլասն է։ Օգտատերերի բազմությունը կազմում են table-ը
#UserMixin - flask_login - ից կլաս, որը իր մեջ է պարունակում 4 հատ ստուգիչ ֆունկցիա, որոնք ստուգում են մուտքագրված տվյալների վալիդությունը login լինելու ժամանակ
    
    id = db.Column(db.Integer, primary_key = True)   #այս տողի վրա սահմանված է User մատրի id սյունը, db.Integer - սյան արժերը ամբողջ թվեր են, primary_key = True - սյան ամեն մի արժը չի կրկնվում մեկ ուրիշ տողի վրա

    username = db.Column(db.String(20), unique = True, nullable = False) #db.String(20) - արժը 20-ը չգերազանցող երկարությամբ str է, unique = T - չկրկ, nullable = F - չդատարկ (պտի լինի)
    
    email = db.Column(db.String(120), unique = True, nullable = False) 

    image_file = db.Column(db.String(20), nullable = False, default = 'default.jpg') #profile picture represented by filename (a string), default - էն արժը, որը կընդունվի եթե հատուկ ոչ մի բան չասենք

    password = db.Column(db.String(60), nullable = False)


    posts = db.relationship('Post', backref = 'author', lazy = True)    #db.relationship('Post') - posts ատրը կապված է Post մոդելի հետ
    #backref - տալով Post-ին user_id ատրը այն կապում ենք համխան User ID-ին User մոդելում (համխան մարդուն)։ Այդ մարդուն Post մոդելի ներսում (պոստերի միջոցով) կարելի է հասնել backref-ի փոփի տակ։ Օրինակ եթե Արեգը արել է post_14, ապա post_14.author = Արեգ։
    # ամեն User ունի պոստեր, դա արտահայտում է վերոնշյալ posts ատրը։ db.relationship - ի միջոցով շեշտում ենք, որ այդ պոստերը Post կլասի օրինակներ են, և այդ պոստերը Post կլասի ներսում ունեն լրացուցիչ ատր՝ backref - ի տեսքով։ Մեր դեպքում backref - ը (author) համարժեք է Post - ի user_id ատրին։ Ամեն օգտատեր իր պոստերի նկատմամբ backref-ն է, այսինքն author-ը։ Նենց որ post_12.author <==> համխանող User
    # lazy = True - մեր պահանջով ամբողջ posts-ի տվյալները միաժամանակ կտպվեն

    def get_reset_token(self):    # creating tokens for password reset
        s = Serializer(current_app.config['SECRET_KEY'])    # creating Serializer object with secret key of app.config['SECRET_KEY'] 
        return s.dumps({'user_id': self.id})        # s.dumps - initializing the token, here we're returning token created by s Serializer with payload of current (տրված) user's username and secret key of app.config['SECRET_KEY'] 

    @staticmethod
    def verify_reset_token(token):      # verifying existing tokens, ԻՄԱՆՈՒՄ ԵՆՔ ԹԵ ՈՐ ՕԳՏԱՏԻՐՈՋՆ
        
        s = Serializer(current_app.config['SECRET_KEY'])    # creating Serializer object with secret key of app.config['SECRET_KEY']                                    
                                                                            
        try:    # որ տոկենը հարցում ենք, կարողա ինվալիդ կամ ժամկետանց լինի ու exception տա, դրա համար զուտ փորձում ենք
            user_id = s.loads(token, max_age=1800)['user_id'] #s.loads - token loading (արդեն իսկ ստեղծված տոկենի հարցում) ք․ո․ payload - ը D էր մենք դրա միջից բանալով օգտանունն ենք հանում
            print(user_id)                                    # max_age = 1800 - տոկենի վավերության ժամկետը վայրկյաններով
        
        except:     # եթե տոկենի հետ մի բան էն չի, ուղղակի ոչինչ չվերադարձնել
            return None
        
        return User.query.get(user_id)      # return the current user (with that user_id) if token is valid
    
    def __repr__(self):     # __repr__ or dunder repr - ներկայացուցչական ցուցադրում ծրագրավորողների համար
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
    

class Post(db.Model):       # Օգտատերերի հրապարակումները արտահայտող կլաս

    id = db.Column(db.Integer, primary_key = True)

    title = db.Column(db.String(100), nullable = False)

    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)   #փակագծեր չենք դնում լոտե կգրի հենց հիմիկվա ժամը (06.07.2024; 16:50)

    content = db.Column(db.Text, nullable = False)     #db.Text - տեքստի բլոկ


    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)     #db.ForeignKey - այս ատրը կապ ունի մեկ ուրիշ մոդուլի հետ, այստեղ User-ի id սյան հետ, այսպես ասած համխանում/հանգում/համընկնում է դրան


    def __repr__(self):     # __repr__ or dunder repr - ներկայացուցչական ցուցադրում ծրագրավորողների համար
        return f"Post('{self.title}', '{self.date_posted}')"
    