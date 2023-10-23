import sys
import shutil
import re
from pathlib import Path

JPEG_IMAGES = []
JPG_IMAGES = []
PNG_IMAGES = []
SVG_IMAGES = []
MP3_AUDIO = []
OGG_AUDIO = []
WAV_AUDIO = []
AMR_AUDIO = []
MP4_VIDEO = []
MOV_VIDEO = []
MKV_VIDEO = []
AVI_VIDEO = []
DOC = []
DOCX = []
TXT = []
PDF = []

MY_OTHER = []
ARCHIVES = []

REGISTER_EXTENSION = {
    'JPEG': JPEG_IMAGES,
    'JPG': JPG_IMAGES,
    'PNG': PNG_IMAGES,
    'SVG': SVG_IMAGES,
    'MP3': MP3_AUDIO,
    'ZIP': ARCHIVES,
    "OGG": OGG_AUDIO,
    "WAV": WAV_AUDIO,
    "AMR": AMR_AUDIO,
    "MP4": MP4_VIDEO,
    "MOV": MOV_VIDEO,
    "MKV": MKV_VIDEO,
    "AVI": AVI_VIDEO,
    "DOC": DOC,
    "DOCX": DOCX,
    "TXT": TXT,
    "PDF": PDF
}

FOLDERS = []
EXTENSIONS = set()
UNKNOWN = set()

def get_extension(name: str) -> str:
    return Path(name).suffix[1:].upper()  # suffix[1:] -> .jpg -> jpg

def scan(folder: Path):
    for item in folder.iterdir():
        # Робота з папкою
        if item.is_dir():  # перевіряємо чи обєкт папка
            if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'MY_OTHER'):
                FOLDERS.append(item)
                scan(item)
            continue

        # Робота з файлом
        extension = get_extension(item.name)  # беремо розширення файлу
        full_name = folder / item.name  # беремо повний шлях до файлу
        if not extension:
            MY_OTHER.append(full_name)
        else:
            try:
                ext_reg = REGISTER_EXTENSION[extension]
                ext_reg.append(full_name)
                EXTENSIONS.add(extension)
            except KeyError:
                UNKNOWN.add(extension)  # .mp4, .mov, .avi
                MY_OTHER.append(full_name)



CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")

TRANS = dict()

for cyrillic, latin in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(cyrillic)] = latin
    TRANS[ord(cyrillic.upper())] = latin.upper()


def normalize(name: str) -> str:
    name_without_extension = name[:name.rfind('.')]  # Убираем расширение
    extension = name[name.rfind('.'):]
    translate_name = re.sub(r'\W', '_', name_without_extension.translate(TRANS))
    return f"{translate_name}{extension}"



def handle_files(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    file_suffix = file_name.suffix
    file_name.replace(target_folder / normalize(file_name.name.replace(file_name.suffix, '')))

def handle_archive(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    folder_for_file = target_folder / normalize(file_name.name.replace(file_name.suffix, ''))
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(str(file_name.absolute()), str(folder_for_file.absolute()))
    except shutil.ReadError:
        folder_for_file.rmdir()
        return
    file_name.unlink()



def main(folder: Path):
    scan(folder)
    for file in JPEG_IMAGES:
        handle_files(file, folder / 'images' / 'JPEG')
    for file in JPG_IMAGES:
        handle_files(file, folder / 'images' / 'JPG')
    for file in PNG_IMAGES:
        handle_files(file, folder / 'images' / 'PNG')
    for file in SVG_IMAGES:
        handle_files(file, folder / 'images' / 'SVG')
    for file in MP3_AUDIO:
        handle_files(file, folder / 'audio' / 'MP3_AUDIO')
    for file in OGG_AUDIO:
        handle_files(file, folder / 'audio' / 'OGG_AUDIO')
    for file in WAV_AUDIO:
        handle_files(file, folder / 'audio' / 'WAV_AUDIO')
    for file in AMR_AUDIO:
        handle_files(file, folder / 'audio' / 'AMR_AUDIO')
    for file in MP4_VIDEO:
        handle_files(file, folder / 'video' / 'MP4_VIDEO')
    for file in MOV_VIDEO:
        handle_files(file, folder / 'video' / 'MOV_VIDEO')
    for file in MKV_VIDEO:
        handle_files(file, folder / 'video' / 'MKV_VIDEO')
    for file in AVI_VIDEO:
        handle_files(file, folder / 'video' / 'AVI_VIDEO')
    for file in DOC:
        handle_files(file, folder / 'documents' / 'DOC')
    for file in DOCX:
        handle_files(file, folder / 'documents' / 'DOCX')
    for file in TXT:
        handle_files(file, folder / 'documents' / 'TXT')
    for file in PDF:
        handle_files(file, folder / 'documents' / 'PDF')
    for file in MY_OTHER:
        handle_files(file, folder / 'MY_OTHER')

    for file in ARCHIVES:
        handle_archive(file, folder / 'ARCHIVES' / 'ZIP')

    for folder in FOLDERS[::-1]:
        try:
            folder.rmdir()
        except OSError:
            print(f'Error during remove folder {folder}')

def start():
    if sys.argv[1]:
        folder_process = Path(sys.argv[1])
        main(folder_process)


