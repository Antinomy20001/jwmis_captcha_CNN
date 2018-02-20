from PIL import Image
import sys


def depoint(img):  # input: gray image
    pixdata = img.load()
    w, h = img.size
    for i in [0, h - 1]:
        for j in range(w):
            pixdata[j, i] = 255
    for i in [0, w - 1]:
        for j in range(h):
            pixdata[i, j] = 255
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            count = 0
            limit = 200
            if pixdata[x, y - 1] > limit:  # 上
                count = count + 1
            if pixdata[x, y + 1] > limit:  # 下
                count = count + 1
            if pixdata[x - 1, y] > limit:  # 左
                count = count + 1
            if pixdata[x + 1, y] > limit:  # 右
                count = count + 1
            if pixdata[x - 1, y - 1] > limit:  # 左上
                count = count + 1
            if pixdata[x - 1, y + 1] > limit:  # 左下
                count = count + 1
            if pixdata[x + 1, y - 1] > limit:  # 右上
                count = count + 1
            if pixdata[x + 1, y + 1] > limit:  # 右下
                count = count + 1
            if count > 4:
                pixdata[x, y] = 255
    return img


def binary(img):
    pixdata = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            limit = 200
            if pixdata[x, y] > limit:
                pixdata[x, y] = 255
            else:
                pixdata[x, y] = 0
    return img


def crop(img):
    spt = [2, 32, 62, 92, 122]
    y_min, y_max = 0, 54
    imgs = [img.crop([u, y_min, v, y_max]) for u, v in zip(spt[:-1], spt[1:])]
    return imgs


def handle(path):
    return crop(binary(depoint(depoint(depoint(Image.open(path).convert('L'))))))
