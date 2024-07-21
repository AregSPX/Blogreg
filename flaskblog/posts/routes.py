# Blueprint - ները դա ենթա-package - ներ են, որոնց միջոցով տեղի է ունենում posts - ի հետագա refactoring
# Այստեղ ներառված են միայն այն route - ները, որոնք վերաբերվում են պոստերին (posts) 

from flask import render_template, url_for, flash, redirect, request, abort, Blueprint                   
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm




posts = Blueprint('posts', __name__)        # 'posts' package - ի հռչակում որպես Blueprint


# posts.route - ը սարքում ենք posts.route լոտե Blueprint - ը վերցրել ենք posts փոփի տակ

@posts.route("/post/new", methods = ['GET', 'POST'])     # նոր պոստ հրապարակելու էջ
@login_required
def new_post():
    form = PostForm()               # այստեղ մենք սահմանում ենք ֆորմի տրամաբանությունը (backend) իսկ զուտ ֆոնի տեղադրումը էջի վրա արդեն create_post.html - ում
    if form.validate_on_submit():
       post = Post(title = form.title.data, content = form.content.data, author = current_user)     # մենք կարող ենք user_id - ի տեղը օգտագործենք 'author' backref-ը, ըստ ճաշակի է
       db.session.add(post)
       db.session.commit()
       flash('Your post has been created!', 'success')
       return redirect(url_for('main.home'))    # արդեն որ ներմուծել ենք blueprint - ներ, պետք է այսպես ձևափոխել բոլոր url_for - ները relative - ի
    
    return render_template('create_edit_post.html', title='New Post', form = form, legend = 'New Post')



@posts.route("/post/<int:post_id>")       # route - ների խումբ, որոնք տարբերվում են ըստ post_id փոփոխականի, որը int է․ ամեն մեկը համխան պոստի ամբողջական դիտման էջն է
def post(post_id):
    post = Post.query.get_or_404(post_id)   # եթե գոյություն ունի վերցրու, այլապես 404 շպրտի
    return render_template('post.html', title=post.title, post=post)      # 'New Post' str-ն legend փոփի ներքո ուղարկում ենք template 


@posts.route("/post/<int:post_id>/update", methods = ['GET', 'POST'])    # route - ների խումբ, որոնք տարբերվում են ըստ post_id փոփոխականի, որը int է․ ամեն մեկը համխան պոստի թարմացման էջն է
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)   # եթե գոյություն ունի վերցրու, այլապես 404 շպրտի
    
    if post.author != current_user:     # եթե պոստի չտերը փորձում է այն թարմացնել։
        abort(403)          # շպրտել 403, հետագայում կոճավորենք այդ էջը 
    
    form = PostForm()

    if form.validate_on_submit():           # Թարմացրու պոստի տվյալները բազայի մեջ (կարճ ասած պոստը) եթե ֆորմը վալիդ է լրացվել
        
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id = post.id))       # արդեն որ ներմուծել ենք blueprint - ներ, պետք է այսպես ձևափոխել բոլոր url_for - ները relative - ի
    
    
    elif request.method == 'GET':       # օգտատիրոջ տվյալների թարմացման պես

        form.title.data = post.title        # նենց ենք անում որ պոստը թարմացնելուց ֆորմի մեջ գրած լինի ներկա տվյալները (վերնագիր և կոնտենտ)
        form.content.data = post.content

    return render_template('create_edit_post.html', title='Update Post', form = form, legend = 'Update Post')      # 'Update Post' str-ն legend փոփի ներքո ուղարկում ենք template 





@posts.route("/post/<int:post_id>/delete", methods = ['POST'])  # այս route - ը ինքն իրենով էջ չէ, իր ֆունկցիան պոստը բազայից ջնջելն է և միաժամանակ ուղարկել տնային էջ
@login_required                              # միայն POST լոտե մոդալից ընդհամենը պատասխան (մուտքագրում) ենք վերցնում և էլ ոչինչ
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)   # եթե գոյություն ունի վերցրու, այլապես 404 շպրտի
    
    if post.author != current_user:     # եթե պոստի չտերը փորձում է այն թարմացնել։
        abort(403)          # շպրտել 403, հետագայում կոճավորենք այդ էջը 

    db.session.delete(post)     # պոստի ջնջում բազայից
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))       # արդեն որ ներմուծել ենք blueprint - ներ, պետք է այսպես ձևափոխել բոլոր url_for - ները relative - ի
    

