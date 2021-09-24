import os, json, argparse
from ffmpy import FFmpeg
from os import path as osp


outputExtension = ".jpg"

soccernetClassesFile = open("classes_conversion.json")
soccernetClassesJson = json.load(soccernetClassesFile)
soccernetClassesFile.close()
classesDurationFile = open("classes_duration.json")
classesDurationJson = json.load(classesDurationFile)
classesDurationFile.close()

def parse_args():
    parser = argparse.ArgumentParser(description='Extract frames from full videos given labels annotation')
    parser.add_argument(
        'root',
        type=str,
        help='Folder containing the environment. eg. home/opekta/copaeurope'
    )
    parser.add_argument(
        'dataset',
        type=str,
        help='Name of the dataset'
    )
    parser.add_argument(
        'source',
        type=str,
        help='Folder of the full videos'
    )
    return(parser.parse_args())

def findShotAction(jsonAnnotation, halfTime, timingValue):
    for annotation in jsonAnnotation['annotations']:
        if annotation['visibility'] == "not shown":
            continue
        classe = getClasse(annotation)
        if (classe in ['FreeKick', 'Penalty']):
            actionTimeValue = 60*int(annotation['gameTime'][4:6]) + int(annotation['gameTime'][7:9])
            if (halfTime == annotation['gameTime'][0]) & (abs(actionTimeValue - timingValue) <= 1):
                return True
    return False

def followedByAGoal(jsonAnnotation, halfTime, timingValue):
    for annotation in jsonAnnotation['annotations']:
        if annotation['visibility'] == "not shown":
            continue
        classe = getClasse(annotation)
        if (classe == 'Goal'):
            actionTimeValue = 60*int(annotation['gameTime'][4:6]) + int(annotation['gameTime'][7:9])
            if ((halfTime == annotation['gameTime'][0]) & (abs(actionTimeValue - timingValue) <= 2)):
                return True
    return False


def getClasse(annotation):
    if annotation['label'] in soccernetClassesJson['classes']:
        return annotation['label']
    if annotation['label'] in soccernetClassesJson['conversion']:
        return soccernetClassesJson['conversion'][annotation['label']]
    return None


def main():

    args=parse_args()
    rootPath=args.root
    dataset=args.dataset
    sourceVideos=args.source

    rootPath = "/home/opekta/copaeurope/"
    dataset='soccernet'
    labelsPath = osp.join(rootPath, "mmaction2/data/"+dataset+"/labels")
    targetRawframesFolder = osp.join(rootPath, "mmaction2/data/"+dataset+"/extractedFrames")

    for classe in soccernetClassesJson['classes']:
        # Create folders to store trimmed copy videos ordered by action.
        tmpPath = osp.join(targetRawframesFolder, classe)
        os.makedirs(tmpPath, exist_ok=True)

    for root, dirs, files in os.walk(sourceVideos):

        # Create folders to store trimmed copy videos ordered by match.
    #    tmpPath = os.path.join(trimmedVideosPath, root[1+len(sourceVideos):])
    #    os.makedirs(tmpPath, exist_ok=True)

        labelFolder = osp.join(labelsPath, root[1+len(sourceVideos):])
        labelPath = osp.join(labelFolder, "Labels-v2.json")
#        cutAnnotationsPath = osp.join(labelFolder, "Labels-cameras.json")
        ligueTrigram = root[1+len(sourceVideos):4+len(sourceVideos)]

        if osp.exists(labelPath):

            f = open(labelPath)
            annotationsData = json.load(f)
            f.close()
            videoFolder = osp.join(sourceVideos, annotationsData["UrlLocal"])
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
                        if (classe == 'Shot') & findShotAction(annotationsData, halfTime, start):
                            continue
                        if ((classe == 'Shot') & (followedByAGoal(annotationsData, halfTime, start))):
                            newTrimmedPath = osp.join(targetRawframesFolder, classe + "/" + classe + '_'
                                            + ligueTrigram + '_' + dateExtension + '_'
                                            + firstLettersHostTeam + '_'
                                            + str(start + 45*60*(int(halfTime)-1))
                                            )
                        else:
                            newTrimmedPath = osp.join(targetRawframesFolder, classe + "/" + classe + '_'
                                            + ligueTrigram + '_' + dateExtension + '_'
                                            + firstLettersHostTeam + '_'
                                            + str(start + 45*60*(int(halfTime)-1))
                                            )
                        os.makedirs(newTrimmedPath, exist_ok=True)
                        newTrimmedPath = osp.join(newTrimmedPath, "img_%05d"
                                        + outputExtension)
                        if osp.exists(newTrimmedPath):
                            print(newTrimmedPath, "already exists. Extraction is skipped")
                        else:
    #                        start = int(element['gameTime'][4:]) - classesDurationJson[classe][1]
                            ff = FFmpeg(
                                inputs={videoLQPath: ['-y', '-ss',
                                                    str(start - classesDurationJson[classe]["anticipation"])
                                                    ]},
                                outputs={newTrimmedPath: ['-qmin', '1', '-qscale:v', '2',
                                                        '-frames:v', str(classesDurationJson[classe]["duration"])]}
                            )
                            # print(ff.cmd)
                            # print('start', start)
                            # print('nextCut', nextCut)
                            # The usual command line can be found in ff.cmd
                            ff.run()


if __name__ == "__main__":
    main()
