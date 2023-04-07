from app.main.commons.classes.mysql import *
from app.main.commons.classes.upbit import *


class Skills():

    def __init__(self):
        self.mysql = Mysql()
        self.upbit = Upbit()


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


    def night_owl_protocol(self):
        """
        솔라나 요청 오면 
        솔라나 관련 hdate 다 지워버리고 
        
        
        """

        # 나이트 오울 특정 티커 관련 된 레디스를 다 지워버리고 

        # 나이트 오울 티커에 담아서 
        return

    def highnoon_eagle_protocol(self):
        return