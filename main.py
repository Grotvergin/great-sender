from source import *


def Main() -> None:
    while True:
        try:
            AnnualCheck()
        except Exception as e:
            Stamp(f'{e}', 'e')
            Stamp(traceback.format_exc(), 'e')
        finally:
            Sleep(60)


def AnnualCheck():
    cur_time = datetime.now().strftime('%d.%m.%Y %H:%M')
    data = GetSector('A2', 'I100', SERVICE, 'Расписание', SHEET_ID)
    for row in data:
        # if cur_time == row[0] + ' ' + row[1]:
            ids = row[8].split(',')
            Stamp(f'Sending message to {' '.join(ids)}', 'i')
            base = 'https://drive.google.com/uc?export=view&id='
            media = []
            for i in range(3, 7):
                link = base + re.search(PATTERN, row[i]).group(1) if row[i] != '-' else None
                media.append(link)
            for id_channel in ids:
                if media[0]:
                    BOT.send_photo(id_channel, media[0], caption=row[7])
                if media[2]:
                    BOT.send_video_note(id_channel, media[2])


if __name__ == '__main__':
    Main()
