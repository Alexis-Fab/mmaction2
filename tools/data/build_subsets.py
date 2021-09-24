import os, random, argparse
from os import path as osp

## TODO put root path as argument
def parse_args():
    parser = argparse.ArgumentParser(description='Split files in train, val, test')
    parser.add_argument(
        'dataset',
        type=str,
        help='name of the folder containing the data. Must be root/mmaction2/data/myDataSet'
    )
    parser.add_argument(
        'root_folder', type=str, help='path to the folder containing mmaction2'
    )
    parser.add_argument(
        '--with_test', type=bool, default=False, help='Save some files for final testing'
    )
    parser.add_argument(
        '--format', type=str, default='videos', choices=['videos', 'rawframes'], help='Data format, videos or rawframes'
    )
    args=parser.parse_args()
    
    return args

def main():
    args=parse_args()
    rootPath = args.root_folder
    annotationPath = osp.join(rootPath, 'mmaction2/data/'+args.dataset+'/annotations')
    datasetPath = osp.join(rootPath, 'mmaction2/data/'+args.dataset+'/extractedFrames') #TODO change to args.format
#    datasetPath = osp.join(rootPath, 'mmaction2/data/'+args.dataset+'/'+args.format)
    valProportion = 0.1
    if args.with_test:
        trainProportion, testProportion = 0.8, 0.1
    else:
        trainProportion, testProportion = 0.9, 0
    assert trainProportion + valProportion + testProportion == 1

    filetrain = open(osp.join(annotationPath, "trainlist.txt"),"w+")
    fileval = open(osp.join(annotationPath, "vallist.txt"),"w+")
    filetest = open(osp.join(annotationPath, "testlist.txt"),"w+")

    for dir in os.listdir(datasetPath):
        for file in os.listdir(osp.join(datasetPath, dir)):
            myRandom2 = random.uniform(0,1)
            if (file[:4]=='Foul'):
                continue
            if (file[:6]=='Corner') & (myRandom2 > 0.4):
                continue
            if (file[:8]=='FreeKick') & (myRandom2 > 0.8):
                continue
            if (file[:4]=='Goal') & (myRandom2 > 0.9):
                continue
            if (file[:4]=='Shot') & (myRandom2 > 0.15):
                continue
            if (file[:10]=='YellowCard') & (myRandom2 > 0.8):
                continue
            if (file[:8]=='NoAction') & (myRandom2 > 0.1):
                continue
            myRandom = random.uniform(0,1)
            if myRandom <= trainProportion:
                filetrain.write(osp.join(dir,file)+"\n")
            elif myRandom <= trainProportion + valProportion:
                fileval.write(osp.join(dir,file)+"\n")
            else:
                filetest.write(osp.join(dir,file)+"\n")

    filetrain.close()
    fileval.close()
    filetest.close()

if __name__ == '__main__':
    main()