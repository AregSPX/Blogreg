import os, secrets
from PIL import Image
from flask import url_for, current_app     # since we no longer have app variable to import, we use flask's built in alternative to refer to the current app we work with
from flask_mail import Message
from flaskblog import mail


def save_picture(form_picture):     # ֆունկցիա։ պահպանել/մուտքագրել տրված նկարը տվյալների բազայի մեջ՝ կոդավորված անվան տակ
    random_hex = secrets.token_hex(8)       # մենք չենք ուզում որ ֆայլերի անունները կրկնվեն պապկի մեջ նենց որ ամեն մեկին համխանեցնում ենք կոդ
    _, f_ext = os.path.splitext(form_picture.filename)   # a, b = os.path.splitext(file.jpg) <==> a = 'file', b = '.jpg', ք․ո․ form_picture-ը ֆորմից ստացված ֆայլ է ինքը ունի filename ատրը
    picture_fn = random_hex + f_ext     # նկարի ֆայլի անվան կոդավորում՝ պահպանելով իր extension-ը (jpg/png)
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)   # os.path.join - ֆայլի Path-ի ստեղծում, app.root_path - գծումա ճամփեն մինչև package-ը (flaskproject պապկեն), փակագծի միջի գրածները կպցնում ենք իրար և ստացվում է ամբողջական ճանապարհը։

    output_size = (125, 125)        # 125x125 pixels (a tuple)
    i = Image.open(form_picture)    # i - ը հավասարեցնում/համխանեցնում ենք մուտքագրված նկարին
    i.thumbnail(output_size)        # i - ի չափերը փոխում ենք 125x125 (ըստ տրված tuple-ի)

    i.save(picture_path)     # պահպանում ենք մուտքագրված նկարը մեր ուզած պապկի մեջ (մեր գծած ճամփով), կոդավորված անվան տակ և չափերը հարմարեցրած, սա անում ենք որ սերվերը չծանրաբեռնվի

    return picture_fn     # ֆունկցիան վերադարձնում է պահպանված նկարի ֆայլի անունը (կամ էլ հենց էտ նկարը)


def send_reset_email(user):         # ուղարկել տրված օգտատիրոջը resetpassword email
    token = user.get_reset_token()  # initialize a token
    
    msg = Message('Password Reset Request', sender='noreply@flaskblog.com', recipients=[user.email])    # sending the email
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}       

If you did not make this request, then simply ignore this email and no changes will be made.
'''             # _external = True - to get an absolute URL
    
    mail.send(msg)   # ուղարկել նամակը․ Message-ի մեջ արդեն նշված է թե ումից և ում
    