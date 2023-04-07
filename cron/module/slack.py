import os
import json
import requests
import slack_sdk
from dotenv import load_dotenv
load_dotenv()


class Slack():

    def __init__(self):
        self.slack_client = slack_sdk.WebClient(token=os.getenv("SLACK_TOKEN"))

    def post_to_slack(self, msg):
        """ 
        def description : 슬랙 메세지 전송 

        Parameters
        ----------
        msg = 메세지

        Returns
        -------
        response_object : 결과 오브젝트 (dict)
        """
        self.slack_client.chat_postMessage(
            channel='#coinvillage',
            text=msg

        )
        # response = requests.post(
        #     self.webhook_url, data=slack_data,
        #     headers={"Content-Type": "application/json"}
        # )

        # if response.status_code != 200:
        #     response_object = {
        #         "status": "fail",
        #         "message": str(response.text)
        #     }
        #     return response_object

        response_object = {
            "status": "success",
            "message": "success"
        }
        return response_object
