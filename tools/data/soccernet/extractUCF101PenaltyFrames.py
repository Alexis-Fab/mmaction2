import os
from os import path as osp
from ffmpy import FFmpeg

srcFolder = '/home/opekta/copaeurope/mmaction2/data/soccernet/penaltyFromUCF101'
targetFolder = '/home/opekta/copaeurope/mmaction2/data/soccernet/extractedFrames/Penalty'
outputExtension = ".jpg"

#for root, dirs, files in os.walk(srcFolder):
for file in os.listdir(srcFolder):
    videoPath=osp.join(srcFolder,file)
    targetPath=osp.join(targetFolder,file[:-4])
    os.makedirs(targetPath, exist_ok=True)
    targetPath=osp.join(targetPath,'img_%5d'+outputExtension)
    if osp.exists(targetPath):
        print(targetPath, "already exists. Extraction is skipped")
    else:
        ff = FFmpeg(
            inputs={videoPath: ['-y']},
            outputs={targetPath: ['-qmin', '1', '-qscale:v', '2', '-vf', 'scale=398:224']}
        )
        ff.run()