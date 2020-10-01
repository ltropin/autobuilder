from os import listdir, path, remove, mkdir
import shutil
from pathlib import Path
from os.path import isfile, join
from automated_building.config import LOG_FILES, BUILD_DIR_OUTPUT, LOG_PATH, IS_FLUTTER

BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))

def create_log_files():
    for filename in LOG_FILES.values():
        abs_file_path = f'{BASE_DIR}/{LOG_PATH}/{filename}'
    
        Path(f'{BASE_DIR}/{LOG_PATH}').mkdir(parents=True, exist_ok=True)
        open(abs_file_path, 'a').close()


def clear_directories():
    if path.exists(f'{BASE_DIR}/{BUILD_DIR_OUTPUT}'):
        shutil.rmtree(f'{BASE_DIR}/{BUILD_DIR_OUTPUT}')
    # Clear cache files
    if path.exists(f'{path.expanduser("~")}/Library/Developer/Xcode/DerivedData'):
        shutil.rmtree(f'{path.expanduser("~")}/Library/Developer/Xcode/DerivedData')
    if IS_FLUTTER and path.exists(f'{BASE_DIR}/ios/Runner.xcworkspace'):
        shutil.rmtree(f'{BASE_DIR}/ios/Runner.xcworkspace')
    if IS_FLUTTER and path.exists(f'{BASE_DIR}/ios/Pods'):
        shutil.rmtree(f'{BASE_DIR}/ios/Pods')
    elif path.exists(f'{BASE_DIR}/Pods'):
        shutil.rmtree(f'{BASE_DIR}/Pods')



def get_ipa_file(path_to_ipa: str):
    onlyfiles = [f for f in listdir(path_to_ipa) if isfile(join(path_to_ipa, f))]
    only_ipa = [el for el in onlyfiles if len(el) >= 4 and el[-4:] == '.ipa'][0]
    return path_to_ipa + f'/{only_ipa}'