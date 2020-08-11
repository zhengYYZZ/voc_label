import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join


def check_dir(dir):
    """
    创建文件夹
    :param dir:
    :return:
    """
    if not os.path.exists(dir):
        os.makedirs(dir)


def read_file(file_name):
    """
    读取txt文件内容
    :param file_name:文件位置
    :return:
    """
    with open(file_name,'r',encoding='utf-8') as file_object:
        data = file_object.read().splitlines()
    return data


def convert(size, box):
    """
    坐标转换
    :param size:长,宽
    :param box:x1,y1,x2,y2
    :return:
    """
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return x, y, w, h


def convert_annotation(path, save_path, image_id):

    image_id_basename = os.path.split(image_id)[-1]
    image_name = os.path.splitext(image_id_basename)[0]

    in_file = open('%s/%s.xml' % (path, image_name))
    check_dir(save_path)
    out_file = open('%s/%s.txt' % (save_path, image_name), 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

    in_file.close()
    out_file.close()


if __name__ == '__main__':
    classes = read_file('classes/classes.txt')
    image_ids = read_file('val.txt')
    for image_id in image_ids:
        convert_annotation('ORI','labels',image_id)