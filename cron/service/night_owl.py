

import sys

sys.path.append('/var/www/coin_village/cron')

from module.upbit import *
from module.slack import *
from module.log import *
from module.redis import *
from common.function.common_function import *

import time


class NightOwlService:

    def __init__(self):
        # bbbb >> 하단 붕괴 

        self.upbit = Upbit()
        self.slack = Slack()
        self.log = Log()
        self.redis = Redis()

        self.ticker = None                      # 티커
        self.close_price_list = []              # 종가 리스트

        self.bbbb_price = None                  # bbbb가격
        self.bbbb_status = None                 # bbbb상태

        self.prev_bollinger_state = None        # 이전 볼린저 상태 값
        self.prev_minimum_price = None          # 이전 최저가 
        self.prev_maximum_price = None          # 이전 최고가 

        self.current_price = None               # 현재가
        self.current_bollinger_state = None     # 현재 볼린저 상태 값
        self.current_minimum_price = None       # 현재 최저가
        self.current_maximum_price = None       # 현재 최저가

        self.order_cnt = 0                      # 주문 횟수
        self.krw_balance = 0                    # 원화 잔고
        self.krw_order = 0                      # 원화 주문
        
        self.pref_bbbb_price = "night_owls_bundle_bbbb_price"                  # bbbb가격 prefix
        self.pref_bbbb_status = "night_owls_bundle_bbbb_status"                # bbbb상태 prefix

        self.pref_bollinger_state = "night_owls_bundle_bollinger_state"       # 볼린저 상태 prefix
        self.pref_minimum_price = "night_owls_bundle_minimum_price"            # 볼린저 최소가 prefix
        self.pref_maximum_price = "night_owls_bundle_maximum_price"            # 볼린저 최대가 prefix

        self.pref_order_cnt = "night_owls_bundle_order_cnt"                    # 볼린저 주문수량 prefix

    def reset_redis(self, ticker):
        """
        def description : 레디스 초기화
        """

        self.redis.hdel_data(self.pref_bbbb_price, ticker)
        self.redis.hdel_data(self.pref_bbbb_status, ticker)
        self.redis.hdel_data(self.pref_bollinger_state, ticker)
        self.redis.hdel_data(self.pref_minimum_price, ticker)
        self.redis.hdel_data(self.pref_maximum_price, ticker)
        self.redis.hdel_data(self.pref_order_cnt, ticker)

        return

    """
    SETTER
    """
    def set_standard_data(self):
        """
        def description : 기준데이터 조회
        """
        
        self.bbbb_price = self.redis.hget_data(self.pref_bbbb_price, self.ticker)    # bbbb 가격
        self.bbbb_status = self.redis.hget_data(self.pref_bbbb_status, self.ticker)  # bbbb 상태
        self.order_cnt = self.redis.hget_data(self.pref_order_cnt, self.ticker)      # 주문 횟수

        self.close_price_list = self.upbit.get_target_interval_prices("minute5", 10)            # 종가 10개 조회

        if self.bbbb_price: self.prev_minimum_price = float(self.bbbb_price)
        if self.order_cnt: self.order_cnt = float(self.order_cnt)

        return
    
    def set_prev_data(self):
        """
        def description : 과거데이터 조회
        """

        self.prev_bollinger_state = self.redis.hget_data(self.pref_bollinger_state, self.ticker)        # 볼린저 상태 값 

        
        self.prev_minimum_price = self.redis.hget_data(self.pref_minimum_price, self.ticker)             # 최저가
        self.prev_maximum_price = self.redis.hget_data(self.pref_maximum_price, self.ticker)             # 최고가

        if self.prev_minimum_price: self.prev_minimum_price = float(self.prev_minimum_price)
        if self.prev_maximum_price: self.prev_maximum_price = float(self.prev_maximum_price)

        return

    def set_current_data(self):
        """
        def description : 현재데이터 조회
        """

        # 현재 상태 조회
        self.current_price = self.upbit.get_current_price()
        self.current_bollinger_state = self.upbit.get_bollinger_state(interval="minute5")["bollinger_state"]
        
        return

    """
    UPDATE
    """
    def update_prev_data(self):
        """
        def description : 이전데이터 갱신
        """

        # 볼린저 상태 갱신
        self.redis.hupd_date(self.pref_bollinger_state, self.ticker, self.current_bollinger_state)

        # 최저가 계산 및 갱신
        price_list = []

        if self.prev_minimum_price: price_list.append(self.prev_minimum_price)
        if self.current_price: price_list.append(self.current_price)
        if self.close_price_list: 
            for close_price in self.close_price_list:
                price_list.append(close_price)
        
        self.current_minimum_price = self.upbit.get_minimum_price(price_list)
        self.redis.hupd_date(self.pref_minimum_price, self.ticker, self.current_minimum_price)

        # 최고가 계산 및 갱신
        price_list = []

        if self.prev_maximum_price: price_list.append(self.prev_maximum_price)
        if self.current_price: price_list.append(self.current_price)
        if self.close_price_list: 
            for close_price in self.close_price_list:
                price_list.append(close_price)

        self.current_maximum_price = self.upbit.get_maximum_price(price_list)
        self.redis.hupd_date(self.pref_maximum_price, self.ticker, self.current_maximum_price)
        
        return

    """
    BBBB MORNITORING
    """
    def off_bbbb(self):
        """
        def description : bbbb 대기 

        Parameters
        ----------
        """

        if self.current_bollinger_state == "below_bot" and self.prev_bollinger_state == "below_bot":
            self.pre_bbbb()
        
        # CASE : 최대가 대비 현재가가 가격변화율이 2%이하로 내려감
        elif self.upbit.get_price_change_rate_by_price(self.current_maximum_price, self.current_price) < -2:
            self.pre_bbbb()

        # CASE : 상승세 감지             
        elif self.current_bollinger_state in ("over_mid", "over_top"):
            self.redis.hdel_data(self.pref_minimum_price, self.ticker)
        
        return
    
    def pre_bbbb(self):
        """
        def description : bbbb 사전처리

        Parameters
        ----------
        """

        # Redis 갱신
        self.redis.hupd_date(self.pref_bbbb_price, self.ticker, self.current_price) 
        self.redis.hupd_date(self.pref_bbbb_status, self.ticker, "on_bbbb")
        self.redis.hdel_data(self.pref_maximum_price, self.ticker)

        # 메세지 전송
        self.slack.post_to_slack(f"무너짐이 감시 되었습니다. 모니터링을 시작합니다. {datetime.datetime.now()}")

        return

    def on_bbbb(self):
        """
        def description : bbbb 모니터링

        Parameters
        ----------
        """

        #

        # CASE : 매수 포인트 감지 
        """
        - 현재 볼린저 상태가 below_bot이면 아님
        - 이전 볼린저 상태가 below_bot이면 아님
        - 10분전 종가보다 5분전 종가가 커야함
        - bbbb당시 가격보다 1%이하로 내려와야함
        """
        if self.close_price_list[0] > 0 and\
            self.current_bollinger_state != "below_bot" and\
            self.prev_bollinger_state != "below_bot" and\
            self.close_price_list[1] > self.close_price_list[2] and\
            self.current_price < (float(self.bbbb_price) - float(self.bbbb_price) * 0.01): 

            # 매매 수량 결정
            self.krw_balance = self.upbit.get_krw_balance()

            if not self.order_cnt:
                self.order_cnt = 0.01

            # 잔고의 n%만큼 구매 
            self.krw_order = self.krw_balance * self.order_cnt
            #self.upbit.buy_coin(self.krw_order)
            
            self.post_bbbb()

        # CASE : 매수 없이 상승세 감지             
        elif self.current_bollinger_state in ("over_mid", "over_top"):

            # 레디스 초기화 
            self.redis.hdel_data(self.pref_bbbb_price, self.ticker)
            self.redis.hdel_data(self.pref_bbbb_status, self.ticker)
            self.redis.hdel_data(self.pref_bollinger_state, self.ticker)
            self.redis.hdel_data(self.pref_minimum_price, self.ticker)
            self.redis.hdel_data(self.pref_maximum_price, self.ticker)

            # 메세지 전송 (TODO : 삭제 예정)
            self.slack.post_to_slack(f"상승세를 감지하였습니다. 모니터링을 중단합니다. {datetime.datetime.now()}")

        return

    def post_bbbb(self):
        """
        def description : bbbb 사후처리

        Parameters
        ----------
        """
        if self.redis.hget_data(self.pref_bbbb_price, self.ticker):
            
            self.slack.post_to_slack(f"매수를 시행하였습니다. {datetime.datetime.now()}")

            # Redis 갱신
            self.redis.hupd_date(self.pref_order_cnt, self.ticker, (self.order_cnt + 0.01))
            self.redis.hupd_date(self.pref_bbbb_status, self.ticker, "off_bbbb")
            self.redis.hdel_data(self.pref_bbbb_price, self.ticker)
            self.redis.hdel_data(self.pref_minimum_price, self.ticker)

        return
    
    """
    MAIN SERVICE
    """
    def start(self, ticker="KRW-BTC"):
        """
        def description : 

        Parameters
        ----------
        ticker : 티커

        """


        # 티커 셋팅 
        self.ticker = ticker
        self.upbit.set_ticker(self.ticker)

        # 데이터 셋팅
        self.set_prev_data()
        self.set_current_data()
        self.set_standard_data()
        
        #self.slack.post_to_slack(f"{self.current_bollinger_state}")

        # 이전 데이터 갱신
        self.update_prev_data()

        if self.bbbb_status != "on_bbbb":
            self.off_bbbb()
            
        else:
            self.on_bbbb()

        return 