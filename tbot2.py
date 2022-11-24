import telebot
from googletrans import Translator
from lang import lang, langKey, isPresentLang
import requests
from extract import extract
from neuralintents import GenericAssistant

api = "YOUR API KEY"
bot = telebot.TeleBot(api)

tl = Translator()

# Part of Code Which helps in Google Translation
def translateLang(targetLang, inputText):
    t_lang = langKey(targetLang)
    result = tl.translate(inputText, dest=t_lang)
    inp_dect = lang(result.src)
    out_dect = lang(result.dest)
    return f"Translated text : {result.text}\nPronunciation : {result.pronunciation}\nInput language detected : {inp_dect}\nOutput language : {out_dect}"

def translateLangDefault(inputText):
    result = tl.translate(inputText, dest="hi")
    inp_dect = lang(result.src)
    out_dect = lang(result.dest)
    return f"Translated text : {result.text}\nPronunciation : {result.pronunciation}\nInput language detected : {inp_dect}\nOutput language : {out_dect}"



# General Functions
@bot.message_handler(commands=['help']) # help message handler
def send_welcome(message):
    bot.send_message(message.chat.id, "I think the following stuff can help you!\n\nCommands List:\n/help -> To get the help\n/start -> To start\n/send -> To send something\n/gfg -> GeeksforGeeks\n\nCool Features 😎>>>>\n\n1. For Google Translation:\nEnter the keyword 'tl' and then after type your text. And if you want to get the result in a specific language then you have to specify the language after the keyword.\nExample: Tl korean how are you?\nIf you are not specifying the language then by default it will translate the text from direct language to hindi.\n\n2. For extracting the text from images:\nJust send the image which contains text.\n(P.S. This function is little bit slow but works absolutely fine, I'm working on it)\n\n3. AI Chatting:\nYou can simply chat with the bot.\n\n Developed by: Sushant Verma (@susverma)")

@bot.message_handler(commands=['start']) # welcome message handler
def start_function(message):
    bot.reply_to(message, 'Hello, Welcome!\nType /help to get the help!')

@bot.message_handler(commands=['send']) # help message handler
def send_help(message):
    bot.reply_to(message, 'What do you want to send ? but sorry to say you this function is not implemented yet😂')

@bot.message_handler(commands=['gfg']) # help message handler
def send_gfg(message):
    bot.reply_to(message, "Welcome to geeks for geeks:\nhttps://www.geeksforgeeks.org/")


# Google Translate funcationality
def keyword_req(message):
    request = message.text.split()
    keyword = request[0]
    if len(request)<2 or keyword.lower() not in "tl":
        return False
    else:
        return True

@bot.message_handler(func=keyword_req)
def send(message):
    t = message.text.split()
    if isPresentLang(t[1].lower()):
        request = message.text.split(' ', 2)
        translated_text = translateLang(request[1].lower(), request[2])
        bot.send_message(message.chat.id, translated_text)
    else:
        request = message.text.split(' ', 1)
        translated_text = translateLangDefault(request[1])
        bot.send_message(message.chat.id, translated_text)


# Implementation of extracting the text from images when we send the image to the bot

def image_url(file_id):
    api_id = api
    r = requests.post(f'https://api.telegram.org/bot{api_id}/getFile?file_id={file_id}')
    response = r.json()
    filePath = response['result']['file_path']
    img_url = f'https://api.telegram.org/file/bot{api_id}/{filePath}'
    return img_url

@bot.message_handler(content_types=['photo'])
def test_on_image(message):
    fileId = message.photo[2].file_id
    final_image_url = image_url(fileId)
    etext = extract(final_image_url)
    bot.send_message(message.chat.id, etext)



# Reply to messages and make conversation (AI part)
assistant = GenericAssistant('intents.json', model_name="test_model")
assistant.load_model()


@bot.message_handler(func=lambda m: True)
def repeat(message):
    temp = message.text
    msg_res = assistant.request(temp)
    bot.send_message(message.chat.id, msg_res)


bot.infinity_polling()