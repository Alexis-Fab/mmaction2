import os
from os import path as osp
from posix import listdir
from ffmpy import FFmpeg

outputExtension = '.jpg'

sourceFolder = '/media/opekta/CopaEurope/SoccerDB/videos/China Association Super League'
videoName = 'cb70205ecc7511e885786c96cfde8f.mp4'
video = osp.join(sourceFolder, videoName)
destination = osp.join('/home/opekta/copaeurope/mmaction2/data/soccernet/tests', videoName[:-4])
destinationFrame = osp.join(destination, "img_%05d" + outputExtension)

if osp.exists(destination):
    for file in listdir(destination):
        os.remove(osp.join(destination,file))
else:
    os.makedirs(destination, exist_ok=True)

hourStart=0
minuteStart=34
secondStart=50
start=3600*hourStart+60*minuteStart+secondStart
hourEnd=0
minuteEnd=34
secondEnd=53
end=3600*hourEnd+60*minuteEnd+secondEnd

ff = FFmpeg(
    inputs={video: ['-y', '-an', '-ss', str(start),
            '-to', str(end)]},
            outputs={destinationFrame: ['-r', '30', '-qmin', '1', '-qscale:v', '2', '-vf', 'scale=398:224']}
)
ff.run()
