# logging_config.py 

# دیکشنری پیکربندی کامل لاگ‌گیری
dict_config = {
    'version': 1,
    'disable_existing_loggers': False, # اجازه می‌دهد لاگرهای موجود غیرفعال نشوند

    # 1. فرمت‌ها (Formatters)
    'formatters': {
        'default_formatter': {
            # فرمت مورد نیاز: سطح | لاگر | زمان | شماره خط | پیام
            'format': '%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s'
        },
    },

    # 2. هندلرها (Handlers)
    'handlers': {
        'console_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'default_formatter',
            'level': 'DEBUG', # تنظیم سطح لاگ برای کنسول
            'stream': 'ext://sys.stdout', # اطمینان از خروجی به stdout
        },
    },

    # 3. لاگرها (Loggers)
    'loggers': {
        # تنظیمات لاگر 'app'
        'app': {
            'level': 'DEBUG',
            'handlers': ['console_handler'],
            'propagate': False,
        },
        # تنظیمات لاگر 'utils'
        'utils': {
            'level': 'DEBUG',
            'handlers': ['console_handler'],
            'propagate': False,
        },
    },

    # 4. لاگر ریشه (Root Logger)
    'root': {
        'level': 'DEBUG',
        'handlers': ['console_handler'],
    }
}
