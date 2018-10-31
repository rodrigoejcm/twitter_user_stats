import json
#import db_init
import datetime
#from pony.orm import *
#from dateutil import parser


from birdy.twitter import UserClient
import pass_tw_2 ## twitter credentials
#import unicodedata
#from unidecode import unidecode


client = UserClient(pass_tw_2.CONSUMER_KEY,
                    pass_tw_2.CONSUMER_SECRET,
                    pass_tw_2.ACCESS_TOKEN,
                    pass_tw_2.ACCESS_TOKEN_SECRET)

#follow = ['8802752','9317502','14594813','790680', '2174537102', '54341363', '65473559', '17715048', '14594698', '16632084', '128372940', '354095556', '29913589'] 
follow = ['23941036','21207962','142393421']
# revista piaui = 23941036
# epocA = 21207962
# globo news = 142393421

#follow = ['790680']

for u in follow:

    u_id = u

    response = client.api.statuses.user_timeline.get(user_id=u_id,exclude_replies=True, include_rts=False, count=30)

    with open('/home/rodrigo/Projects/twitter_test_birdy_lib/tw_user_stats/json/'+u_id+'_twitter_user_tl.json', 'a') as my_file:
        json.dump(response.data, my_file)