import os
import logging
import dj_database_url

logger = logging.getLogger('items')  

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#本地配置参数  
class Local():  
    DATABASES = {  
        # 'default': {  
        #     'ENGINE': 'django.db.backends.mysql',  
        #     'NAME': 'xxx',  
        #     'USER': 'xxx',  
        #     'PASSWORD': 'xxx',  
        #     'HOST': '127.0.0.1',  
        #     'PORT': '3306',  
        # },  
        #    'default': {
        #        'ENGINE': 'django.db.backends.sqlite3',
        #        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        #    }

	'default': {
        	'ENGINE': 'django.db.backends.postgresql_psycopg2',
        	'NAME': 'blogdb',
        	'USER': 'blogdbuser',
        	'PASSWORD': '666666',
        	'HOST': '127.0.0.1',
        	'PORT': '5432',
   		 }
        }
    CACHES = {
            "default": {
                "BACKEND": "django_redis.cache.RedisCache",
                "LOCATION": "redis://127.0.0.1:6379/1",
                "OPTIONS": {
                    "CLIENT_CLASS": "django_redis.client.DefaultClient",
                    # "PASSWORD": "mysecret"
                }
            }
        }

#服务器配置参数  
class Remote():  
    # DATABASES = {  
    #     'default': {  
    #         'ENGINE': 'django.db.backends.mysql',  
    #         'NAME': 'xxx',  
    #         'USER': 'xxx',  
    #         'PASSWORD': 'xxx',  
    #         'HOST': 'w.rdc.sae.sina.com.cn',  
    #         'PORT': '3307',  
    #     }  
    # }  
    DATABASES = {
        'default': dj_database_url.config()
    }
    # DATABASES['default'] = dj_database_url.config()
  
class MyConfig():  
    __conf = None  
    __is_remote = 'DATABASE_URL' in os.environ  
  
    def is_remote_env(self):  
        return self.__is_remote  
  
    def get_config(self):  
        if self.__conf == None:  
            if self.__is_remote:  
                logger.info("set remote config")  
                self.__conf = Remote()  
            else:  
                logger.info("set local config")  
                self.__conf = Local()  
        return self.__conf  
