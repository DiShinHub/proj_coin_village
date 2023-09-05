from app.main.commons.classes.mysql import *
from app.main.commons.classes.upbit import *
from app.main.commons.classes.redis import *


class Cv():

    def __init__(self):
        self.mysql = Mysql()
        self.upbit = Upbit()
        self.redis = Redis()

    def percent_buy(self, req_data):
        """ 
        def description : 보유 잔고 대비 퍼센트 매수

        Returns
        response_object : 결과 (dict)
        -------
        """
        log.info(f" def: percent_buy, req_data : {req_data}")

        # 필수 값 체크
        mendatory_list = [
            "ticker",
            "trade_rate"
        ]
        for mendatory in mendatory_list:
            if mendatory not in req_data:
                raise RequiredException(msg=f"필수 값 누락입니다, *{mendatory}")

        if req_data["trade_rate"] <=0:
            raise RequiredException(msg=f"trade_rate는 0이하일 수 없습니다.")

        self.upbit.set_ticker(req_data["ticker"])

        krw_balance = self.upbit.get_krw_balance()

        if krw_balance:
            krw_order = krw_balance/(req_data["trade_rate"]/100)
            self.upbit.buy_coin(krw_order)

        # 결과
        response_object = {
            "status": "success",
            "message": "정상 처리되었습니다"
        }
        return response_object, 201

    def percent_sell(self, req_data):
        """ 
        def description : 보유 수량 대비 퍼센트 매도

        Returns
        response_object : 결과 (dict)
        -------
        """
        log.info(f" def: percent_sell, req_data : {req_data}")

        # 필수 값 체크
        mendatory_list = [
            "ticker",
            "trade_rate"
        ]
        for mendatory in mendatory_list:
            if mendatory not in req_data:
                raise RequiredException(msg=f"필수 값 누락입니다, *{mendatory}")

        if req_data["trade_rate"] <=0:
            raise RequiredException(msg=f"trade_rate는 0이하일 수 없습니다.")

        self.upbit.set_ticker(req_data["ticker"])

        target_balance = self.upbit.get_ticker_balance()

        if target_balance:
            krw_order = target_balance/(req_data["trade_rate"]/100)
            self.upbit.sell_coin(krw_order)

        # 결과
        response_object = {
            "status": "success",
            "message": "정상 처리되었습니다"
        }
        return response_object, 201

    def on_service(self, req_data):
        """ 
        def description : 서비스 on

        Returns
        response_object : 결과 (dict)
        -------
        """

        # 필수 값 체크
        mendatory_list = [
            "service_code",
            "ticker"
        ]
        for mendatory in mendatory_list:
            if mendatory not in req_data:
                raise RequiredException(msg=f"필수 값 누락입니다, *{mendatory}")
            
        key = self.convert_service_code_to_key(req_data["service_code"])

        self.redis.hset_data(key, req_data["ticker"], True)

        # 결과
        response_object = {
            "status": "success",
            "message": "정상 처리되었습니다"
        }
        return response_object, 201
    
    def off_night_owl(self, req_data):
        """ 
        def description : 밤부엉이 서비스 off

        Returns
        response_object : 결과 (dict)
        -------
        """

        # 필수 값 체크
        mendatory_list = [
            "service_code",
            "ticker"
        ]
        for mendatory in mendatory_list:
            if mendatory not in req_data:
                raise RequiredException(msg=f"필수 값 누락입니다, *{mendatory}")
        
        key = self.convert_service_code_to_key(req_data["service_code"])

        self.redis.hdel_data(key, req_data["ticker"])
        
        # 결과
        response_object = {
            "status": "success",
            "message": "정상 처리되었습니다"
        }
        return response_object, 201

    def convert_service_code_to_key(self, code):
        """ 
        def description : 코드 키 변환 

        Returns
        response_object : 결과 (dict)
        -------
        """
            
        if code == "00":
            key = "night_owls_target_tickers"
            
        elif code == "01":
            key = "high_noon_eagles_target_tickers"
            
        elif code == "02":
            key = "baby_hunter_pumas_target_tickers"
            
        elif code == "03":
            key = "good_boy_poodle_target_tickers"
        
        return key
