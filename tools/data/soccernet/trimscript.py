import sys, os, json, subprocess
import find_next_cut
from ffmpy import FFmpeg, FFprobe
#from ffprobe import FFProbe
from os import path as osp

## TODO put root path as argument
rootPath = "/home/opekta/copaeurope/"
#trimmedVideosPath = osp.join(rootPath, "mmaction2/data/soccernet/trimmed")
labelsPath = osp.join(rootPath, "mmaction2/data/soccernet/SoccerNet_V1.1_Labels")
datasetPath = osp.join(rootPath, "mmaction2/data/soccernet/videos")
outputExtension = ".mp4"
videosLQPath = "/media/opekta/CopaEurope/LQ"
soccernetClassesFile = open("soccernet_classes_conversion.json")
soccernetClassesJson = json.load(soccernetClassesFile)
classesDurationFile = open("classes_duration.json")
classesDurationJson = json.load(classesDurationFile)
classesIncrements = {}

for classe in soccernetClassesJson["classes"]:
    # Create folders to store trimmed copy videos ordered by action.
    tmpPath = osp.join(datasetPath, classe)
    os.makedirs(tmpPath, exist_ok=True)
    classesIncrements[classe] = 0

for root, dirs, files in os.walk(videosLQPath):

    # Create folders to store trimmed copy videos ordered by match.
#    tmpPath = os.path.join(trimmedVideosPath, root[1+len(videosLQPath):])
#    os.makedirs(tmpPath, exist_ok=True)

    labelFolder = osp.join(labelsPath, root[1+len(videosLQPath):])
    labelPath = osp.join(labelFolder, "Labels-v2.json")
    cutAnnotationsPath = osp.join(labelFolder, "Labels-cameras.json")

    if osp.exists(labelPath):

        f = open(labelPath)
        annotationsData = json.load(f)
        f.close()
        videoFolder = osp.join(videosLQPath, annotationsData["UrlLocal"])

        for element in annotationsData['annotations']:
            if element["visibility"] == "not shown":
                continue
            if element['label'] in soccernetClassesJson["classes"]:
                classe = element['label']
            elif element['label'] in soccernetClassesJson["conversion"]:
                classe = soccernetClassesJson["conversion"][element['label']]
            else:
                classe = None
            if classe is not None:
                halfTime = element["gameTime"][0]
                videoLQPath = osp.join(videoFolder, halfTime + ".mkv")
                if osp.exists(videoLQPath):
                    classesIncrements[classe] += 1
                    newTrimmedPath = osp.join(datasetPath, classe + "//" + classe + str(classesIncrements[classe]) + outputExtension)
                    if osp.exists(newTrimmedPath):
                        print(newTrimmedPath, "already exists. Extraction is skipped")
                    else:
 #                       metadata = FFprobe(videoLQPath)
#                         print('metadataaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
# #                        print(metadata.streams)
#                         tup_resp = FFprobe(
#                             inputs={videoLQPath: None},
#                             global_options=[
# #                                '-v', 'quiet',
#  #                               '-print_format', 'json',
#   #                              '-show_format', '-show_streams'
#                                  '-loglevel', 'error', '-select_streams', 'v:0',
#                                  '-show_entries', 'packet=pts_time,flags', '-of', 'csv=print_section=0'
#                             ]
#                         ).run(stdout=subprocess.PIPE)
# #                        print(tup_resp)
#                        metadata = json.loads(tup_resp[0].decode('utf-8'))
 #                       print(metadata)
                        # for stream in metadata.streams:
                        #     if stream.is_video():
                        #         print('Stream contains {} frames.'.format(stream.frames()))
                        nextCut = find_next_cut.main(cutAnnotationsPath, element['gameTime'])
#                        print("\n\n\n\n\n\n\n\n\n\n\n")
                        # print('actionTime', element['gameTime'])
                        # print('nextCut', nextCut)
#                        start = int(element['gameTime'][4:]) - classesDurationJson[classe][1]
                        start = 60*int(element['gameTime'][4:6]) + int(element['gameTime'][7:9])
                        duration = min(6, nextCut-start)
                        newTrimmedPath += f"_{duration}s.mp4"
                        ff = FFmpeg(
                            inputs={videoLQPath: ['-fflags', 'genpts', '-y', '-an', "-ss",
                                                    str(start), '-t', str(duration)]},
                            outputs={newTrimmedPath: ['-c', 'copy', '-copyts', '-avoid_negative_ts', 'make_zero']}
                        )
                        # print(ff.cmd)
                        # print('start', start)
                        # print('nextCut', nextCut)
                        # The usual command line can be found in ff.cmd
                        ff.run()

soccernetClassesFile.close()
classesDurationFile.close()