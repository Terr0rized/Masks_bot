import telebot
import string
from telebot import types
from string import Template

token = "931022177:AAERo_5S-vHY0PAw0Xz1U9IaKVdDTgsVd-o"
bot = telebot.TeleBot(token)

entry = {}

dist = {
    'oct':{'name':[], 'adress':[], 'maski':[]},
    'sver':{'name':[], 'adress':[], 'maski':[]},
    'len':{'name':[], 'adress':[], 'maski':[]},
    'perv':{'name':[], 'adress':[], 'maski':[]},
}


class User():
    def __init__(self, account):   
        self.account = account

        keys = [
            'proff',
            'farm_in_bish_dist',
            'farm_dist',
            'farm_name',
            'farm_adress',
            'masok_in_farm',
            'find',
        ]
    
        for key in keys:
            self.key = None


@bot.message_handler(commands=["start"])
def func_user(message):
    try:
        chat_id = message.chat.id
        entry[chat_id] = User(message.text)

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        button1 = types.KeyboardButton("Продавец-Фармацеевт")
        button2 = types.KeyboardButton("Покупатель")
        markup.add(button1, button2)
        msg = bot.send_message(message.chat.id, 'Кто вы?', reply_markup=markup)
        bot.register_next_step_handler(msg, proccess_proff)
    except Exception as e:
        print(e)

def proccess_proff(message):
    try:
        chat_id = message.chat.id
        user = entry[chat_id]
        user.proff = message.text
        print(user.proff)
        if user.proff == "Покупатель":
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            button1 = types.KeyboardButton('Аптеки в районах Бишкека')
            button2 = types.KeyboardButton('Поиск маски по названию и адресу')
            button3 = types.KeyboardButton('Назад')
            markup.add(button1, button2, button3)


            msg = bot.send_message(chat_id, "Что вам надо?", reply_markup=markup)
            bot.register_next_step_handler(msg, proccess_farm_in_bish_dist)
        
            
        if user.proff == "Продавец-Фармацеевт":
            chat_id = message.chat.id
            user = entry[chat_id]
            keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            btn1 = types.KeyboardButton('Октябрьский')
            btn2 = types.KeyboardButton('Свердловский')
            btn3 = types.KeyboardButton('Ленинский')
            btn4 = types.KeyboardButton('Первомайский')
            keyboard.add(btn1, btn2, btn3, btn4)
            msg = bot.send_message(chat_id, "Укажите ваш район: ", reply_markup=keyboard)
            bot.register_next_step_handler(msg, proccess_farm_dist)
    except Exception as e:
        print(e)

# poisk
@bot.message_handler(content_types=['text'])
def proccess_find(message):
    try:
        chat_id = message.chat.id
        user = entry[chat_id]
        user.find = message.text.lower()
        if len(user.find) < 3:
            bot.send_message(chat_id, "Попробуйте другое слово, я вас не понял")
        else:
            new_name_list = []
            new_adress_list = []
            new_maski_list = []
            for name in dist['oct']['name']:
                new_name_list.append(name)
            for name1 in dist['sver']['name']:
                new_name_list.append(name1)
            for name2 in dist['len']['name']:
                new_name_list.append(name2)
            for name3 in dist['perv']['name']:
                new_name_list.append(name3)
            for adress in dist['oct']['adress']:
                new_adress_list.append(adress)
            for adress2 in dist['sver']['adress']:
                new_adress_list.append(adress2)
            for adress3 in dist['len']['adress']:
                new_adress_list.append(adress3)
            for adress4 in dist['perv']['adress']:
                new_adress_list.append(adress4)
            for maska in dist['oct']['maski']:
                new_maski_list.append(maska)
            for maska2 in dist['sver']['maski']:
                new_maski_list.append(maska2)
            for maska3 in dist['len']['maski']:
                new_maski_list.append(maska3)
            for maska4 in dist['perv']['maski']:
                new_maski_list.append(maska4)
            some_list = zip(new_name_list, new_adress_list, new_maski_list)
            print(some_list)
            # if user.find in some_list:
            new_list = [x for x in string.ascii_letters]
            for item in some_list:
                item = list(item)
                print(item)
                for word in item:
                    if word.startswith(user.find) or user.find in new_list:
                        msg = bot.send_message(chat_id, f"Аптека: {item[0]}\nАдрес: {item[1]}\nКол-во масок {item[2]}")          
    except Exception as e:
        print(e)

# Seller
def proccess_farm_dist(message):
    try:
        chat_id = message.chat.id
        user = entry[chat_id]
        user.farm_dist = message.text
        if user.farm_dist == "Октябрьский":
            msg = bot.send_message(chat_id, "Название вашей аптеки: ")
            bot.register_next_step_handler(msg, proccess_farm_name_oct)
        if user.farm_dist == "Свердловский":
            msg = bot.send_message(chat_id, "Название вашей аптеки: ")
            bot.register_next_step_handler(msg, proccess_farm_name_sver)
        if user.farm_dist == "Ленинский":
            msg = bot.send_message(chat_id, "Название вашей аптеки: ")
            bot.register_next_step_handler(msg, proccess_farm_name_len)
        if user.farm_dist == "Первомайский":
            msg = bot.send_message(chat_id, "Название вашей аптеки: ")
            bot.register_next_step_handler(msg, proccess_farm_name_perv)
    except Exception as e:
        print(e)

# Seller
def proccess_farm_name_oct(message):
    try:
        chat_id = message.chat.id
        user = entry[chat_id]
        user.farm_name = message.text.lower()
        dist['oct']['name'].append(user.farm_name)
        print(dist.items())
        msg = bot.send_message(chat_id, "Введите адрес аптеки: ")
        bot.register_next_step_handler(msg, proccess_farm_adress_oct)
    except Exception as e:
        print(e)

# Seller
def proccess_farm_name_sver(message):
    try:
        chat_id = message.chat.id
        user = entry[chat_id]
        user.farm_name = message.text.lower()
        dist['sver']['name'].append(user.farm_name)
        print(dist.items())
        msg = bot.send_message(chat_id, "Введите адрес аптеки: ")
        bot.register_next_step_handler(msg, proccess_farm_adress_sver)
    except Exception as e:
        print(e)

# Seller
def proccess_farm_name_len(message):
    try:
        chat_id = message.chat.id
        user = entry[chat_id]
        user.farm_name = message.text.lower()
        dist['len']['name'].append(user.farm_name)
        print(dist.items())
        msg = bot.send_message(chat_id, "Введите адрес аптеки: ")
        bot.register_next_step_handler(msg, proccess_farm_adress_len)
    except Exception as e:
        print(e)

# Seller
def proccess_farm_name_perv(message):
    try:
        chat_id = message.chat.id
        user = entry[chat_id]
        user.farm_name = message.text.lower()
        dist['perv']['name'].append(user.farm_name)
        print(dist.items())
        msg = bot.send_message(chat_id, "Введите адрес аптеки: ")
        bot.register_next_step_handler(msg, proccess_farm_adress_perv)
    except Exception as e:
        print(e)

# Seller
def proccess_farm_adress_oct(message):
    try:
        chat_id = message.chat.id
        user = entry[chat_id]
        user.farm_adress = message.text.lower()
        dist['oct']['adress'].append(user.farm_adress)
        print(dist.items())
        msg = bot.send_message(chat_id, "Укажите кол-во масок: ")
        bot.register_next_step_handler(msg, proccess_masok_in_farm_oct)
    except Exception as e:
        print(e)

# Seller
def proccess_farm_adress_sver(message):
    try:
        chat_id = message.chat.id
        user = entry[chat_id]
        user.farm_adress = message.text.lower()
        dist['sver']['adress'].append(user.farm_adress)
        print(dist.items())
        msg = bot.send_message(chat_id, "Укажите кол-во масок: ")
        bot.register_next_step_handler(msg, proccess_masok_in_farm_sver)
    except Exception as e:
        print(e)

# Seller
def proccess_farm_adress_len(message):
    try:
        chat_id = message.chat.id
        user = entry[chat_id]
        user.farm_adress = message.text.lower()
        dist['len']['adress'].append(user.farm_adress)
        print(dist.items())
        msg = bot.send_message(chat_id, "Укажите кол-во масок: ")
        bot.register_next_step_handler(msg, proccess_masok_in_farm_len)
    except Exception as e:
        print(e)

# Seller
def proccess_farm_adress_perv(message):
    try:
        chat_id = message.chat.id
        user = entry[chat_id]
        user.farm_adress = message.text.lower()
        dist['perv']['adress'].append(user.farm_adress)
        print(dist.items())
        msg = bot.send_message(chat_id, "Укажите кол-во масок: ")
        bot.register_next_step_handler(msg, proccess_masok_in_farm_perv)
    except Exception as e:
        print(e)

# Seller
def proccess_masok_in_farm_oct(message):
    try:
        chat_id = message.chat.id
        user = entry[chat_id]
        user.masok_in_farm = message.text
        dist['oct']['maski'].append(user.masok_in_farm)
        print(dist.items())
        bot.send_message(chat_id, getRegData(user, "Ваша заявка", message.from_user.first_name), parse_mode="Markdown")
    except Exception as e:
        print(e)

# Seller
def proccess_masok_in_farm_sver(message):
    try:
        chat_id = message.chat.id
        user = entry[chat_id]
        user.masok_in_farm = message.text
        dist['sver']['maski'].append(user.masok_in_farm)
        print(dist.items())
        bot.send_message(chat_id, getRegData(user, "Ваша заявка", message.from_user.first_name), parse_mode="Markdown")
    except Exception as e:
        print(e)

# Seller
def proccess_masok_in_farm_len(message):
    try:
        chat_id = message.chat.id
        user = entry[chat_id]
        user.masok_in_farm = message.text
        dist['len']['maski'].append(user.masok_in_farm)
        print(dist.items())
        bot.send_message(chat_id, getRegData(user, "Ваша заявка", message.from_user.first_name), parse_mode="Markdown")
    except Exception as e:
        print(e)

# Seller
def proccess_masok_in_farm_perv(message):
    try:
        chat_id = message.chat.id
        user = entry[chat_id]
        user.masok_in_farm = message.text
        dist['perv']['maski'].append(user.masok_in_farm)
        print(dist.items())
        bot.send_message(chat_id, getRegData(user, "Ваша заявка", message.from_user.first_name), parse_mode="Markdown")
    except Exception as e:
        print(e)

# Seller
def getRegData(user, title, name):
    try:
        t = Template('$title *$name* \n Название: *$name* \n Адрес: *$adress* \n Маски: *$maski*')
        return t.substitute({
            'title': title,
            'name': name,
            'UserAccount': user.account,
            'name': user.farm_name,
            'adress': user.farm_adress,
            'maski': user.masok_in_farm,
        })
    except Exception as e:
        print(e)

    


def proccess_farm_in_bish_dist(message):
    chat_id = message.chat.id
    user = entry[chat_id]
    user.farm_in_bish_dist = message.text
    print(user.farm_in_bish_dist)
    markup = types.ReplyKeyboardRemove(selective=False)

    if user.farm_in_bish_dist == 'Аптеки в районах Бишкека':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        button1 = types.KeyboardButton('Октябрьский')
        button2 = types.KeyboardButton('Свердловский')
        button3 = types.KeyboardButton('Ленинский')
        button4 = types.KeyboardButton('Первомайский')
        button5 = types.KeyboardButton('Назад')
        markup.add(button1, button2, button3, button4, button5)
        msg = bot.send_message(chat_id, "Выберите район", reply_markup=markup)
        bot.register_next_step_handler(msg, proccess_oct_dist)

    if user.farm_in_bish_dist == "Поиск маски по названию и адресу":
        msg = bot.send_message(chat_id, "Поиск по ключевым словам")
        bot.register_next_step_handler(msg, proccess_find)

    if user.farm_in_bish_dist == "Назад":
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        button1 = types.KeyboardButton("Продавец-Фармацеевт")
        button2 = types.KeyboardButton("Покупатель")
        markup.add(button1, button2)
        msg = bot.send_message(message.chat.id, 'Кто вы?', reply_markup=markup)
        bot.register_next_step_handler(msg, proccess_proff)

def proccess_oct_dist(message):
    try:
        chat_id = message.chat.id
        user = entry[chat_id]
        user.oct_dist = message.text
        if user.oct_dist == "Назад":
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            button1 = types.KeyboardButton('Аптеки в районах Бишкека')
            button2 = types.KeyboardButton('Поиск маски по названию и адресу')
            button3 = types.KeyboardButton('Назад')
            markup.add(button1, button2, button3)

            msg = bot.send_message(chat_id, "Что вам надо?", reply_markup=markup)
            bot.register_next_step_handler(msg, proccess_farm_in_bish_dist)

        if user.oct_dist == "Октябрьский":
            new_name_list = []
            new_adress_list = []
            new_maski_list = []
            for name in dist['oct']['name']:
                new_name_list.append(name)
            for adress in dist['oct']['adress']:
                new_adress_list.append(adress)
            for maska in dist['oct']['maski']:
                new_maski_list.append(maska)
            some_list = zip(new_name_list, new_adress_list, new_maski_list)
            for item in some_list:
                msg = bot.send_message(chat_id, f"Аптека: {item[0]}\nАдрес: {item[1]}\nКол-во масок {item[2]}")
                bot.register_next_step_handler(msg, proccess_proff)
        if user.oct_dist == "Свердловский":
            new_name_list = []
            new_adress_list = []
            new_maski_list = []
            for name in dist['sver']['name']:
                new_name_list.append(name)
            for adress in dist['sver']['adress']:
                new_adress_list.append(adress)
            for maska in dist['sver']['maski']:
                new_maski_list.append(maska)
            some_list = zip(new_name_list, new_adress_list, new_maski_list)
            for item in some_list:
                bot.send_message(chat_id, f"Аптека: {item[0]}\nАдрес: {item[1]}\nКол-во масок {item[2]}") 
        if user.oct_dist == "Ленинский":
            new_name_list = []
            new_adress_list = []
            new_maski_list = []
            for name in dist['len']['name']:
                new_name_list.append(name)
            for adress in dist['len']['adress']:
                new_adress_list.append(adress)
            for maska in dist['len']['maski']:
                new_maski_list.append(maska)
            some_list = zip(new_name_list, new_adress_list, new_maski_list)
            for item in some_list:
                bot.send_message(chat_id, f"Аптека: {item[0]}\nАдрес: {item[1]}\nКол-во масок {item[2]}") 
        if user.oct_dist == "Первомайский":
            new_name_list = []
            new_adress_list = []
            new_maski_list = []
            for name in dist['perv']['name']:
                new_name_list.append(name)
            for adress in dist['perv']['adress']:
                new_adress_list.append(adress)
            for maska in dist['perv']['maski']:
                new_maski_list.append(maska)
            some_list = zip(new_name_list, new_adress_list, new_maski_list)
            for item in some_list:
                bot.send_message(chat_id, f"Аптека: {item[0]}\nАдрес: {item[1]}\nКол-во масок {item[2]}") 
    except Exception as e:
        print(e)


if __name__ == "__main__":
    bot.polling()