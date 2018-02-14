from PIL import Image
import os
import shutil

if __name__ == '__main__':
    src = 'dataset/'
    dst = 'train_image/'
    files = sorted(os.listdir(src))
    cnt = 0
    try:
        for i in files:
            cnt += 1
            Image.open(src + i).save('tmp.jpg')
            path = input(src + i + ': ').upper()
            shutil.move(src + i, dst + path + '.jpg')
            # os.rename(src + i, src + path + '.jpg')
    except KeyboardInterrupt as e:
        print('dama: %d' % cnt)