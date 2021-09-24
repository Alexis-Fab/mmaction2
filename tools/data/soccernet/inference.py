import torch, time, os
from os import path as osp
from mmaction.apis import init_recognizer, inference_recognizer

#TODO parse arguments from bash script
def main():
    config_file = "/home/opekta/copaeurope/mmaction2/configs/recognition/slowfast/slowfast_r50_8x8x1_256e_soccernet_rgb.py"
    checkpoint_file1 = "/home/opekta/copaeurope/mmaction2/checkpoints/slowfast_r50_8x8x1_256e/2021 09 15 NoAction/epoch_760.pth"
    checkpoint_file2 = "/home/opekta/copaeurope/mmaction2/checkpoints/slowfast_r50_8x8x1_256e/2021 09 15 NoAction/best_top1_acc_epoch_288.pth"
    device = 'cuda:0'
    device = torch.device(device)

    rawframesList=[]
    for root,dirs,files in os.walk("/home/opekta/copaeurope/mmaction2/data/soccernet/tests"):
        if root == "/home/opekta/copaeurope/mmaction2/data/soccernet/tests":
            continue
        rawframesList.append(root)
    # rawframesList.append("/home/opekta/copaeurope/mmaction2/data/soccernet/tests/cb70205ecc7511e885786c96cfde8f")
    # rawframesList.append("/home/opekta/copaeurope/mmaction2/data/soccernet/tests/d4b14afed5ac11e8b2536c96cfde8f-021")
    # rawframesList.append("/home/opekta/copaeurope/mmaction2/data/soccernet/tests/d5d712d8d5ac11e8b2536c96cfde8f-062")
    # rawframesList.append("/home/opekta/copaeurope/mmaction2/data/soccernet/tests/d9d9ea54d5ac11e8b2536c96cfde8f-055")
    # rawframesList.append("/home/opekta/copaeurope/mmaction2/data/soccernet/tests/Nova_2")
    labels = "/home/opekta/copaeurope/mmaction2/data/soccernet/annotations/label_map_soccernet.txt"

    for checkpoint_file in [checkpoint_file1, checkpoint_file2]:

        model = init_recognizer(config_file, checkpoint_file, device=device, use_frames=True)
        print(model.test_cfg['average_clips'])
#        model.test_cfg['average_clips']='score'
        print(model.test_cfg)
        for rawframes in rawframesList:
            t0 = time.time()
            results=inference_recognizer(model, rawframes, labels, use_frames=True)
            t1 = time.time()
            print(checkpoint_file[-13:])
            print(f'Inference for {osp.basename(rawframes)} took {t1-t0} seconds')
            print('The top5 labels with corresponding scores are :')
            for result in results:
                print(f'{result[0]}: ', result[1])

if __name__=='__main__':
    main()
