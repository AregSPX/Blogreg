# seperating configurations into a seperate module, summarizing them in a class


import os


class Config:


    SECRET_KEY = os.environ.get('SECRET_KEY')     #անվտանգության կոդ, ֆորմերի վրա մանիպուլյացիաները կանխելու համար (secrets.token_hex())


    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')     # URI - the location of our database, infact it's just a file in our file system 

    
    MAIL_SERVER = 'smtp.gmail.com'   # using Gmail to send the emails
    MAIL_PORT = 587
    MAIL_USE_TLS = True              # TLS is some security stuff

    MAIL_USERNAME = os.environ.get('EMAIL_USER')         # using our environment variables (Email User and Email Password) to privately use the sender email
    MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

