import telebot.types

from source import *


def Main() -> None:
    Thread(target=AnnualCheck, daemon=True).start()
    while True:
        try:
            BOT.polling(none_stop=True, interval=1)
        except Exception as e:
            Stamp(f'In Main: {e}', 'e')
            BOT.send_message(LOG_ID, f'ERROR in Main: {e}')
            Stamp(traceback.format_exc(), 'e')


@BOT.message_handler(content_types=['text', 'voice', 'photo', 'video', 'video_note', 'sticker', 'animation'])
def TextAccept(message: telebot.types.Message) -> None:
    Stamp(f'User {message.from_user.username} sent {message.content_type}', 'i')
    users = GetSector('A2', 'A100', SERVICE, 'Пользователи', SHEET_ID)
    users = [item for sublist in users for item in sublist]
    if message.from_user.username in users:
        if message.content_type == 'text':
            BOT.send_message(message.from_user.id, "Send me any media and get its ID on Telegram servers!")
            BOT.send_message(message.from_user.id, f'Chat ID: {message.chat.id}, Message ID: {message.message_id}')
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
        elif message.content_type == 'animation':
            BOT.send_message(message.from_user.id, message.animation.file_id)
    else:
        BOT.send_message(message.from_user.id, 'Access denied!')


def AnnualCheck():
    while True:
        try:
            sheets = SERVICE.spreadsheets().get(spreadsheetId=SHEET_ID, fields='sheets.properties.title').execute()
            sheets = [sheet['properties']['title'] for sheet in sheets['sheets'] if sheet['properties']['title'][0] in ('@', '-')]
            cur_time = datetime.now().strftime('%d.%m.%Y %H:%M')
            data = GetManySectors(SCAN[0], SCAN[1], SERVICE, sheets, SHEET_ID)
            for id_channel, value in data.items():
                for row in value['values']:
                    caption = None
                    markup = None
                    if cur_time == row[0] + ' ' + row[1]:
                        Stamp(f"Sending message to {id_channel}", 'i')
                        if row[COL_MSG] != '-':
                            caption = row[COL_MSG]
                        if row[COL_LINK_URL] != '-' and row[COL_LINK_TEXT] != '-':
                            links = row[COL_LINK_URL].split(',')
                            texts = row[COL_LINK_TEXT].split(',')
                            markup = telebot.types.InlineKeyboardMarkup()
                            for link, text in zip(links, texts):
                                markup.add(telebot.types.InlineKeyboardButton(url=link, text=text))
                        if row[COL_PHOTO] != '-':
                            photos = row[COL_PHOTO].split(',')
                            if len(photos) == 1:
                                BOT.send_photo(id_channel, row[COL_PHOTO], caption=caption, reply_markup=markup, parse_mode='Markdown')
                            else:
                                media = []
                                for i, photo in enumerate(photos):
                                    if i == 0:
                                        media.append(telebot.types.InputMediaPhoto(media=photo, caption=caption, parse_mode='Markdown'))
                                    else:
                                        media.append(telebot.types.InputMediaPhoto(media=photo, parse_mode='Markdown'))
                                BOT.send_media_group(id_channel, media)
                        elif row[COL_VIDEO] != '-':
                            BOT.send_video(id_channel, row[COL_VIDEO], caption=caption, reply_markup=markup, parse_mode='Markdown')
                        elif row[COL_CIRCLE] != '-':
                            BOT.send_video_note(id_channel, row[COL_CIRCLE], reply_markup=markup, parse_mode='Markdown')
                        elif row[COL_VOICE] != '-':
                            BOT.send_voice(id_channel, row[COL_VOICE], caption=caption, reply_markup=markup, parse_mode='Markdown')
                        elif row[COL_STICKER] != '-':
                            BOT.send_sticker(id_channel, row[COL_STICKER])
                        elif row[COL_ANIM] != '-':
                            BOT.send_animation(id_channel, row[COL_ANIM], caption=caption, reply_markup=markup, parse_mode='Markdown')
                        elif row[COL_MSG] != '-':
                            BOT.send_message(id_channel, caption, reply_markup=markup, parse_mode='Markdown')
                        BOT.send_message(LOG_ID, f'Sent to {id_channel}')
                        break
        except Exception as e:
            Stamp(f'In AnnualCheck: {e}', 'e')
            BOT.send_message(LOG_ID, f'ERROR in AnnualCheck: {e}')
            Stamp(traceback.format_exc(), 'e')
        finally:
            Sleep(60)


if __name__ == '__main__':
    Main()
