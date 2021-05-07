import youtube_dl
from setting import DOWNLOAD_DST
import os


class Youtube:
    def __init__(self, link, logger=None):
        self.logger = logger or print
        self.log_percent_seq = [0, 20, 40, 60, 80, 100]
        self.sent_log = None
        self.options = {
            # 'format': 'best',
            'logger': self.MyLogger(self.log_manager),
            'progress_hooks': [self.my_hook],
            'outtmpl': DOWNLOAD_DST + '%(title)s.%(ext)s'
        }
        self.link = link
        self.filepath = None

    def log_manager(self, level, message):
        if level == 'debug':
            if 'Merging formats into' in message:
                self.filepath = message.split('"')[1]
        else:
            self.logger(message)

    def get_info(self):
        result = youtube_dl.YoutubeDL().list_formats(self.link)
        self.logger(result)

    class MyLogger:
        def __init__(self, logger):
            self.logger = logger

        def debug(self, msg):
            self.logger('debug', msg)

        def warning(self, msg):
            self.logger('warning', msg)

        def error(self, msg):
            self.logger('error', msg)

    def my_hook(self, d):
        def message_generator(input):
            keys = ['filename', '_percent_str', '_eta_str', '_speed_str', '_total_bytes_str']
            return '\n'.join(key + ': ' + input[key] for key in keys)

        if d['status'] == 'downloading':
            percent = round(float(d['_percent_str'][1:-1]))
            if self.sent_log is None:
                self.sent_log = percent
                self.logger(message_generator(d))

            if percent in self.log_percent_seq and percent > self.sent_log:
                self.sent_log = percent
                self.logger(message_generator(d))

        if d['status'] == 'finished':
            self.filepath = d['filename']
            self.logger('finished')

    def download(self):
        with youtube_dl.YoutubeDL(self.options) as ytdl:
            print(self.link)
            ytdl.download([self.link])
            os.rename(self.filepath, self.filepath.replace(" ", "_"))
