from flaskblog import db, User, Post     #import the database instance and its modules

db.create_all()    #create the database file

user_1 = User(username='SPX', email='S@demo.com', password='password')      #sample info   
user_2 = User(username='Corey', email='C@demo.com', password='password')    #sample info

db.session.add(user_1)      #letting SQL know we want to add this data to database, but not actually doing it yet
db.session.add(user_2)      #letting SQL know we want to add this data to database, but not actually doing it yet

db.session.commit()         #committing all the changes to database (CTRL+S), user_1 and user_2 are added to database now