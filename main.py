from flask import Flask, request
import telebot
import os

app = Flask(__name__)
TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)

with open('courses.txt') as file:
    courses = [item.split(',') for item in file]

with open('schedule.txt') as file:
    courses_plan = {
        'start': [],
        'pro': [],
        'other': [],
    }

    for item in file:
        if 'start' in item.lower():
            courses_plan['start'].append(item)
        elif 'pro' in item.lower():
            courses_plan['pro'].append(item)
        else:
            courses_plan['other'].append(item)



@bot.message_handler(commands=['start'])
def message_start(message):
    bot.send_message(message.chat.id, 'Hello, user!')


@bot.message_handler(commands=['help'])
def help_message(message):
    res = '/courses - list of courses\n' \
          '/schedule - schedule of courses,'
    bot.reply_to(message, res)


@bot.message_handler(commands=['courses'])
def list_of_courses(message):
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)

    for text, url in courses:
        url_button = telebot.types.InlineKeyboardButton(text=text.strip(), url=url.strip(' \n'))
        keyboard.add(url_button)

    bot.send_message(message.chat.id, 'A list of courses:', reply_markup=keyboard)


@bot.message_handler(commands=['schedule'])
def list_of_courses(message):
    res = 'Schedule of courses:\n\n'

    for category in courses_plan:
        for item in courses_plan[category]:
            title, date = item.split(',')
            res += f'<b>{title}</b>: <code>{date}</code>'
        res += '\n'

    bot.send_message(message.chat.id, text=res, parse_mode='HTML')

@bot.message_handler(func=lambda x: x.text.startswith('info'))
def get_course_info(message):
    text_from_user = message.json['text']
    if 'python' in text_from_user.lower():
        res = ''
        for category in courses_plan:
            for item in courses_plan[category]:
                title, date = item.split(',')
                if 'python' in title.lower():
                    res += f'<b>{title}</b>: <code>{date}</code>'
        res += '\n'
        bot.send_message(message.chat.id, text=res, parse_mode='HTML')
    elif 'java' in text_from_user.lower():
        res = ''
        for category in courses_plan:
            for item in courses_plan[category]:
                title, date = item.split(',')
                if 'java' in title.lower():
                    res += f'<b>{title}</b>: <code>{date}</code>'
        res += '\n'
        bot.send_message(message.chat.id, text=res, parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, f'I don\'t understand you')


@app.route('/' + TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "Python Telegram Bot 24-11-2021", 200


@app.route('/')
def main():
    bot.remove_webhook()
    bot.set_webhook(url='https://chatbot23456.herokuapp.com/' + TOKEN)
    return "Python Telegram Bot", 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))