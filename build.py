import os, sys
from automated_building.config import *
import random
from automated_building.bcolors import bcolors
import subprocess
from diawi_uploader import upload
from automated_building.preprocess import create_log_files, clear_directories, get_ipa_file
import requests
from datetime import datetime
from requests_toolbelt import MultipartEncoder
import telebot

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

has_error = False

build_command = 'xcodebuild ' + \
f'-workspace {PROJECT_NAME}.xcworkspace ' + \
f'-scheme {PROJECT_NAME} ' + \
f'-sdk iphoneos build'
build_command += '' if VERBOSE else f' > {BASE_DIR}/{LOG_PATH}/{LOG_FILES["build"]}'

archive_command = 'xcodebuild ' + \
f'-workspace {PROJECT_NAME}.xcworkspace ' + \
f'-scheme {PROJECT_NAME} ' + \
f'-sdk iphoneos ' + \
f'-archivePath {BASE_DIR}/{ARCHIVE_PATH}/{PROJECT_NAME}.xcarchive ' + \
f'archive'
archive_command += '' if VERBOSE else f' > {BASE_DIR}/{LOG_PATH}/{LOG_FILES["archive"]}'


export_command = 'xcrun xcodebuild ' + \
'-exportArchive IPA ' + \
f'-archivePath  {BASE_DIR}/{ARCHIVE_PATH}/{PROJECT_NAME}.xcarchive ' + \
f'-exportOptionsPlist {BASE_DIR}/{OPTIONS_PLIST_PATH_FILE} ' + \
f'-exportPath  {BASE_DIR}/{EXPORT_PATH} ' + \
f'-target iOS ' + \
f'-sdk iphoneos'
export_command += '' if VERBOSE else f' > {BASE_DIR}/{LOG_PATH}/{LOG_FILES["export"]}'

pod_install_command = 'pod install'
pod_install_command += '' if VERBOSE else f' > {BASE_DIR}/{LOG_PATH}/{LOG_FILES["pod"]}'

old = datetime.now()

# PREPROCESS
clear_directories()
create_log_files()

# DESCRIPTION = ''
# if USE_DECRIPTION:
#     print('Description: ', end='')
#     lines = []
#     while True:
#         try:
#             line = input()
#         except:
#             break
#         lines.append(line)
        
#     DESCRIPTION = '\n' + '\n'.join(lines)

# BUILD FOR FLUTTER
if IS_FLUTTER:
    android_build = 'flutter build apk'
    android_build += '' if VERBOSE else f' > {BASE_DIR}/{LOG_PATH}/{LOG_FILES["apk"]}'
    
    subprocess.check_output(android_build, shell=True, stderr=subprocess.DEVNULL)

    if not VERBOSE:
        with open(f'{BASE_DIR}/{LOG_PATH}/{LOG_FILES["apk"]}', 'r') as f:
            if f'Built {FLUTTER_BUILD_PATH_FILE}' in f.read():
                print(f'{bcolors.OKGREEN}{bcolors.BOLD}Build APK successful{bcolors.ENDC}')
            else:
                # has_error = True
                print(f'{bcolors.FAIL}{bcolors.BOLD}Build APK failed{bcolors.ENDC}')

    os.chdir(f'{BASE_DIR}/ios')

# INSTALL PODS
subprocess.check_output(pod_install_command, shell=True, stderr=subprocess.DEVNULL)

if not VERBOSE:
    with open(f'{BASE_DIR}/{LOG_PATH}/{LOG_FILES["pod"]}', 'r') as f:
        if 'Pod installation complete' in f.read():
            print(f'{bcolors.OKGREEN}{bcolors.BOLD}Pods installed successful{bcolors.ENDC}')
        else:
            has_error = True
            print(f'{bcolors.FAIL}{bcolors.BOLD}Pods installed failed{bcolors.ENDC}')

# BUILDING PROJECT
subprocess.check_output(build_command, shell=True, stderr=subprocess.DEVNULL)

if not VERBOSE and not has_error:
    with open(f'{BASE_DIR}/{LOG_PATH}/{LOG_FILES["build"]}') as f:
        if 'BUILD SUCCEEDED' in f.read():
            print(f'{bcolors.OKGREEN}{bcolors.BOLD}Build succeeded{bcolors.ENDC}')
        else:
            has_error = True
            print(f'{bcolors.FAIL}{bcolors.BOLD}Build failed{bcolors.ENDC}')

# ARCHIVING
subprocess.check_output(archive_command, shell=True, stderr=subprocess.DEVNULL)

if not VERBOSE and not has_error:
    with open(f'{BASE_DIR}/{LOG_PATH}/{LOG_FILES["archive"]}') as f:
        if 'ARCHIVE SUCCEEDED' in f.read():
            print(f'{bcolors.OKGREEN}{bcolors.BOLD}Archive succeeded{bcolors.ENDC}')
        else:
            has_error = True  
            print(f'{bcolors.FAIL}{bcolors.BOLD}Archive failed{bcolors.ENDC}')

# EXPORT IPA
subprocess.check_output(export_command, shell=True, stderr=subprocess.DEVNULL)

if not VERBOSE and not has_error:
    with open(f'{BASE_DIR}/{LOG_PATH}/{LOG_FILES["export"]}') as f:
        if 'EXPORT SUCCEEDED' in f.read():
            print(f'{bcolors.OKGREEN}{bcolors.BOLD}Export succeeded{bcolors.ENDC}')
        else:
            has_error = True  
            print(f'{bcolors.FAIL}{bcolors.BOLD}Export failed{bcolors.ENDC}')

if not has_error:
    os.chdir(BASE_DIR)
    # SENDING ANDROID ASSEMBLY
    if IS_FLUTTER:
        multipart_encoder = MultipartEncoder(fields={
            "file": (os.path.basename(f'{BASE_DIR}/{FLUTTER_BUILD_PATH_FILE}'), open(f'{BASE_DIR}/{FLUTTER_BUILD_PATH_FILE}', "rb"), 'application/octet-stream'),
        })
        try:
            bot.send_document(
                TELEGRAM_GROUP_ID,
                open(f'{BASE_DIR}/{FLUTTER_BUILD_PATH_FILE}', "rb"),
                timeout=10000,
                caption=f'{f"{ANDROID_PREFIX} " if USE_PREFIX else ""}'
            )
            print(f'{bcolors.OKGREEN}{bcolors.BOLD}[Android] Build was successfully sent{bcolors.ENDC}')
        except:
            has_error = True
            print(f'{bcolors.FAIL}{bcolors.BOLD}[Android] Build was not sent{bcolors.ENDC}')


    # SENDING IOS URL
    path_ipa = get_ipa_file(path_to_ipa=f'{BASE_DIR}/{EXPORT_PATH}')
    link = upload(token=DAIWI_TOKEN, file_path=path_ipa)

    url_send_message = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    ios_res = requests.post(url_send_message, data={
            'chat_id': TELEGRAM_GROUP_ID,
            'text': f'{f"{IOS_PREFIX} " if USE_PREFIX else ""}{link}'
            })
    
    obj_ios = ios_res.json()

    if obj_ios['ok']:
        print(f'{bcolors.OKGREEN}{bcolors.BOLD}[iOS] Build was successfully sent{bcolors.ENDC}')
    else:
        has_error = True
        print(f'{bcolors.FAIL}{bcolors.BOLD}[iOS] Build was not sent{bcolors.ENDC}')
    
    print(f'Elapsed time: {datetime.now() - old}')