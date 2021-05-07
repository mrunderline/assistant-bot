from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from setting import BOT_TOKEN, DOWNLOAD_PATH_PREFIX
from downloader import Youtube


def text_callback(update, context):
    message = update.message
    text = message.text

    if text.count(' ') < 1:
        message.reply_text('i dont know and dont care :]')

    command, *others = text.split(' ')
    if command == 'yt':
        link = others[0]
        youtube = Youtube(link, message.reply_text)
        youtube.download()
        message.reply_text(f'{DOWNLOAD_PATH_PREFIX}{youtube.filepath.split("/")[-1].replace(" ", "_")}')
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
