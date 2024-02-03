from PIL import Image
from icrawler.builtin import BingImageCrawler
import os
import shutil

#ПЕРЕД ИСПОЛЬЗВОАНИЕ ПРОЧИТАТЬ!!!!!
#Данный скрипт сможет увеличить ваш датасет очень легко и достаточно быстро
#Данный скрипт не является обезательным к использованию, но может сильно облегчить работу с datasince
#Скрипт рабтает с библиотекой icrawler ПРИ ИСПОЛЬЗВОВАНИИ ВЕРСИЯ ПАЙТОНА ДОЛЖНА БЫТЬ МЕНЬШЕ 3.12(icrawler не поддерживает 3.12)

#----ГАЙД НА ЗАПУСК СКРИПТА----
#для начала укажите в переменной dirr путь до папки куда будем скачавать картинки
#следующим шагом укажите в массиве keywords,слова или выражения, по которым будет вестись поиск в интренете, в кейвордс можете указывать сколько угодно поисковых запросов
#Дальше нам нужно выставить количество картинок для скачивания, для этого меняем переменную int_pic_download
#дальше запустим нашии функции create_folders(dirr, keywords), people_crawl(), move_files(dirr), remove_folders_with_prefix(dirr, prefix)- create_folders() создаст нужное колличество папок(по колличеству кейвордов) в указаной дерриктории
#после чего people_crawl() скачает нужное вам колличество картинок(int_pic_download), move_files отвечает за переименовку файлов в каждой папке на нужное имя(icrawler скачвает картинки как 00001, 00002 и тд),
#и переносит все картинки в одну папку, после чего не нужны папки удаляет remove_folders_with_prefix(dirr, prefix)


papka_delite_name = 'images' #начало названия файлов
prefix = papka_delite_name + '_crawler' #основное название картинки
dirr = 'C:/Users/Admin/Desktop/29_01_yolo_gun_detect/detect_pack/images/train/dete' #путь к папке куда скачивать картинки
lener_mass = []
mass_train = []
dir_mass = []
keywords = [
    "Фотографии вооруженных сил",
    "Фото людей с огнестрельным оружием",
    "Фото солдат с огнестрельным оружием",
    "Фото вооруженных милиционеров",
    "Изображения людей с оружием",
    "Фото мужчин с оружием",
    "Фотографии вооруженных граждан",
    "Фото вооруженной группы"
    ] #список слов по которым будет работать поиск картинки


#---Функция-на-создание-папок-по-кейвордам----
def create_folders(dirr, keywords):
    for i in range(len(keywords)):
        folder_name = "images_crawler" + str(i)
        folder_path = os.path.join(dirr, folder_name)
        os.makedirs(folder_path)


#---Основная-функиция-скачивания-картинок---
def people_crawl():
    pass_dirr = dirr
    for i in range(len(keywords)):
        pass_dirr = pass_dirr + '/' + 'images_crawler' + str(i) + '/'
        #print(pass_dirr)
        bing_crawler = BingImageCrawler(parser_threads=8, downloader_threads=10, storage={'root_dir': pass_dirr})
        # потеря при скачивании картинок от 0 - 10%*(потери при скачиванни картинок по 100шт)
        #так же потери при скачивании сильно завыисят от интернета
        int_pic_download = 100 #сколько картинок скачается на каждое слово из keywords
        bing_crawler.crawl(keyword=keywords[i], max_num=int_pic_download)
        pass_dirr = dirr


#---перенос-всех-фотографий-в-одну-папку---
def move_files(dirr):
    path=dirr
    dest_folder = os.path.join(path, "images_all")
    os.makedirs(dest_folder, exist_ok=True)
    file_counter = 409
    for folder_name in os.listdir(path):
        if folder_name.startswith(prefix):
            folder_path = os.path.join(path, folder_name)
            for file_name in os.listdir(folder_path):
                if file_name.endswith(".jpg"):
                    src_file = os.path.join(folder_path, file_name)
                    dest_file = os.path.join(dest_folder, "images" + str(file_counter).zfill(3) + ".jpg")
                    shutil.move(src_file, dest_file)
                    file_counter += 1


#---Функиция-на-удаление-не-нужных-папок---
def remove_folders_with_prefix(dirr, prefix):
    for filename in os.listdir(dirr):
        if filename.startswith(prefix) and os.path.isdir(os.path.join(dirr, filename)):
            folder_path = os.path.join(dirr, filename)
            os.rmdir(folder_path)


create_folders(dirr, keywords)
people_crawl()
move_files(dirr)
remove_folders_with_prefix(dirr, prefix)