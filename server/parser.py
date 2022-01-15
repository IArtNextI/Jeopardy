import xmltodict
import json
from os import listdir, rename
from os.path import join as path_join
from urllib.parse import unquote


def xmlToJson(filepath):
    with open(filepath, 'r', encoding='utf-8') as xml_file:
        data = xml_file.read()

    d = xmltodict.parse(data)
    return json.loads(d)


def decodeFileNames(directory):
    print(directory)
    for filename in listdir(directory):
        print(filename, unquote(filename))
        rename(path_join(directory, filename), path_join(directory, unquote(filename)))


def parsePack(pack_path):
    print(pack_path)
    decodeFileNames(path_join(pack_path, 'Audio'))
    decodeFileNames(path_join(pack_path, 'Images'))
    return xmlToJson(path_join(pack_path, 'content.xml'))
