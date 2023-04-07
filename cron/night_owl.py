import sys
sys.path.append('/var/www/coin_village/cron')

from module.redis import *
from service.night_owl import *

#from multiprocessing import Process

rs = Redis()

tickers = rs.get_json_data("night_owls_target_tickers")

nos = NightOwlService()
nos.start("KRW-APT")

# if int(str(datetime.datetime.now())[11:13]) > 8:
#     nos.reset_redis("KRW-APT")
    
        
# for ticker in tickers:
#     nos = NightOwlService()
#     nos.start(ticker)

    # if int(str(datetime.datetime.now())[11:13]) > 8:
        
    #     rs.hdel_data("night_owls_bundle__bbbb_price", ticker)
    #     rs.hdel_data("night_owls_bundle__minimum_price", ticker)
    #     rs.hdel_data("night_owls_bundle__maximum_price", ticker)
    #     rs.hdel_data("night_owls_bundle__order_cnt", ticker)
    #     rs.hdel_data("night_owls_bundle__bollinger_states", ticker)