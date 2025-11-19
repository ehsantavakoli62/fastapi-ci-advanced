# logging_config.py 
dict_config = {
    'version': 1,
    'disable_existing_loggers': False, 

    # 1. Formatters / قالب‌دهنده‌ها
    'formatters': {
        'default_formatter': {
            'format': '%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s'
        },
    },

    # 2. Handlers / مدیریت‌کننده‌ها
    'handlers': {
        'console_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'default_formatter',
            'level': 'DEBUG', 
            'stream': 'ext://sys.stdout',
        },
    },

    # 3. Loggers / لاگرها (ایجاد ساختار درختی)
    'loggers': {
        # Define 'app' logger / تعریف لاگر 'app'
        'app': {
            'level': 'INFO',
            'handlers': ['console_handler'],
            'propagate': False, # Stop propagation to root
        },
        # Define 'utils' logger / تعریف لاگر 'utils'
        'utils': {
            'level': 'DEBUG',
            'handlers': ['console_handler'],
            'propagate': True, # Allow propagation to root
        },
        # Define a child logger for testing the tree structure / تعریف یک لاگر فرزند
        'app.submodule': {
            'level': 'WARNING',
            'propagate': True,
        }
    },

    # 4. Root Logger / لاگر ریشه
    'root': {
        'level': 'WARNING',
        'handlers': ['console_handler'],
    }
}
