from genericpath import exists
import os
from ffmpy import FFmpeg
from os import path as osp

root='/home/opekta/copaeurope/mmaction2'
folders = [osp.join(root,'data/soccernet/extractedFrames/Penalty')]#,osp.join(root,'data/soccernet/extractedFrames/RedCard')]

for folder in folders:
    # for r00t, dirs, files in os.walk(folder):
    #     for file in files:
    #         if file == 'i.jpg':
    #             print(file)
    for dir in os.listdir(folder):
        if dir[0] in ['c','d']:
            dirPath=osp.join(folder,dir)
            flippedDirPath=dirPath+'_flipped'
            os.makedirs(flippedDirPath,exist_ok=True)
            for file in os.listdir(dirPath):
                image=osp.join(dirPath,file)
                flippedImage=osp.join(flippedDirPath, file)
                print(flippedImage)
                ff=FFmpeg(
                    inputs={image: ['-y', '-an']},
                    outputs={flippedImage: ['-vf', 'hflip']}
                )
                ff.run()