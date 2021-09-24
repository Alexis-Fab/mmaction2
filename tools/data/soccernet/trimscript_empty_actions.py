import os, json, argparse
from ffmpy import FFmpeg
from os import path as osp

outputExtension = ".jpg"

soccernetClassesFile = open("classes_conversion.json")
soccernetClassesJson = json.load(soccernetClassesFile)
soccernetClassesFile.close()

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

    os.makedirs(osp.join(targetRawframesFolder, "NoAction"), exist_ok=True)

    for root, dirs, files in os.walk(sourceVideos):
        labelFolder = osp.join(labelsPath, root[1+len(sourceVideos):])
        labelPath = osp.join(labelFolder, "Labels-v2.json")
        ligueTrigram = root[1+len(sourceVideos):4+len(sourceVideos)]

        if osp.exists(labelPath):

            f = open(labelPath)
            annotationsData = json.load(f)
            f.close()
            videoFolder = osp.join(sourceVideos, annotationsData["UrlLocal"])
            folderName = osp.basename(osp.normpath(videoFolder))
            dateExtension = folderName[:10] + '_' + folderName[13:18]
            firstLettersHostTeam = folderName[19:22]

            actionsMarks = []
            emptyMoments = []

            for element in annotationsData['annotations']:

                if element["visibility"] == "not shown":
                    continue
                classe = getClasse(element)
                if classe is not None:
                    halfTime = element["gameTime"][0]
                    videoLQPath = osp.join(videoFolder, halfTime + ".mkv")
                    start = 60*int(element['gameTime'][4:6]) + int(element['gameTime'][7:9])
                    actionsMarks.append(start)

            actionsMarks.sort()

            for i in range(len(actionsMarks)-1):
                if actionsMarks[i+1] - actionsMarks[i] > 60:
                    nbExtractions = (actionsMarks[i+1] - actionsMarks[i] - 60) // 15
                    for j in range(nbExtractions):
                        # on attend 30s après l'action annotée puis on extraira toutes les 10s des petites séquences (~3s) tant qu'on n'est pas à moins de 10s de l'action suivante
                        emptyMoments.append(actionsMarks[i] + (j+2) * 15)


            for momentStart in emptyMoments:

                newTrimmedPath = osp.join(targetRawframesFolder, "NoAction" + "/" + "NoAction_"
                                + ligueTrigram + '_' + dateExtension + '_'
                                + firstLettersHostTeam + '_'
                                + str(momentStart + 45*60*(int(halfTime)-1))
                                )

                os.makedirs(newTrimmedPath, exist_ok=True)
                newTrimmedPath = osp.join(newTrimmedPath, "img_%05d"
                                + outputExtension)

                if osp.exists(newTrimmedPath):
                    print(newTrimmedPath, "already exists. Extraction is skipped")
                else:
                    ff = FFmpeg(
                        inputs={videoLQPath: ['-y', '-ss',
                                            str(momentStart)
                                            ]},
                        outputs={newTrimmedPath: ['-qmin', '1', '-qscale:v', '2',
                                                '-frames:v', str(90)]}
                    )
                    # print(ff.cmd)
                    # print('start', start)
                    # print('nextCut', nextCut)
                    # The usual command line can be found in ff.cmd
                    ff.run()


if __name__ == "__main__":
    main()
