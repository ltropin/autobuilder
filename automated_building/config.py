
DAIWI_TOKEN = '<DIAWI TOKEN>'
TELEGRAM_BOT_TOKEN = '<TELAGRAM API TOKEN>'

# View chat ids 
# https://api.telegram.org/bot<API TOKEN>/getUpdates
TELEGRAM_GROUP_ID = '<GROUP TELEGRAM ID>'
# TELEGRAM_GROUP_ID = '964661580'

IS_FLUTTER = True
VERBOSE = False
PROJECT_NAME = 'Runner'
BUILD_DIR_OUTPUT = 'build'
IOS_PREFIX = '#сборка_iOS'
USE_PREFIX = True
# USE_DECRIPTION = True

OPTIONS_PLIST_PATH_FILE = 'ios/Runner/OptionsPlist.plist'

# Don't touch

LOG_PATH = f'{BUILD_DIR_OUTPUT}/ios/logs'
ARCHIVE_PATH = f'{BUILD_DIR_OUTPUT}/ios/archive'
EXPORT_PATH = f'{BUILD_DIR_OUTPUT}/ios/export'

LOG_FILES = {
    'pod': 'pod.log',
    'build': 'xcode_build.log',
    'archive': 'xcode_archive.log',
    'export': 'xcode_export.log',
    'apk': 'flutter_apk.log'
}

# For flutter
FLUTTER_BUILD_PATH_FILE = 'build/app/outputs/flutter-apk/app-release.apk'
ANDROID_PREFIX = '#сборка_Android'