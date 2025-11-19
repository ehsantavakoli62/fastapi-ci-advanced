# logging_config.py 

dict_config = {
    'version': 1,
    'disable_existing_loggers': False,

    # 1. فرمت‌ها (Formatters)
    'formatters': {
        'default_formatter': {
            'format': '%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s'
        },
    },

    # 2. فیلترها (Filters)
    'filters': {
        'ascii_only_filter': {
            # Class path to our custom filter / مسیر کلاس فیلتر سفارشی ما
            '()': 'filters.AsciiFilter', 
        }
    },

    # 3. هندلرها (Handlers)
    'handlers': {
        'console_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'default_formatter',
            'level': 'DEBUG', 
            'stream': 'ext://sys.stdout',
            # Apply the custom filter to the handler / اعمال فیلتر سفارشی به هندلر
            'filters': ['ascii_only_filter'], 
        },
    },

    # 4. لاگرها (Loggers)
    'loggers': {
        'app': {
            'level': 'DEBUG',
            'handlers': ['console_handler'],
            'propagate': False,
        },
        'utils': {
            'level': 'DEBUG',
            'handlers': ['console_handler'],
            'propagate': False,
        },
    },

    # 5. لاگر ریشه (Root Logger)
    'root': {
        'level': 'DEBUG',
        'handlers': ['console_handler'],
    }
}
