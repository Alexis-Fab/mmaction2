import sys, os, json
import find_next_cut
from ffmpy import FFmpeg
from os import path as osp

## TODO put root path as argument
rootPath = "/home/opekta/copaeurope/"
#trimmedVideosPath = osp.join(rootPath, "mmaction2/data/soccernet/trimmed")
labelsPath = osp.join(rootPath, "mmaction2/data/soccernet/SoccerNet_V1.1_Labels")
datasetPath = osp.join(rootPath, "mmaction2/data/soccernet/videos")
outputExtension = ".mp4"
videosLQPath = osp.join(rootPath, "mmaction2/data/soccernet/LQ")
soccernetClassesFile = open("soccernet_classes_conversion.json")
soccernetClassesJson = json.load(soccernetClassesFile)
classesDurationFile = open("classes_duration.json")
classesDurationJson = json.load(classesDurationFile)

def findShotAction(jsonAnnotation, halfTime, timingValue):
    for annotation in jsonAnnotation['annotations']:
        if annotation["visibility"] == "not shown":
            continue
        classe = getClasse(annotation)
        if (classe in ['Corner', 'FreeKick', 'Goal', 'Penalty']):
            actionTimeValue = 60*int(annotation['gameTime'][4:6]) + int(annotation['gameTime'][7:9])
            if (halfTime == annotation['gameTime'][0]) & (abs(actionTimeValue - timingValue) < 3):
                return True
    return False

def getClasse(annotation):
    if annotation['label'] in soccernetClassesJson["classes"]:
        return annotation['label']
    elif annotation['label'] in soccernetClassesJson["conversion"]:
        return soccernetClassesJson["conversion"][annotation['label']]
    else:
        return None

def main():

    for classe in soccernetClassesJson["classes"]:
        # Create folders to store trimmed copy videos ordered by action.
        tmpPath = osp.join(datasetPath, classe)
        os.makedirs(tmpPath, exist_ok=True)

    for root, dirs, files in os.walk(videosLQPath):

        # Create folders to store trimmed copy videos ordered by match.
    #    tmpPath = os.path.join(trimmedVideosPath, root[1+len(videosLQPath):])
    #    os.makedirs(tmpPath, exist_ok=True)

        labelFolder = osp.join(labelsPath, root[1+len(videosLQPath):])
        labelPath = osp.join(labelFolder, "Labels-v2.json")
        cutAnnotationsPath = osp.join(labelFolder, "Labels-cameras.json")
        ligueTrigram = root[1+len(videosLQPath):4+len(videosLQPath)]

        if osp.exists(labelPath):

            f = open(labelPath)
            annotationsData = json.load(f)
            f.close()
            videoFolder = osp.join(videosLQPath, annotationsData["UrlLocal"])
            folderName = osp.basename(osp.normpath(videoFolder))
            dateExtension = folderName[:10] + '_' + folderName[13:18]
            firstLettersHostTeam = folderName[19:22]

            for element in annotationsData['annotations']:

                if element["visibility"] == "not shown":
                    continue
                classe = getClasse(element)
                if classe is not None:
                    halfTime = element["gameTime"][0]
                    videoLQPath = osp.join(videoFolder, halfTime + ".mkv")
                    if osp.exists(videoLQPath):
                        start = 60*int(element['gameTime'][4:6]) + int(element['gameTime'][7:9])
                        newTrimmedPath = osp.join(datasetPath, classe + "//" + classe + '_'
                                        + ligueTrigram + '_' + dateExtension + '_'
                                        + firstLettersHostTeam + '_'
                                        + str(start + 45*60*(int(halfTime)-1))
                                        + outputExtension)
                        if osp.exists(newTrimmedPath):
                            print(newTrimmedPath, "already exists. Extraction is skipped")
                        else:
                            if (classe == 'Shot'):
                                alreadyDealt = findShotAction(annotationsData, halfTime, start)
                                if alreadyDealt:
                                    continue
    #                        start = int(element['gameTime'][4:]) - classesDurationJson[classe][1]
                            ff = FFmpeg(
                                inputs={videoLQPath: ['-fflags', 'genpts', '-y', '-an', "-ss",
                                                    str(start - classesDurationJson[classe]["anticipation"]),
                                                    '-t', str(classesDurationJson[classe]["duration"])]},
                                outputs={newTrimmedPath: ['-c', 'copy', '-copyts', '-avoid_negative_ts', 'make_zero']}
                            )
                            # print(ff.cmd)
                            # print('start', start)
                            # print('nextCut', nextCut)
                            # The usual command line can be found in ff.cmd
                            ff.run()

soccernetClassesFile.close()
classesDurationFile.close()

if __name__ == "__main__":
    main()
