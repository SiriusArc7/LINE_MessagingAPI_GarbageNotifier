import os
import time
import logging
import schedule
from datetime import datetime as dt
from dotenv import load_dotenv
from linebot.v3.messaging import (
    Configuration,
    MessagingApi,
    ApiClient,
    PushMessageRequest,
    TextMessage,
)
from linebot.v3.messaging.exceptions import ApiException

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
USER_ID = os.environ.get("LINE_USER_ID")

if not CHANNEL_ACCESS_TOKEN or not USER_ID:
    raise ValueError("LINE_CHANNEL_ACCESS_TOKEN と LINE_USER_ID の設定が必要です")

configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)

def send_message(text: str) -> None:
    try:
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            message = TextMessage(text=text)
            request = PushMessageRequest(to=USER_ID, messages=[message])
            line_bot_api.push_message(request)
        logger.info(f"メッセージ送信成功: {text}")
    except ApiException as e:
        logger.error(f"LINE API エラー: {e}")
    except Exception as e:
        logger.error(f"予期しないエラー: {e}")

def schedule_message() -> None:
    now = dt.now()
    weekday = now.weekday()   # Mon=0 ... Sun=6
    day = now.day

    if weekday == 3:  # 木曜の夜
        send_message("[ゴミ捨て通知]明日は資源ゴミの日です。Powered By GCP")
    elif weekday in (2, 6):  # 水曜と日曜の夜
        send_message("[ゴミ捨て通知]明日は燃えるゴミの日です。Powered By GCP")
    elif weekday == 0 and (8 <= day <= 14 or 22 <= day <= 28):  # 月曜の夜
        send_message("[ゴミ捨て通知]明日は燃えないゴミの日です。Powered By GCP")

schedule.every().day.at("21:00").do(schedule_message)

while True:
    schedule.run_pending()
    time.sleep(1)