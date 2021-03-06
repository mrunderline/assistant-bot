from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from setting import BOT_TOKEN, DOWNLOAD_PATH_PREFIX, DOWNLOAD_DST
from downloader import Youtube
import shutil
from zipfile import ZipFile
import os
from os.path import basename


def text_callback(update, context):
    message = update.message
    text = message.text

    if text.count(' ') < 1:
        message.reply_text('i dont know and dont care :]')
        return

    command, *others = text.split(' ')
    command = command.lower()
    if command == 'yt':
        link = others[0]
        youtube = Youtube(link, message.reply_text)
        youtube.download()
        message.reply_text(f'{DOWNLOAD_PATH_PREFIX}{youtube.filepath.split("/")[-1].replace(" ", "_")}')
    elif command == 'files':
        order = others[0]
        if order == 'zip':
            zip_file_name = 'files.zip'
            with ZipFile(DOWNLOAD_DST + zip_file_name, 'w') as zipObj:
                for folder, _, filenames in os.walk(DOWNLOAD_DST):
                    for filename in filenames:
                        if filename == zip_file_name:
                            continue
                        file_path = os.path.join(folder, filename)
                        zipObj.write(file_path, basename(file_path))

            message.reply_text(f'files zipped\n{DOWNLOAD_PATH_PREFIX}{zip_file_name}')
        elif order == 'rm':
            shutil.rmtree(DOWNLOAD_DST)
            message.reply_text('remove files')
        elif order == 'list':
            message.reply_text('\n'.join([f for f in os.listdir(DOWNLOAD_DST)]))
    elif command == 'ssl':
        site = others[0]
        stream = os.popen(f'bash scripts/ssl.sh {site}')
        message.reply_text(stream.read())
    else:
        message.reply_text('i dont know and dont care :]')


def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", text_callback))
    dp.add_handler(MessageHandler(Filters.text, text_callback))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
