import cv2
import os
import numpy as np

# data url: http://www.cs.toronto.edu/~kriz/cifar.html
imgData = np.load('./data_batch_1')['data']
srcData = np.load('./data_batch_1')
# keys: ['data', 'labels', 'batch_label', 'filenames']
if not os.path.exists('./img'):
    os.mkdir('./img')

for i in range(100):
    srcImg = imgData[i]
    R = srcImg[0:1024].reshape(32,32)
    G = srcImg[1024:2048].reshape(32,32)
    B = srcImg[2048:3072].reshape(32,32)
    img = np.stack([R,G,B], axis=0)
    img = img.transpose(1,2,0)
    imgName = np.load('./data_batch_1')['filenames'][i]
    cv2.imwrite('./img/{}.jpg'.format(str(i)), img)

print max(srcData['labels'])  # 9
print min(srcData['labels'])  # 0

print srcData['batch_label']  # 'training batch 1 of 5', 5W张训练集中的1W张

# filenames: such as 'american_saddle_horse_s_000008.png'
# typeNames
# ['airplane','automobile','bird','cat','deer','dog','frog','horse','ship','truck']