import os

from flask import Flask, request

import telebot

TOKEN = '5760440710:AAHYt6RNmpl9O2xcKzsR8vOFx64PNvCqY78'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

def check_ask(search):
    text = open('risposte.txt','r')
    datafileTemp = text.read().split('\n')
    datafile = []
    for elem in datafileTemp:
        if elem != '':
            datafile.append(elem)
    asks = []
    answers = []
    for i in range(0,len(datafile)):
        if search in datafile[i] and datafile[i][0] != "•":
            ask = datafile[i]
            while(datafile[i+1][0] != "•"):
                ask = ask + datafile[i+1]
                i=i+1
            answer = datafile[i+1]
            asks.append(ask)
            answers.append(answer)
    return [asks,answers]


# Handle '/start'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """\
Bot per trovare la risposta alle domande del Test VCA. \n /help per info
""")


# Handle '/help'
@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, """\
Inserire LA PRIMA RIGA (o una sua sottoparte) del testo della domanda
""")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    search = message.text
    [asks, answers] = check_ask(search)
    result = ""
    if len(asks) != 0:
        for i in range(0,len(asks)):
            result = result + "\n La domanda è : \n"
            result = result + asks[i]
            result = result + "\n La risposta è : \n"
            result = result + answers[i]
    else:
        result = "Domanda non trovata"
    bot.reply_to(message, result)

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://your_heroku_project.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))