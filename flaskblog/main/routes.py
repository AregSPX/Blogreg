# Blueprint - ները դա ենթա-package - ներ են, որոնց միջոցով տեղի է ունենում app - ի հետագա refactoring
# Այստեղ ներառված են միայն այն route - ները, որոնք կրում են առավել ընդհանուր բնույթ (main) 


from flask import render_template, request, Blueprint
from flaskblog.models import Post

main = Blueprint('main', __name__)        # 'main' package - ի հռչակում որպես Blueprint



# app.route - ը սարքում ենք main.route լոտե Blueprint - ը վերցրել ենք main փոփի տակ

@main.route('/')     #routes let us make pages of website, փակագծի պարունակությունը էտ կոնկրետ էջի կոդը կամ անուննա (էտի պտի գրես սայտի անունի վերջում որ էտ էջը բացես)
@main.route('/home') #շարքով ինչքան ուզում ես ռուտեր ավելացրա, սաղ փակագծի կոդերը տակի 1 ֆ-ով սահմանվող միարժեք նույն էջին կբերեն

def home():             #էջի պարունակությունը, որը արտահայտվում է f-ով
                        #main = Post.query.all()    # Post.query.all() - մատրի բոլոր տողերի հարցում/հավաքագրում main փոփի տակ

    page = request.args.get('page', 1, type=int)       # url - ի մեջ 'page' փոփը ընդունում է բնական թիվ արժեքներ (type = int), default - ը 1-ն է (1)․ բոլոր այդ բնական թվերով որոշված route-ները վերցնում ենք page փոփի տակ

    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5) # պոստերի բաժանում էջերի, per_page = 5 - ամեն էջի վրա 5 պոստ, page = page - թե որ էջը ցույց տալ, դա որոշվում է url - ի page փոփով, որը փաստացի բնական թվերի բազմություն է, փաստացի home էջը բաժանեցինք ենթաէջերի
    # Post.query.order_by(Post.date_posted.desc()) - պոստերը դասավորում ենք ըստ ամսաթվերի նվազման կարգով, այսինքն ամենաուշից ամենաշուտ, հետո նոր արդեն արդյունքը էջավորում ենք

    return render_template('home.html', posts = posts) # render_template թ․է․տ․ տեքստը ընդեղ գրել ու կարճ քցել ստեղ, main փոփի տակինը (տվյալ դեպքում ինչ որ L) դառնում է հասանելի template-ի մեջ main-ի տակ


@main.route('/about')  
def about():
    return render_template('about.html', title = 'About')

