from flask import Flask, request, abort

from linebot import (
   LineBotApi, WebhookHandler
)
from linebot.exceptions import (
   InvalidSignatureError
)
from linebot.models import (
   MessageEvent, TextMessage, TextSendMessage,
)

import os
import hotel

app = Flask(__name__)

YOUR_CHANNEL_ACCESS_TOKEN = os.environ["Et/ne8oRDkSzx2e0GAwgQUsywwOjp6Qamp3INPojV9rFhTkRgPffAEW+lVAERpWSybY6FRLrIma2ZjpprNnteMtBXVUshQdNeE86RetHzLxh5Th1mMKWf/l2ZdiPhXMiiDuIw6uUngls6XtUtGsekQdB04t89/1O/w1cDnyilFU="]
YOUR_CHANNEL_SECRET = os.environ["c435a6688826c9192f45da5027f52aaa"]
//apiver1 heroku名
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/")
def hello_world():
   return "hello world!"

@app.route("/callback", methods=['POST'])
def callback():
   # get X-Line-Signature header value
   signature = request.headers['X-Line-Signature']

   # get request body as text
   body = request.get_data(as_text=True)
   app.logger.info("Request body: " + body)

   # handle webhook body
   try:
       handler.handle(body, signature)
   except InvalidSignatureError:
       print("Invalid signature. Please check your channel access token/channel secret.")
       abort(400)

   return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
   push_text = event.message.text
   results = hotel.extract_words(push_text)
   if isinstance(results, tuple):
       msg = hotel.hotel_search(*results)
   else:
       msg = results
   line_bot_api.reply_message(event.reply_token,TextSendMessage(text=msg))

if __name__ == "__main__":
   port = int(os.getenv("PORT"))
   app.run(host="0.0.0.0", port=port)