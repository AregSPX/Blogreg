# Blueprint - ները դա ենթա-package - ներ են, որոնց միջոցով տեղի է ունենում app - ի հետագա refactoring
# Այստեղ ներառված են միայն այն route - ները, որոնք վերաբերվում են օգտատերերին (users) 


import os
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm                                   
from flaskblog.users.utils import save_picture, send_reset_email



users = Blueprint('users', __name__)        # 'users' package - ի հռչակում որպես Blueprint


# app.route - ը սարքում ենք users.route լոտե Blueprint - ը վերցրել ենք users փոփի տակ
@users.route("/register", methods = ['GET', 'POST'])  #պտի թույլ տանք POST մեթոդը որ էջը կարանա ընդունի մուտքագրված տվյալները 
def register():
    if current_user.is_authenticated:   # եթե արդեն օգտատեր կա լոգին եղած registerlogin-ը անիմաստ են դառնում
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    
    if form.validate_on_submit():   #validate_on_submit() - ստուգումա թե արդյուք ֆորմի տվյալները հաջողաբար լրացրվել են
        
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')   #generate_password_hash() - մուտքագրված պառոլը (form.password.data) hash-ում ենք (շիֆռում) կամ նույնը կլինի ասել գաղտնագրում, ․decode('utf-8') - hash-ը կլինի str այլոչթե բայթերով

        user = User(username = form.username.data, email = form.email.data, password = hashed_password)  # գաղտնագրվածն ենք գրանցում բազայում, որ խակեռը բան չկարանա անի
        
        db.session.add(user)  # տեղյակ պահում որ ուզում ենք ավելացնենք (բուֆեռ քցում)

        db.session.commit()   # բուն ավելացում

        flash('Your account has been created! You are now able to log in.', 'success')  #flash - վերևից ծանուցում-նամակ, success - Bootstrap-ից flash-ի ոճ 
        
        return redirect(url_for('users.login'))    #redirect - ուղարկի/քցի նշված էջ
    
    return render_template('register.html', title='Register', form=form)  #register.html template-ին փոխանցում ենք RegistrationForm կլասի օրինակ form-ը, հենց իր անվան տակ


@users.route("/login", methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:    # եթե արդեն օգտատեր կա լոգին եղած registerlogin-ը անիմաստ են դառնում
        return redirect(url_for('main.home'))
    form = LoginForm()
    
    if form.validate_on_submit():       #եթե սկզբնական տեստերը (ֆորմի դաշտերի սահմանաչափեր) անցել/վալիդ են

        user = User.query.filter_by(email=form.email.data).first()  #user - այն օգտատերը, որի email-ը մուտքագրվել է ֆորմի մեջ, first() -ը ընդհանրապես առաջին օբյեկտն է վերցնում բազայից, բայց ք․ո․ ամեն email-ը այնտեղ յուրահատուկ է տարբերություն չկա, հենց էտ մեկը կվերադարձնի

        if user and bcrypt.check_password_hash(user.password, form.password.data):  #եթե այդպիսի օգտատեր գոյություն ունի և այդ օգտատիրոջ գաղտնաբառը բազայում (user.password) նույնն է ինչ ֆորմի մեջ մուտքագրվածը (form.password.data):
            login_user(user, remember = form.remember.data)     #user-ը մտնում է համակարգ, remember - նա կհիշվի եթե ճտիկը սղմվել է (form.remember.data = True)
            next_page = request.args.get('next')    # լոգինի էջի URL-ի մեջ կարա լինի պարամետր և դրան համխանող route (այստեղ պարամը next-ն է, route-ը /account): request-ը թէտ այդ route-ին հասնել, բռնել, վերցնել և դնել փոփի տակ 
            return redirect(next_page) if next_page else redirect(url_for('main.home'))    # եթե վերոնշյալ՝ next պարամետրին համխանող route-ը առհասարակ գոյություն ունի, ապա ուղղորդում այդ էջ, այլապես ուղղորդում դեպի տնական էջ
        
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')   #danger - error style
    return render_template('login.html', title='Login', form=form) # մնում ենք նույն էջի վրա (ուղղորդվեցինք դեպի նույն էջը) սա կլինի եթե վերոնշյալ if statement-ները = False


@users.route("/logout")
def logout():
    logout_user()                         #ոչինչ պետք չէ գրել լոտե պարզ է արդեն թե ովա մտած, 1 մարդա եղածը
    return redirect(url_for('main.home'))



@users.route("/account", methods = ['GET', 'POST'])
@login_required         #եթե լոգին եղած չի, մինչև էս էջը մտնելը մի հատ կքցի login-ի էջ
def account():
    form = UpdateAccountForm()
    
    if form.validate_on_submit():       #փոփոխում ենք օգտատիրոջ տվյալները բազայի մեջ, եթե ամեն-ինչը վալիդ է
        
        if form.picture.data:       # եթե ֆորմի մեջ մուտքագրվել է նկար
            
            if current_user.image_file != 'default.jpg':    # եթե օգտատիրոջ նկարը default - ը չէր։
                os.remove(os.path.abspath('flaskblog/static/profile_pics/' + current_user.image_file))  # ապա ջնջել այդ (հին) նկարը բազայից

            picture_file = save_picture(form.picture.data)      # նոր (ֆորմի մեջ լրացված) նկարը պահպանում ենք բազայի մեջ (profile_pics պապկեն)
            current_user.image_file = picture_file              # թարմացնում ենք օգտատիրոջ նկարը
        
        current_user.username = form.username.data  
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))     # սա անում ենք որ չբերի 'Are you sure' flash-ը
    
    elif request.method == 'GET':   # GET method - ոչ թե տվյալների մուտքագրում, այլ դրանց վերբեռնում։ Եթե տեղի ունի GET-ը (ֆորմը չի լրացվել, տվյալները չեն թարմացվել) ապա ցուցադրել ներկա տվյալները դաշտերում
       form.username.data = current_user.username 
       form.email.data = current_user.email

    image_file = url_for('static', filename = 'profile_pics/' + current_user.image_file)    #նկարները static պապկի մեջ են, մեր ուզած նկարը ստանալու համար այդտեղից մտնում ենք նաև profile_pics, որտեղ պահվում են նկարները, և վերջում ավելացնում հենց այդ նկարի անունը 
    return render_template('account.html', title='Account', image_file=image_file, form = form)



@users.route("/user/<string:username>")
def user_posts(username):           # օգտատիրոջ բոլոր պոստերը                
                        

    page = request.args.get('page', 1, type=int)       # url - ի մեջ 'page' փոփը ընդունում է բնական թիվ արժեքներ (type = int), default - ը 1-ն է (1)․ բոլոր այդ բնական թվերով որոշված route-ները վերցնում ենք page փոփի տակ

    user = User.query.filter_by(username=username).first_or_404()#բազայից ֆիլտրում ենք ֆունկցիայի պարամետրով տրված օգտատիրոջը (համխան մատրի տողը), եթե ինքը չգտնվի end-user - ին շպրտել 404 

    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5) # (author = user) օգտատիրոջ պոստերի բաժանում էջերի, per_page = 5 - ամեն էջի վրա 5 պոստ, page = page - թե որ էջը ցույց տալ, դա որոշվում է url - ի page փոփով, որը փաստացի բնական թվերի բազմություն է, փաստացի էջը բաժանեցինք ենթաէջերի
    # Post.query.order_by(Post.date_posted.desc()) - պոստերը դասավորում ենք ըստ ամսաթվերի նվազման կարգով, այսինքն ամենաուշից ամենաշուտ, հետո նոր արդեն արդյունքը էջավորում ենք

    return render_template('user_posts.html', posts = posts, user = user) # render_template թ․է․տ․ տեքստը ընդեղ գրել ու կարճ քցել ստեղ, posts փոփի տակինը (տվյալ դեպքում ինչ որ L) դառնում է հասանելի template-ի մեջ posts-ի տակ


    

@users.route("/reset_password", methods = ['GET', 'POST'])    
def reset_request():     # this is where they request the password to be reset
    
    if current_user.is_authenticated:    # եթե արդեն օգտատեր կա լոգին եղած այս route - ը անիմաստ է դառնում
        return redirect(url_for('main.home'))

    form = RequestResetForm()

    if form.validate_on_submit():       # եթե այդպիսի էլփոստով օգտատեր կա և ֆորմի լրացումը անցավ բարեհաջող։
        
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)      # the function creates a token (with expiration date) and sends the email
        flash('An email has been sent with instructions to reset your password. Make sure to check the Spam folder.', 'info')
        return redirect(url_for('users.login'))

    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods = ['GET', 'POST'])    
def reset_token(token):     # this is where they actually reset the password with the token active
    
    if current_user.is_authenticated:    # եթե արդեն օգտատեր կա լոգին եղած այս route - ը անիմաստ է դառնում
        return redirect(url_for('main.home'))
    
    user = User.verify_reset_token(token)   # if we dont receive a user here, the token is either invalid or expired

    if user is None:        # բանն այն է որ տոկենը իր մեջ է կրում user - ին, չկա տոկեն = չկա օգտատեր  
        
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    
    # եթե տոկենը վալիդա անցնում ենք առաջ
    form = ResetPasswordForm()

    if form.validate_on_submit():   #validate_on_submit() - ստուգումա թե արդյուք ֆորմի տվյալները հաջողաբար լրացրվել են
        
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')   #generate_password_hash() - մուտքագրված պառոլը (form.password.data) hash-ում ենք (շիֆռում) կամ նույնը կլինի ասել գաղտնագրում, ․decode('utf-8') - hash-ը կլինի str այլոչթե բայթերով

        user.password = hashed_password  # reset password
      
        db.session.commit()   # բուն ավելացում

        flash('Your password has been updated.', 'success')  #flash - վերևից ծանուցում-նամակ, success - Bootstrap-ից flash-ի ոճ 
        
        return redirect(url_for('users.login'))    #redirect - ուղարկի/քցի նշված էջ

    return render_template('reset_token.html', title='Reset Password', form=form)
