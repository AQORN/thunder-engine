"""
Django settings for thunder cloud

For more information on this file, see
https://docs.djangocloud.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangocloud.com/en/1.7/ref/settings/
"""

# Build paths inside the cloud like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
MEDIA_ROOT = os.path.join(SITE_ROOT, 'media').replace('\\', '/')

# Quick-start development settings - unsuitable for production
# See https://docs.djangocloud.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(d$=_@29=_z(zb0&lz0#+bk3jg8@-qi0&cle@@!1+qo_ec!h8t'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

TEMPLATE_LOADERS = (
    'django_jinja.loaders.FileSystemLoader',
    'django_jinja.loaders.AppLoader',
)

# To set the simulator mode
SIMULATOR_MODE = False
ENABLE_VLAN_TAG = True

# set main paths of thunder
THUNDER_PORT = '9000'
CHEF_SERVER_IP = 'localhost'
THUNDER_HOST = 'localhost'
LOCAL_REPO_IP = 'localhost:8080'
THUNDER_ABS_PATH = "/opt/thunder_web"
BASE_URL = 'http://' + THUNDER_HOST + ':' + THUNDER_PORT + '/'
PKG_DOWNLOAD_URL = 'http://' + LOCAL_REPO_IP + '/mydebs'
THUNDER_NAME = 'Thunder'
NODE_PREFIX = 'Node'
PASS_PREFIX = 'Thund3R!'
PASS_SUFFIX = '!thund3R' 
DISKDRIVE_EXTRA = 0
NETWORK_EXTRA_FIELD = 3
SYSTEM_PARTITON_SPACE = 4
DHCP_LEASES_FILE_LOC = "/var/lib/dhcp/dhcpd.leases"
DHCP_STATIC_FILE_LOC = "/var/lib/dhcp/dhcpd.conf_subnet"
COBBLER_UBUNTU_PROFILE = "ubuntu-12_04-x86_64"
OS_INSTALLATION_DISK = "/dev/sda"

# thunder db settings
THUNDER_DB_HOST = "localhost"
THUNDER_DB_NAME = "thunder"
THUNDER_DB_USER = "root"
THUNDER_DB_PASS = ""

# Setting patch related paths
PATCH_UPLOAD_PATH = "/opt/thunder_web/patches/"
DB_PATCH_UPLOAD_PATH = "/opt/thunder_web/db/"
PATCH_ROLLBACK_PATH = "/opt/thunder_rollback/thunder_web/"
DB_PATCH_ROLLBACK_PATH = "/opt/thunder_web/db/rollback/"
PATCH_RELEASE_FILE_PATH = "/opt/thunder_web/patches/RELEASES.txt"
PATCH_INSTALL_SH_FILE_PATH = "/opt/thunder_web/patches/"
PATCH_ROLLBACK_SH_FILE_PATH = "/opt/thunder_web/patches/rollback/"
PATCH_COMPRESS_FILE = "Thunder"
PATCH_VERSION_TEXT = "THUNDER_RELEASE_VERSION"

#zabbix settings
ZABBIX_DB_HOST = 'localhost'
ZABBIX_DB_NAME = "zabbix"
ZABBIX_DB_USER = "root"
ZABBIX_DB_PASS = ""
ZABBIX_SERVER = "http://localhost:8080/zabbix"
ZABBIX_USERNAME = "admin"
ZABBIX_PASSWORD = "zabbix"
ZABBIX_GROUPID = 4
ZABBIX_ICMP_TEMP_ID = 10104

# deploy os related credentials
SYS_OS_USERNAME = "root"
SYS_OS_SUDO = True

# adding api url using base url
API_URL = BASE_URL + "api"

#settings for the context processors
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'cloud.context_processors.baseUrl',
    'cloud.context_processors.cloudName', 
    'cloud.context_processors.nodeName',
    'cloud.context_processors.hasNewAlerts',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',  
    'cloud.context_processors.mediaRoot',
    'cloud.context_processors.systemSpace',
)

ALLOWED_HOSTS = ['*']
DELETE_MESSAGES = 50
MESSAGE_TAGS = { DELETE_MESSAGES : 'deleted',  }

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_jinja',
    'urlbreadcrumbs',
    'django_bootstrap_breadcrumbs',
    'django_tables2',    
    'shoogie',
    'cloud',
    'task',
    'rest_framework',
    'api',
    'network',
    'deployment',
    'job',
    'download',
    'thunderadmin'
    )

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'thunder.urls'

WSGI_APPLICATION = 'thunder.wsgi.application'

#breadcrumb name mapping
URLBREADCRUMBS_NAME_MAPPING = {
    'index'  : 'Home page',
    'CloudAdd' : 'Cloud Add',
    'CloudEdit' : 'Cloud Edit',
    'AssignedRole' : 'Assigned Role',
    'roleAssign' : 'Role Assignment',
}

# Database
# https://docs.djangocloud.com/en/1.7/ref/settings/#databases 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': THUNDER_DB_NAME,
        'USER': THUNDER_DB_USER,
        'PASSWORD': THUNDER_DB_PASS,
        'HOST': THUNDER_DB_HOST,
    },
    'zabbix': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': ZABBIX_DB_NAME,                    
        'USER': ZABBIX_DB_USER,                      
        'PASSWORD': ZABBIX_DB_PASS,                     
        'HOST': ZABBIX_DB_HOST,                   
        'PORT': '',                          
    }
}
 
# Internationalization
# https://docs.djangocloud.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangocloud.com/en/1.7/howto/static-files/
STATIC_URL = '/static/'

#logging system.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file':{
            'level': 'DEBUG',                      
            'class': 'logging.FileHandler',
            'filename': '/var/log/mylog.log',
            'formatter': 'verbose'
        },
        'db':{
            'level': 'ERROR',         
            'class': 'cloud.loggers.dbLogHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': False,
            },
        'myapplog': {
            'handlers': ['db'],   
            'level': 'DEBUG',
            'propagate': False,
        }
    }
}

#Default authentication system for the API
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.permissions.IsAuthenticated',
    )
}
