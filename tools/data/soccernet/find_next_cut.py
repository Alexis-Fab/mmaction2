import sys, os, json
from os import path as osp

## TODO put root path as argument
rootPath = "/home/opekta/copaeurope/"

def main(cutAnnotationsPath, actionTime):

    valueRef = 60*int(actionTime[4:6]) + int(actionTime[7:9])
    f = open(cutAnnotationsPath)
    cutJSON = json.load(f)
    f.close()
    annotations = cutJSON['annotations']
    nextCutFound = False

    for cut in annotations:
        cutValue = 60*int(cut['gameTime'][4:6])+int(cut['gameTime'][7:9])
        if (not nextCutFound) & (actionTime[0] == cut['gameTime'][0]) & (valueRef < cutValue):
            nextCutFound = True
            break
    return(cutValue)

if __name__ == "__main__":
    main()
