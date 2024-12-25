LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'task_1_all': {
            'format': '{asctime} {levelname} {message}',
            'datetime': '%Y.%m.%d %H:%M:%S',
            'style': '{',
        },
        'task_1_warning': {
            'format': '{asctime} {levelname} {message} {pathname}',
            'datetime': '%Y.%m.%d %H:%M:%S',
            'style': '{',
        },
        'task_1_er_cr': {
            'format': '{asctime} {levelname} {message} {pathname} {exc_info}',
            'datetime': '%Y.%m.%d %H:%M:%S',
            'style': '{',
        },
        'task_2': {
            'format': '{asctime} {levelname} {module} {message}',
            'datetime': '%Y.%m.%d %H:%M:%S',
            'style': '{',
        },
        'task_3': {
            'format': '{asctime} {levelname} {message} {pathname} {exc_info}',
            'datetime': '%Y.%m.%d %H:%M:%S',
            'style': '{',
        },
        'task_4': {
            'format': '{asctime} {levelname} {module} {message}',
            'datetime': '%Y.%m.%d %H:%M:%S',
            'style': '{',
        },
        'task_5': {
            'format': '{asctime} {levelname} {message} {pathname}',
            'datetime': '%Y.%m.%d %H:%M:%S',
            'style': '{',
        },
    },

    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },

    'handlers': {
        'console_1_all': {
            'class': 'logging.StreamHandler',
            'formatter': 'task_1_all',
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
        },
        'console_1_warning': {
            'class': 'logging.StreamHandler',
            'formatter': 'task_1_warning',
            'level': 'WARNING',
            'filters': ['require_debug_true'],
        },
        'console_1_er_cr': {
            'class': 'logging.StreamHandler',
            'formatter': 'task_1_er_cr',
            'level': 'ERROR',
            'filters': ['require_debug_true'],
        },
        'general': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'general.log',
            'formatter': 'task_2',
            'filters': ['require_debug_false'],
        },
        'errors': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'errors.log',
            'formatter': 'task_3',
        },
        'security': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'security.log',
            'formatter': 'task_4',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'task_5',
            'filters': ['require_debug_false'],
        },
    },

    'loggers': {
        'django': {
            'handlers': ['console_1_all', 'console_1_warning', 'console_1_er_cr', 'general'],
            'level': 'DEBUG'
        },
        'django.request': {
            'handlers': ['errors', 'mail_admins'],
            'level': 'ERROR'
        },
        'django.server': {
            'handlers': ['errors', 'mail_admins'],
            'level': 'ERROR'
        },
        'django.template': {
            'handlers': ['errors'],
            'level': 'ERROR'
        },
        'django.db.backends': {
            'handlers': ['errors'],
            'level': 'ERROR'
        },
        'django.db.security': {
            'handlers': ['security'],
            'level': 'INFO'
        },
    },
}
