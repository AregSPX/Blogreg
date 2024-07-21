#For anyone who needs help for the Serializer part:
# token - անհատական կոդ որը թէտ անել նենց որ միայն կոնկրետ մարդը կարանա պառոլը ռեսետ անի

from itsdangerous import URLSafeTimedSerializer as Serializer   # a tool for generating tokens
s = Serializer('secret')  # we use Serializer to pass the secret key ('secret')
token = s.dumps({'user_id': 1})    # s.dumps - generating the token, փակագծերի մեջ սահմանում ենք payload - ը, դա հենց նամակի պարունակությունն է (message - ը) որը ուզում ենք ուղարկենք end-user - ին
s.loads(token, max_age=30)  # s.loads - տոկենի պարունի (payload) ցուցադրում, max_page - տոկենի պիտանելիության ժամկետը վայրկյաններով

#if you wait until 'max_age' seconds, you'll get Signature expired.