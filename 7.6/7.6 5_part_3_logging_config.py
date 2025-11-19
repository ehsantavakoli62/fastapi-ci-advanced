# logging_config.py 
dict_config = {
    'version': 1,
    'disable_existing_loggers': False,

    # 1. فرمت‌ها (Formatters)
    'formatters': {
        'default_formatter': {
            # فرمت مورد نیاز تمرین‌های قبلی: سطح | لاگر | زمان | شماره خط | پیام
            'format': '%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s'
        },
    },

    # 2. هندلرها (Handlers)
    'handlers': {
        # هندلر چرخش زمانی برای فایل utils.log
        'rotating_file_handler': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'default_formatter',
            'filename': 'utils.log', # فایل مورد نظر
            'when': 'h', # چرخش بر اساس ساعت (hour)
            'interval': 10, # هر 10 ساعت
            'backupCount': 2, # نگه داشتن 2 کپی پشتیبان (اختیاری)
            'level': 'INFO', # فقط INFO و بالاتر ثبت شوند
            'encoding': 'utf-8',
        },
        # هندلر کنسول برای نمایش عمومی (اختیاری)
        'console_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'default_formatter',
            'level': 'DEBUG', 
            'stream': 'ext://sys.stdout',
        }
    },

    # 3. لاگرها (Loggers)
    'loggers': {
        # لاگر utils: فقط INFO و بالاتر به فایل utils.log ارسال شود
        'utils': {
            'level': 'INFO', # سطح لاگر utils روی INFO
            'handlers': ['rotating_file_handler'], # فقط این هندلر را دارد
            'propagate': False, # مطمئن می‌شویم که لاگ‌ها به ریشه ارسال نشوند
        },
        # لاگر app: می تواند هندلر کنسول را داشته باشد (برای تست)
        'app': {
            'level': 'INFO',
            'handlers': ['console_handler'],
            'propagate': False,
        },
    },

    # 4. لاگر ریشه (Root Logger)
    'root': {
        'level': 'WARNING',
        'handlers': ['console_handler'],
    }
}
