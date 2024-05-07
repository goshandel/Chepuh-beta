import telebot as telebot

from config import token
from database import Database
from gpt import Question_gpt2, count_tokens
from speak import text_to_speech, speech_to_text


#"6024803621:AAGmLrTzC1i998cYjdawslKDvDuBxFc4EYo"
bot = telebot.TeleBot(token=token)

@bot.message_handler(commands=["start"])
def challenge_to_duel(message):
    db = Database()
    users = db.get_total_users_count()
    if not db.check_user_exists(message.chat.id) and users < 5:
        db.add_user(message.chat.id, message.chat.first_name, message.chat.username)
    else:
        bot.send_message(message.chat.id, "а тебя не хватило мест!")
    db.close()
    bot.send_message(message.chat.id, "Привет!!!\nЭто тестовая версия чепуха(гоше лень переносить от сюда всё в основного бота)\n/help")

@bot.message_handler(commands=["help"])
def challenge_to_duel(message):
    bot.send_message(message.chat.id,"здесь ничего нет проработанного: смайликов, приколов и тд.\n\n<b>Чепух-тест</b> это <i>младший брат</i> <b>чепух</b>\n\n/help\n/speak\n/text\n/GPT", parse_mode='html')
    db = Database()
    speech_blocks = db.check_blocks(message.chat.id)
    text_tokens = db.get_tokens(message.chat.id)
    gpt_tokens = db.check_gpt_tokens(message.chat.id)
    bot.send_message(message.chat.id,
                     f"твои токены:\nТокны для запроса к гпт: {gpt_tokens}\nТокены для распознования речи: {speech_blocks}\nТокены для синтеза речи: {text_tokens}")
    db.close()
@bot.message_handler(commands=["speak"])
def challenge_to_duel(message):
    db = Database()
    if not db.check_user_exists(message.chat.id):
        bot.send_message(message.chat.id, "ты не можешь поьзоваться")
        return
    tokens = db.get_tokens(message.chat.id)
    db.close()
    bot.send_message(message.chat.id, f"у тебя {tokens} символов\n\nвведи текст который хочешь чтоб длыдмсчлыс:")
    bot.register_next_step_handler(message, send_to)

def  send_to(message):
    text = message.text
    db = Database()
    tokens = db.get_tokens(message.chat.id)
    db.close()
    if len(text) > 200 or len(text) > tokens:
        bot.send_message(message.chat.id, "много бкв")
        bot.register_next_step_handler(message, send_to)
        return
    else:
        db = Database()
        db.add_message(message.chat.id, text)
        db.add_tokens(message.chat.id, len(text))
        status, content = text_to_speech(text)
        if status:
            bot.send_voice(message.chat.id, content)
        else:
            bot.send_message(message.chat.id, f"ошибка ишибка: {content}")
    db.update_to_zero(message.chat.id)
    db.close()
    db = Database()
    speech_blocks = db.check_blocks(message.chat.id)
    text_tokens = db.get_tokens(message.chat.id)
    gpt_tokens = db.check_gpt_tokens(message.chat.id)
    bot.send_message(message.chat.id,
                     f"твои токены:\nТокны для запроса к гпт: {gpt_tokens}\nТокены для распознования речи: {speech_blocks}\nТокены для синтеза речи: {text_tokens}")
    db.close()


@bot.message_handler(commands=["text"])
def challenge_to_duel(message):
    db = Database()
    if not db.check_user_exists(message.chat.id):
        bot.send_message(message.chat.id, "ты не можешь поьзоваться")
        return
    db.close()
    bot.send_message(message.chat.id, 'отправь гс длинной не более 15 сек')
    bot.register_next_step_handler(message, text_to)
def text_to(message):
    if not message.voice:
        bot.send_message(message.chat.id, 'ты че?')
        return
    if message.voice.duration > 15:
        bot.send_message(message.chat.id, 'ты че?')
        return
    db = Database()
    blocks = db.check_blocks(message.chat.id)
    db.close()
    if blocks != 0:
        block = 1
        db.minus_block(message.chat.id, block)
        file_id = message.voice.file_id
        file_info = bot.get_file(file_id)
        file = bot.download_file(file_info.file_path)
        status, text = speech_to_text(file)

        if status:
            bot.send_message(message.chat.id, text, reply_to_message_id=message.id)
        else:
            bot.send_message(message.chat.id, text)
    else:
        bot.send_message(message.chat.id, "бро у тебя кончились офтощсоищгцргв")
    db = Database()
    speech_blocks = db.check_blocks(message.chat.id)
    text_tokens = db.get_tokens(message.chat.id)
    gpt_tokens = db.check_gpt_tokens(message.chat.id)
    bot.send_message(message.chat.id,
                     f"твои токены:\nТокны для запроса к гпт: {gpt_tokens}\nТокены для распознования речи: {speech_blocks}\nТокены для синтеза речи: {text_tokens}")
    db.close()

@bot.message_handler(commands=["GPT"])
def challenge_to_duel(message):
    db = Database()
    if not db.check_user_exists(message.chat.id):
        bot.send_message(message.chat.id, "ты не можешь поьзоваться")
        return
    db.close()
    bot.send_message(message.chat.id, "отправь запрос сообщением или гс:")
    bot.register_next_step_handler(message, gpt_to)
def gpt_to(message):
    if message.voice:
        blocks_in_voise = message.voice.duration // 15
        after_block = message.voice.duration % 15
        if after_block != 0:
            blocks_in_voise += 1
        db = Database()
        db.minus_block(message.chat.id, blocks_in_voise)
        blocks = db.check_blocks(message.chat.id)
        db.close()
        if blocks != 0 or blocks > blocks_in_voise :
            file_id = message.voice.file_id
            file_info = bot.get_file(file_id)
            file = bot.download_file(file_info.file_path)
            status, text = speech_to_text(file)

            if status:
                gpt = Question_gpt2()
                gpt_tokens = db.check_gpt_tokens(message.chat.id)
                tokens_to_gpt = count_tokens(text)
                if gpt_tokens < tokens_to_gpt:
                    bot.send_message(message.chat.id, "тебе не хватило токенов для запроса")
                    return
                promt = gpt.promt(text)
                db.minus_gpt_tokens(message.chat.id, tokens_to_gpt)
                db.add_message(message.chat.id, text)
                your_tokens = count_tokens(promt)
                tokens = db.get_tokens(message.chat.id)
                db.close()
                if your_tokens > 200 or your_tokens > tokens:
                    bot.send_message(message.chat.id, "много бкв, не хватило на отправку ссори")
                    bot.register_next_step_handler(message, send_to)
                    return
                db.add_tokens(message.chat.id, your_tokens)
                status, content = text_to_speech(promt)
                if status:
                    bot.send_voice(message.chat.id, content)
                else:
                    bot.send_message(message.chat.id, f"ошибка ишибка: {content}")
                db.update_to_zero(message.chat.id)
                db.close()
            else:
                bot.send_message(message.chat.id, "ошибка")
        else:
            bot.send_message(message.chat.id, "бро у тебя кончились офтощсоищгцргв")



    elif message.text:
        text = message.text
        db = Database()
        gpt = Question_gpt2()
        gpt_tokens = db.check_gpt_tokens(message.chat.id)
        tokens_to_gpt = count_tokens(text)
        if gpt_tokens < tokens_to_gpt:
            bot.send_message(message.chat.id, "тебе не хватило токенов для запроса")
            return
        db.minus_gpt_tokens(message.chat.id, tokens_to_gpt)
        db.close()
        promt = gpt.promt(text)
        bot.send_message(message.chat.id, promt)

    db = Database()
    speech_blocks = db.check_blocks(message.chat.id)
    text_tokens = db.get_tokens(message.chat.id)
    gpt_tokens = db.check_gpt_tokens(message.chat.id)
    bot.send_message(message.chat.id, f"твои токены:\nТокны для запроса к гпт: {gpt_tokens}\nТокены для распознования речи: {speech_blocks}\nТокены для синтеза речи: {text_tokens}")
    db.close()
bot.infinity_polling()


