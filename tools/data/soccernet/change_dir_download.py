import os
import shutil
from os import path as osp

for dir1 in os.listdir('/media/opekta/CopaEurope/SoccerDB'):
    if (dir1[:11]=='videos-2021'):
        dir2=osp.join('/media/opekta/CopaEurope/SoccerDB/'+dir1,'videos')
        for file in os.listdir(dir2):
            shutil.move(osp.join(dir2,file),'/media/opekta/CopaEurope/SoccerDB/videos')
            