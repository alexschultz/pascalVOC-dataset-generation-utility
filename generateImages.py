import cv2
import os
import random
import annotations

BG_PATH = './backgroundImages/'
EDITED_PATH = './edited/'
OUTPUT_PATH = './VOC2018/JPEGImages/'

FILE_COUNT = 2000
TRAIN_SPLIT = 0.8

bgFiles = os.listdir(BG_PATH)
editedFile = os.listdir(EDITED_PATH)


def getRandomEditedFile():
    return editedFile[random.randint(0, len(editedFile) - 1)]


def getRandomBackgroundFile():
    return bgFiles[random.randint(0, len(bgFiles) - 1)]


def getRandomROIStartPoint(bgImage, overlay):
    h, w, _ = overlay.shape
    maxH, maxW, _ = bgImage.shape
    retHeight = random.randint(0, maxH - h)
    retWidth = random.randint(0, maxW - w)
    return retHeight, retWidth


def getRandomScaleFactor():
    return random.uniform(.75, 1.25)


def createTestTrainSplitFile():
    files = os.listdir(OUTPUT_PATH)
    trainFileCount = int(FILE_COUNT * TRAIN_SPLIT)
    testFileCount = FILE_COUNT - trainFileCount
    print('{} files for training; {} file for testing'.format(trainFileCount, testFileCount))
    trainFiles = files[:trainFileCount]
    testFiles = files[trainFileCount:]
    print('total files: {}; training files count {}; testingFiles count {}'.format(FILE_COUNT, trainFileCount,
                                                                                   testFileCount))

    with open('./VOC2018/ImageSets/trainval.txt', 'w') as x:
        for f in trainFiles:
            print('training file: {}'.format(f))
            x.writelines('{}\n'.format(f[:-4]))

    with open('./VOC2018/ImageSets/test.txt', 'w') as x:
        for f in testFiles:
            print('test file: {}'.format(f))
            x.writelines('{}\n'.format(f[:-4]))


for x in range(FILE_COUNT):
    if x % 5 == 0:
        print('progress: {} out of {}'.format(x + 1, FILE_COUNT))

    backgroundFile = BG_PATH + getRandomBackgroundFile()
    overlayFile = EDITED_PATH + getRandomEditedFile()

    bgSrc = cv2.imread(backgroundFile, cv2.IMREAD_COLOR)
    bgImg = cv2.resize(bgSrc, None, fx=2, fy=2)

    olSrc = cv2.imread(overlayFile, cv2.IMREAD_COLOR)

    scaleFactor = getRandomScaleFactor()
    olImg = cv2.resize(olSrc, None, fx=scaleFactor, fy=scaleFactor)

    h, w = getRandomROIStartPoint(bgImg, olImg)
    olh, olw, _ = olImg.shape
    bgImg[h:(h + olh), w:(w + olw)] = olImg
    outHeight, outWidth, outputChans = bgImg.shape
    cv2.imwrite('{}generated-{}.jpg'.format(OUTPUT_PATH, x), bgImg)
    annotations.generateAnnotationFile('{}generated-{}.jpg'.format(OUTPUT_PATH, x), outHeight, outWidth, outputChans, w,
                                       h, (w + olw), (h + olh))

createTestTrainSplitFile()
