"""
Django settings for TCSDB project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'w!xmoe0)0jd=y&wqt%ax76u)mlce8^f$7ku$w%&f7kpvu6!+&c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'monitor.apps.MonitorConfig',
    'testcase.apps.TestcaseConfig',
    'rbac.apps.RbacConfig',
    'cccs.apps.CccsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'rbac.middlewares.rbac.RbacMiddleware',  # 权限中间件
]

ROOT_URLCONF = 'TCSDB.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'TCSDB.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME'  : 'testcases',
#         'USER'  : 'cuimei',
#         'PASSWORD': '123456',
#         'HOST'   : '127.0.0.1',
#         'PORT'   : '5432',
# #     'ENGINE': 'django.db.backends.mysql',
# #     'NAME':'tcsdb',
# #     'USER': 'root',
# #     'PASSWORD': '',
# #     'HOST': 'localhost',
# #     'PORT': '3306',
#     }
# }


TESTING = len(sys.argv) > 1 and sys.argv[1] == 'test'
if TESTING:
    # 当使用SQLite数据库引擎时，测试将默认使用内存数据库
    DATABASES = {
        'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
        
    }
else:
    DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME':'tcsdb_test',
    'USER': 'postgres',
    'PASSWORD': 'dera1234',
    'HOST': '10.0.4.118',
    'PORT': '5432',
    }
    }


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
# STATIC_ROOT = os.path.join(BASE_DIR,'static')
SERVER_IP = '10.0.2.20'
API_TOKEN = "7d6766a6s5f76safas657889hj78kf91"
############################ 权限管理相关 ################################
PERMISSION_MENU_KEY = "w*d6v&ns8qq_y#1f"
# 不用登陆可访问页面
VALID_URL= [
    '^/login/',
    '^/api/auth/',
    '^/get_code/',
    # '^/index/',
    # '^/index_v3/',
    '^/403/',
    '^/logout/',
    '^/monitor/api/',
    '^/testcase/api/',
    '^/cccs/api/',
]

APPEND_SLASH=False
###############################其它设置##################################
SERVER_IP = ''
CODE_FONT_FILE = os.path.join(BASE_DIR,'static/fonts/wqy-microhei.ttc')  #设置验证码字体文件

##################### 分页器设置 ########################################


PER_PAGE = 20    #每页显示数据数
PAGER_PAGE_COUNT = 11    #页面上最多显示页码数

##################### session配置 ######################################
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # 引擎（默认）
SESSION_COOKIE_NAME = "sessionid"  # Session的cookie保存在浏览器上时的key，即：sessionid=随机字符串（默认）
SESSION_COOKIE_PATH = "/"  # Session的cookie保存的路径（默认）
SESSION_COOKIE_DOMAIN = None  # Session的cookie保存的域名（默认）
SESSION_COOKIE_SECURE = False  # 是否Https传输cookie（默认）
SESSION_COOKIE_HTTPONLY = True  # 是否Session的cookie只支持http传输（默认）
# SESSION_COOKIE_AGE = 3600  # Session的cookie失效日期（1小时）（默认1209600 2周）
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # 是否关闭浏览器使得Session过期（默认False）
SESSION_SAVE_EVERY_REQUEST = True  # 是否每次请求都保存Session，默认修改之后才保存（默认False）


########################### 日志文件配置 ########################################
LOG_FILE_PATH = os.path.join(BASE_DIR,'log')
LOG_BACKUP_COUNT = 5
LOG_MAX_BYTES = 1024*1024*5

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'utils.custom_exception.custom_exception_handler'
}