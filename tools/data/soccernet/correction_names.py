import os
from os import path as osp

folder = "/home/opekta/copaeurope/mmaction2/data/soccernet/extractedFrames/Penalty"

for root, dirs, files in os.walk(folder):
    for dir in dirs:
        if dir[-4:]=='de8f':
            dirPath=osp.join(root,dir)
            for file in os.listdir(dirPath):
                # if (int(file[-7:-4])<=30) or (int(file[-7:-4])>120):
                #     print(file)
                #     os.remove(osp.join(dirPath,file))
                # newFile = file[:-7]+format(int(file[-7:-4])-30, '03d')+'&'+file[-4:]
                # print(newFile)
                print(file)
#                os.rename(osp.join(dirPath,file), osp.join(dirPath,file[:-5]+file[-4:]))
#        if (file[-11:]=='flipped.jpg'):
#        print(osp.join(root,file[:-12]+file[-4:]))
#            os.rename(osp.join(root,file),osp.join(root,file[:-12]+file[-4:]))
