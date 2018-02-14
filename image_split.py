import os
from PIL import Image
from handle_image import handle

import string
CHARS = string.ascii_uppercase + string.digits
cnt = {}
for i in CHARS:
    cnt[i] = 0
source, target = '', ''


def split_to_train(path):
    imgs = handle(os.path.join(source, path))
    for i in range(4):
        imgs[i].save(os.path.join(target, path[i], str(cnt[path[i]]) + '.jpg'))
        cnt[path[i]] += 1


if __name__ == '__main__':
    import sys
    source, target = sys.argv[1], sys.argv[2]
    for i in CHARS:
        try:
            os.mkdir(os.path.join(target, i))
        except:
            pass
    files = os.listdir(os.path.join(source))
    for i in files:
        split_to_train(i)
        print(i)
    os.removedirs(os.path.join(target, '0'))
    os.removedirs(os.path.join(target, '1'))
    os.removedirs(os.path.join(target, 'O'))
    os.removedirs(os.path.join(target, 'I'))
    os.removedirs(os.path.join(target, 'L'))
