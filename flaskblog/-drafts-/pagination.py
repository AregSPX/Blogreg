from flaskblog.models import Post

posts = Post.query.paginate()   # պոստերի տրոհում էջերի 

print(posts.page)   # որ էջի վրա ենք

print(posts.per_page)   # քանի պոստ կա ամեն էջի վրա

for post in posts.items:
    print(post)     # տպել միայն և միայն տվյալ էջի վրա գտնվող պոստերը

posts = Post.query.paginate(per_page=4, page = 2)   # այնպիսի տրոհում, որ ամեն էջի վրա 4 պոստա։ Համ էլ ասինք որ հիմա գտնվի երկրորդ էջի վրա

posts.per_page = 3
posts.page = 3      # ընթացքում կարանք այս ամենը փոփոխենք

print(posts.total)  # տպել բոլոր էջերի բոլոր բոլոր բոլոր պոստերի քանակը 

