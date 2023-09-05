import sys
sys.path.append('/var/www/coin_village/cron')

from module.redis import *
from module.slack import *

rs = Redis()
sl = Slack()

msg_json = rs.hgetall_data("msg_group_B")

if msg_json:

    msg_str = ""
    for key, value in msg_json.items():
        msg_str += f"{key} : {value}\n"

    if len(msg_str) > 0:
        sl.post_msg(msg_str)