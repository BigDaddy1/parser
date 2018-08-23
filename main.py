import csv
import json
import uuid
import os
import telebot
import codecs

TOKEN = '658936679:AAHoaKMllCnyL5BJKIRx7ge31CJmFamwQio'

CURRENT_STEP = 0

if __name__ == "__main__":

    bot = telebot.TeleBot(TOKEN)
    types = telebot.types
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                         one_time_keyboard=True)

    @bot.message_handler(commands=['start'])
    def process_start(message):
        bot.send_message(message.chat.id, "Nahui!")


    @bot.message_handler(content_types=['text', 'audio', 'photo'])
    def process_start(message):
        bot.send_message(message.chat.id, "Nahui twice!")


    @bot.message_handler(commands=['show_all'])
    def time_process(message):
        pass

    @bot.message_handler(content_types=['document'])
    def location_process(message):
        file_list_keys = open('list.json', 'r')
        origin_keys = file_list_keys.read()
        origin_keys_data = json.loads(origin_keys)
        keys_guids = origin_keys_data.keys()
        file_id = message.document.file_id

        file = bot.get_file(file_id)
        file_data = bot.download_file(file.file_path)
        x = json.loads(file_data.decode())
        answ = list()
        count = 0
        error_time = None
        try:
            for i in x['gameBasket']['inventory']:

                couplers = list()
                if 'moniker' in i[2].keys():
                    if 'differentiator' in i[2]['moniker'].keys():
                            count+=1
                            for stack_item in i[2]['container']['stackableItems']:
                                if 'portalCoupler' in \
                                        stack_item['exampleGameEntity'][2]:
                                    for a in stack_item['itemGuids']:
                                        error_time = stack_item['exampleGameEntity'][2]
                                        d = stack_item['exampleGameEntity'][2][
                                            'portalCoupler']
                                        d.update({'differentiator': i[2]['moniker'][
                                            'differentiator']})
                                        couplers.append(d)
                            answ.append(couplers)
            file_name = '{}.csv'.format(uuid.uuid4().hex)
            f = open(file_name, "w")
            f.write('portalTitle,,portalGuid,differentiator,codename')
            f.write('\n')

            print(count)
            count = 0
            for item in answ:
                count += len(item)
                for i in item:
                    s = i
                    codename = ' '
                    if i['portalGuid'] in keys_guids:
                        codename = origin_keys_data[
                            i['portalGuid']]['codename']
                    s.update({'codename': codename})
                    f.write('{},{},{},{}'.format(
                    s['portalTitle'],
                    s['portalGuid'],
                    s['differentiator'],
                    s['codename']
                    ))
                    f.write('\n')
            f.close()

            file_data = open(file_name, 'rb')
            bot.send_document(message.chat.id, file_data)
            file_data.close()
            os.remove(file_name)
            print(count)
        except Exception as e:
            print(error_time)
            print(e)

    # while True:
    try:
        bot.polling()
    except Exception as e:
        bot.stop_polling()

        print(e)
