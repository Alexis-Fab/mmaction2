import os, json
from os import path as osp
from ffmpy import FFmpeg
import csv

classIndFile=open('soccerdb_class_ind.json')
classIndJSON=json.load(classIndFile)
classIndFile.close()
soccerdbVideosPath='/media/opekta/CopaEurope/SoccerDB/videos'
targetFolder='/home/opekta/copaeurope/mmaction2/data/soccernet/extractedFrames'

outputExtension='.jpg'

with open('soccerdb_seg_info.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        if (row[0][:6]=='seg_id'):
            continue
        # print('\n',row)
        # print(len(row))
        splitted=[]
        for rowPart in row:
            element=rowPart.split(',')
            for x in element:
                splitted.append(x)
        # print(splitted)
        # print(len(splitted))
        if (splitted[1][-4:] != '.mp4'):
            continue
        event_labels=[]
        for i in range(6, len(splitted)-1):
            event_labels.append(splitted[i])
            if (classIndJSON['events'][splitted[i]] == "Penalty"):
                print(classIndJSON['events'][splitted[i]])
                start=3600*int(splitted[4][:2])+60*int(splitted[4][3:5])+int(splitted[4][6:8])
                print(start)
                end=3600*int(splitted[5][:2])+60*int(splitted[5][3:5])+int(splitted[5][6:8])
                print(end)
                print(splitted[1][:-4],'\n')
                for root, dirs, files in os.walk(soccerdbVideosPath):
                    for file in files:
                        if (file[:30] == splitted[1][:-4]):
                            videoPath=osp.join(root,file)
                            targetVideoFolder=osp.join(targetFolder,classIndJSON['events'][splitted[i]]+'/'+file[:30])
                            os.makedirs(targetVideoFolder, exist_ok=True)
                            targetImage = osp.join(targetVideoFolder, "img_%05d"
                                            + outputExtension)
                            print(videoPath)
                            print(targetImage)
                            ff = FFmpeg(
                                inputs={videoPath: ['-y', '-ss',
                                                    str(start), '-to', str(end)
                                                    ]},
                                outputs={targetImage: ['-qmin', '1', '-qscale:v', '2', '-vf', 'scale=398:224']}
                            )
                            ff.run()
