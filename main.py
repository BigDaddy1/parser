import csv
import json
import uuid
import os
import telebot
import codecs

TOKEN = '658936679:AAHoaKMllCnyL5BJKIRx7ge31CJmFamwQio'

CURRENT_STEP = 0
message_id = 129488891


if __name__ == "__main__":
    stopped = False
    bot = telebot.TeleBot(TOKEN)
    types = telebot.types
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                         one_time_keyboard=True)

    @bot.message_handler(commands=['start'])
    def process_start(message):
        bot.send_message(message.chat.id, "Nahui!")

 #    @bot.message_handler(commands=['stop_please'])
#    def process_stop(message):
#        global stopped
#        stopped = True
#        exit(0)

    @bot.message_handler(content_types=['text', 'audio', 'photo'])
    def process_start(message):
        bot.send_message(message.chat.id, "Nahui twice!")


    @bot.message_handler(content_types=['document'])
    def location_process(message):
        try:
            print('DOCUMEEEEEEEENT')
            chat_ids = open('chat_ids', 'a')
            chat_ids.write('{}\n'.format(message.chat.id))
            chat_ids.close()
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
                                count += 1
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
                f.write('codename,portalTitle,differentiator')
                f.write('\n')

                count = 0
                for item in answ:
                    count += len(item)
                    for i in item:
                        s = i
                        codename = ''
                        if i['portalGuid'] in keys_guids:
                            codename = origin_keys_data[
                                i['portalGuid']]['codename']
                        s.update({'codename': codename})
                        title = '_' if s['portalTitle'] == '' else s['portalTitle'].replace(',', '.')
                        differ = '_' if s['differentiator'] == '' else s['differentiator'].replace(',', '.')
                        code = '_' if s['codename'] == '' else s['codename'].replace(',', '.')
                        f.write('{},{},{}'.format(code, title, differ))
                        f.write('\n')
                f.close()

                file_data = open(file_name, 'rb')
                bot.send_document(message.chat.id, file_data)
                file_data.close()
                os.remove(file_name)
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)
    def start_me():
        try:
            bot.polling()
            with open('logger', 'w+') as logger:
                logger.write('polling...')
        except Exception as e:
            with open('logger', 'w+') as logger:
                logger.write(e)
            bot.send_message(message_id, e)
            bot.stop_polling()
            print(e)
            start_me()

    with open('logger', 'w+') as logger:
        logger.write('starting...')
    start_me()
    #
    # while True:
    #     try:
    #         bot.polling()
    #     except Exception as e:
    #         bot.send_message(message_id, e)
    #         bot.stop_polling()
    #         print(e)
