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
    data = GetSector('A2', 'G100', SERVICE, 'Расписание', SHEET_ID)
    for row in data:
        if cur_time == row[0] + ' ' + row[1]:
            ids = row[5].split(',')
            link = 'https://drive.google.com/uc?export=view&id=' + re.search(PATTERN, row[3]).group(1)
            Stamp(f'Sending message to {' '.join(ids)}', 'i')
            for id_channel in ids:
                BOT.send_photo(id_channel, link, caption=row[4])


if __name__ == '__main__':
    Main()
