Aim: A proof of concept for Dialogflow as a suitable and simple NLP component to Messenger, Whatsapp, Viber or Telegram bots.

Outcome: I built a simple Flask app response_handler.py to function as a webhook. A RapidPro flow calls the webhook, passing the text of an unknown response along as a query parameter. The Flask app routes the text to Rasa nlu, which does intent detection and parameter extraction. The response from Rasa nlu is then returned to the RapidPro flow.
