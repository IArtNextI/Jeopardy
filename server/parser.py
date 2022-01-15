import xmltodict
import json
from os import listdir, rename
from os.path import join as path_join
from urllib.parse import unquote


def xmlToJson(filepath):
    with open(filepath, 'r', encoding='utf-8') as xml_file:
        data = xml_file.read()

    data = xmltodict.parse(data)
    return data


def decodeFileNames(directory):
    for filename in listdir(directory):
        rename(path_join(directory, filename), path_join(directory, unquote(filename)))


def parsePack(pack_path):
    decodeFileNames(path_join(pack_path, 'Audio'))
    decodeFileNames(path_join(pack_path, 'Images'))
    data = xmlToJson(path_join(pack_path, 'content.xml'))
    return data
