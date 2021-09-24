import os, argparse
from os import path as osp
import matplotlib.pyplot as plt
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)

def parse_args():
    parser = argparse.ArgumentParser(description='Plot top k accuracy on validation set')
    parser.add_argument('--top1',
                        action='store_true')
    parser.add_argument('--top5',
                        action='store_true')
    parser.add_argument('--both',
                        action='store_true')
    return parser.parse_args()

def main():

    dataPath = '/home/opekta/copaeurope/mmaction2/data/soccernet/valtopk.txt'

    args = parse_args()

    with open(dataPath,'r') as data:
        lines = data.readlines()

    top1 = []
    top5 = []

    for line in lines:
        top1.append(float(line[:6]))
        top5.append(float(line[7:14]))

    X = [5*467*(i) for i in range(len(top1))]

    if args.top1 or args.both:
        Y=top1
        label='val_top1'
    if args.top5 or args.both:
        Y=top5
        label='val_top5'
    if args.both or args.top1 or args.top5:

        fig, ax = plt.subplots(figsize=(6.5, 5.5))

        # Set axis ranges; by default this will put major ticks every 25.
        ax.set_xlim(-10000, 450000)
        ax.set_ylim(0, 1)

        # Change major ticks to show every 20.
        ax.xaxis.set_major_locator(MultipleLocator(100000))
        ax.yaxis.set_major_locator(MultipleLocator(0.1))

        # Change minor ticks to show every 5. (20/4 = 5)
        ax.xaxis.set_minor_locator(AutoMinorLocator(10))
        ax.yaxis.set_minor_locator(AutoMinorLocator(5))

        # Turn grid on for both major and minor ticks and style minor slightly
        # differently.
        ax.grid(which='major', color='#CCCCCC', linestyle='--')
        ax.grid(which='minor', color='#CCCCCC', linestyle=':')

        plt.xlabel('iter')

        plt.plot(X,Y,'#e63946',label=label,linewidth=0.9)
        plt.legend()
        plt.grid(True)

        plt.show()
    else:
        print('Please provide at least --top1 or --top5 as argument')

if __name__ == '__main__':
    main()