import os
from ffmpy import FFmpeg

src='/home/opekta/Downloads/y2mate.com - Furious Red Cards Moments In Football 2021_1080pFHR.mp4'
os.makedirs('/home/opekta/copaeurope/mmaction2/data/soccernet/fromYouTube', exist_ok=True)
os.makedirs('/home/opekta/copaeurope/mmaction2/data/soccernet/fromYouTube/RedCard',exist_ok=True)
finalPath='/home/opekta/copaeurope/mmaction2/data/soccernet/fromYouTube/RedCard/Furious Red Cards Moments In Football 2021_'

nb=0
finalPath+=str(nb)+'.mp4'
minuteStart=7
secondStart=44
start=60*minuteStart+secondStart
minuteEnd=7
secondEnd=47
end=60*minuteEnd+secondEnd

ff = FFmpeg(
    inputs={src: ['-fflags', 'genpts', '-y', '-an', '-ss', str(start),
            '-to', str(end)]},
    outputs={finalPath: ['-avoid_negative_ts', 'make_zero']}
)
ff.run()