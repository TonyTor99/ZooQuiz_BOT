import telebot
from telebot import types
from config import TOKEN, quiz_data, questions, review, result
from functions import get_totem_animal, get_animal_photo


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
# Отправляем приветсвенное сообщение в ответ на команду start
def start(message: telebot.types.Message):
    photo = open('.\\Photos\\greet1.jpg', 'rb')
    bot.send_photo(message.chat.id, photo, caption=f'Привет {message.chat.username}! Меня зовут Манул Тимоша🐱. Я живу в Московском Зоопарке'
' и хочу помочь тебе узнать какое твое тотемное животное! А потом я сделаю тебе предложение от которого ты ну прооосто не сможешь отказаться Мур.'
' Думаю нам пора начинать. Нажми на эту кнопочку и мы начнем: /letsgo')

@bot.message_handler(commands=['letsgo'])
# Регистрируем команду letsgo, добавляем результат пользователя в словарь и начинаем викторину
def start_quiz(message):
    user_id = message.chat.id
    if user_id not in quiz_data:
        quiz_data[user_id] = {
            'current_question': 0,
            'answers': []
        }
    send_questions(user_id)

@bot.message_handler(commands=['getreview'])
def get_review(admin_id):
    admin_id = '307658038'
    for rev in review:
        bot.send_message(admin_id, rev)

def send_questions(user_id):
    user = quiz_data[user_id]
    question_index = user['current_question']
    try:
        #Отправляем вопросы пользователю, если они не закончились
        if question_index < len(questions):
            question_data = questions[question_index]
            question_text = question_data['question']
            answers = question_data['answer']

            markup = types.InlineKeyboardMarkup()
            for answer in answers.keys():
                markup.add(types.InlineKeyboardButton(text=answer, callback_data=f'{question_index}_{answer}'))
            bot.send_message(user_id, question_text, reply_markup=markup)
        else:
            #Если вопросов больше нет, то получаем результат и выводим его пользователю с ссылками на дальнейшие функции
            result[user_id] = get_totem_animal(user['answers'])
            totem_animal = get_totem_animal(user['answers'])
            photo = open(get_animal_photo(totem_animal), 'rb')

            markup_end = types.InlineKeyboardMarkup()
            markup_end.add(types.InlineKeyboardButton(text='Поделиться результатом в соцсетях', callback_data='share'))
            markup_end.add(types.InlineKeyboardButton(text='Узнать больше о Программе опеки в Московском зоопарке', url='https://moscowzoo.ru/about/guardianship'))
            markup_end.add(types.InlineKeyboardButton(text='Оставить отзыв', callback_data='review'))
            markup_end.add(types.InlineKeyboardButton(text='Задать вопрос сотруднику Зоопарка', callback_data='question'))
            markup_end.add(types.InlineKeyboardButton(text='Пройти викторину заново', callback_data='replay'))

            bot.send_photo(user_id, photo, f'ВАААУ! Твоё тотемное животное это - {result[user_id]}!!! Знаешь ведь, что своим близким по духу нужно помогать? Конееечно знаешь!'
    f'Так вот. Хочу предложить тебе стать его опекуном. Всю информацию о данном проекте, и еще кое что, ты сможешь найти по ссылочке ниже', reply_markup=markup_end)
    except TypeError:
        quiz_data[user_id]['current_question'] = 0
        quiz_data[user_id]['answers'] = []
        bot.send_message(user_id, 'Произошла ошибка( Попробуйте еще раз')

# Ловим ответы пользователя
@bot.callback_query_handler(func=lambda call: '_' in call.data)
def callback_query1(call):
    user_id = call.message.chat.id
    user = quiz_data[user_id]

    question_index, user_answer = call.data.split('_')
    question_index = int(question_index)

    user['answers'].append(user_answer)
    user['current_question'] = question_index + 1
    send_questions(user_id)

# Ловим нажатия кнопок перезапуска, оставления отзыва и сообщения сотруднику Зоопарка
@bot.callback_query_handler(func=lambda call: call.data == 'replay' or call.data == 'review' or call.data == 'question')
def replay_review(call):
    user_id = call.message.chat.id
    if 'replay' == call.data:
        if user_id in quiz_data:
            del result[user_id]
            quiz_data[user_id]['current_question'] = 0
            quiz_data[user_id]['answers'] = []
            send_questions(user_id)
        else:
            bot.send_message(user_id, "Нет активной викторины для перезапуска.")

    if 'review' == call.data:
        mesg = bot.send_message(user_id, 'Оставьте отзыв в графе сообщения\nЭто поможет нам стать лучше для вас)\nЭто полностью анонимно')
        bot.register_next_step_handler(mesg, add_review)

    if 'question' == call.data:
        ques = bot.send_message(user_id, 'Введите ваш вопрос в графе сообщения в формате:\n<Ваш вопрос>\n<@UserName для обратной связи>')
        bot.register_next_step_handler(ques, send_ques)

def add_review(message):
    review.append(message.text)
    bot.send_message(message.chat.id, 'Спасибо за оставленный отзыв!')

def send_ques(message):
    user_id = message.chat.id
    admin_id = '307658038'
    ques = f'Результат викторины: {result[user_id]}\nСообщение: {message.text}'
    bot.send_message(chat_id=admin_id, text=ques)
    bot.send_message(user_id, 'Ваше сообщение успешно отправлено!')

# Ловим нажатие кнопки поделисться
@bot.callback_query_handler(func=lambda call: call.data == 'share')
def share_result(call):
    user = quiz_data[call.message.chat.id]
    totem_animal = get_totem_animal(user['answers'])
    user_id = call.message.chat.id
    result[user_id] = get_totem_animal(quiz_data[user_id]['answers'])
    photo = open(get_animal_photo(totem_animal), 'rb')
    message_text = f'Мое тотемное животное {result[user_id]}! Пройди викторину и узнай своё тотемное животное!\nhttps://t.me/MosZooQuiz_BOT'

    share_mark = types.InlineKeyboardMarkup()
    share_mark.row(types.InlineKeyboardButton('Поделиться в Телеграм', switch_inline_query=message_text))
    share_mark.row(types.InlineKeyboardButton('Поделиться во Вконтакте', url=f'https://vk.com/share.php?url=https://ltdfoto.ru/image/hneZiU&title={message_text}'))

    bot.send_photo(user_id, photo, caption=message_text, reply_markup=share_mark)


bot.polling(none_stop=True)
