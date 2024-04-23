from source import *


def Main() -> None:
    Thread(target=AnnualCheck, daemon=True).start()
    while True:
        try:
            BOT.polling(none_stop=True, interval=1)
        except Exception as e:
            Stamp(f'In Main: {e}', 'e')
            Stamp(traceback.format_exc(), 'e')


@BOT.message_handler(content_types=['text', 'voice', 'photo', 'video', 'video_note', 'sticker'])
def TextAccept(message: telebot.types.Message) -> None:
    Stamp(f'User {message.from_user.username} sent {message.content_type}', 'i')
    if message.content_type == 'text':
        BOT.send_message(message.from_user.id, "Отправь мне любое медиа, а я скажу его ID на серверах Telegram!")
    elif message.content_type == 'voice':
        BOT.send_message(message.from_user.id, message.voice.file_id)
    elif message.content_type == 'photo':
        BOT.send_message(message.from_user.id, message.photo[-1].file_id)
    elif message.content_type == 'video':
        BOT.send_message(message.from_user.id, message.video.file_id)
    elif message.content_type == 'video_note':
        BOT.send_message(message.from_user.id, message.video_note.file_id)
    elif message.content_type == 'sticker':
        BOT.send_message(message.from_user.id, message.sticker.file_id)


def AnnualCheck():
    while True:
        try:
            cur_time = datetime.now().strftime('%d.%m.%Y %H:%M')
            data = GetSector(SCAN[0], SCAN[1], SERVICE, 'Расписание', SHEET_ID)
            for row in data:
                if cur_time == row[0] + ' ' + row[1]:
                    ids = row[COL_IDS].split(',')
                    Stamp(f"Sending message to {'/'.join(ids)}", 'i')
                    for id_channel in ids:
                        if row[COL_PHOTO] != '-':
                            BOT.send_photo(id_channel, row[COL_PHOTO])
                        if row[COL_VIDEO] != '-':
                            BOT.send_video(id_channel, row[COL_VIDEO])
                        if row[COL_CIRCLE] != '-':
                            BOT.send_video_note(id_channel, row[COL_CIRCLE])
                        if row[COL_VOICE] != '-':
                            BOT.send_voice(id_channel, row[COL_VOICE])
                        if row[COL_STICKER] != '-':
                            BOT.send_sticker(id_channel, row[COL_STICKER])
                        if row[COL_MSG] != '-':
                            if row[COL_LINK_URL] != '-' and row[COL_LINK_TEXT] != '-':
                                markup = telebot.types.InlineKeyboardMarkup()
                                markup.add(telebot.types.InlineKeyboardButton(row[COL_LINK_TEXT], row[COL_LINK_URL]))
                                BOT.send_message(id_channel, row[COL_MSG], reply_markup=markup)
                            else:
                                BOT.send_message(id_channel, row[COL_MSG])
        except Exception as e:
            Stamp(f'IN AnnualCheck: {e}', 'e')
            Stamp(traceback.format_exc(), 'e')
        finally:
            Sleep(60)


if __name__ == '__main__':
    Main()
