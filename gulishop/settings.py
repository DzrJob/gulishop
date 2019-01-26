"""
Django settings for gulishop project.

Generated by 'django-admin startproject' using Django 1.11.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os, sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# os.path.dirname 文件所在目录路径
# os.path.abspath 文仔所在路径
# sys.path.insert 加入搜索路径
# os.path.join 把目录和文件名合成一个路径
# 项目的绝对根路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# apps整合后路径
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
# 第三方apps整合路径
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# 跨站请求伪造保护 秘钥
SECRET_KEY = '8d48#s%6(o737pgsgeou9j#=fj@486srxvg)^*8%_0ysngdq5r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
# APP注册
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users.apps.UsersConfig',
    'goods.apps.GoodsConfig',
    'trade.apps.TradeConfig',
    'operations.apps.OperationsConfig',
    # 安装xadmin依赖后注册app
    'xadmin',
    'crispy_forms',
    # 富文本
    'DjangoUeditor',
    # drf接口
    'rest_framework',
    # 过滤器
    'django_filters',
    # 跨站访问
    'corsheaders',
    # token认证
    # 'rest_framework.authtoken',

]
# 中间件
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 跨站访问
    'corsheaders.middleware.CorsMiddleware',
]
# 主程序路径
ROOT_URLCONF = 'gulishop.urls'
# 模板 自定义
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
                # 将media加入上下文渲染，模板中使用{{MEDIA_URL}}
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'gulishop.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
# 数据库
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'gulishop',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'POST': '3306',
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators
# 验证
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
# https://docs.djangoproject.com/en/1.11/topics/i18n/
# 国际化
LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
# 静态文件路径
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
# 媒体文件路径 存放上传的文件
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 因为USER继承,所以要重新确定路径
AUTH_USER_MODEL = 'users.UserProfile'

# 全局配置
REST_FRAMEWORK = {
    # # 分页配置
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE': 10,

    # # 认证配置
    # 'DEFAULT_AUTHENTICATION_CLASSES': (
    #     'rest_framework.authentication.BasicAuthentication',
    #     'rest_framework.authentication.SessionAuthentication',
    #     # token认证
    #     # 'rest_framework.authentication.TokenAuthentication',
    #     # jwt认证
    #     'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    # )
}

# 跨站访问
CORS_ORIGIN_ALLOW_ALL = True

# 过期时间
import datetime
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
}

# 手机正则
MOBILE_RE = '^((13[0-9])|(14[5,7])|(15[0-3,5-9])|(17[0,3,5-8])|(18[0-9])|166|198|199|(147))\\d{8}$'

# 云片秘钥
YUNPIAN_KEY = '94e3cafc4543943d7c4de9a2fd687a5f'

# 支付宝相关
app_id = '2016092300577425'
private_key = os.path.join(BASE_DIR,'apps/trade/keys/private_key_2048.txt')
ali_key = os.path.join(BASE_DIR,'apps/trade/keys/ali_key_2048.txt')