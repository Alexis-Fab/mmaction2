import argparse
import json, math
import os.path as osp
from collections import defaultdict

import matplotlib.pyplot as plt
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
import numpy as np
import seaborn as sns


def cal_train_time(log_dicts, args):
    for i, log_dict in enumerate(log_dicts):
        print(f'{"-" * 5}Analyze train time of {args.json_logs[i]}{"-" * 5}')
        all_times = []
        for epoch in log_dict.keys():
            if args.include_outliers:
                all_times.append(log_dict[epoch]['time'])
            else:
                all_times.append(log_dict[epoch]['time'][1:])
        all_times = np.array(all_times)
        epoch_ave_time = all_times.mean(-1)
        slowest_epoch = epoch_ave_time.argmax()
        fastest_epoch = epoch_ave_time.argmin()
        std_over_epoch = epoch_ave_time.std()
        print(f'slowest epoch {slowest_epoch + 1}, '
              f'average time is {epoch_ave_time[slowest_epoch]:.4f}')
        print(f'fastest epoch {fastest_epoch + 1}, '
              f'average time is {epoch_ave_time[fastest_epoch]:.4f}')
        print(f'time std over epochs is {std_over_epoch:.4f}')
        print(f'average iter time: {np.mean(all_times):.4f} s/iter')
        print()

def getScaleOrder(x):
    k=1
    i=10
    while(x//i != 0):
        if ( ((math.log10(i/9.8)) % 1) != 0):
            i=i+(10**k)/5
        else:
            k=k+1
            i=10**k
    return(i)

def getValAccuracy(logFile):
    with open(logFile,'r') as data:
        lines = data.readlines()
    top1 = []
    top5 = []

    iterPerEpochFound = False
    for line in lines:
        if 'metrics=[' in line:
            validationInterval = int(line[13:14]) #TODO add case interval greater than 9
        if 'mmaction - INFO - Epoch' in line:
            iterPerEpoch = int(line[57:60]) #TODO add case iter per epoch not in [100,999]
            print(iterPerEpoch)
            iterPerEpochFound = True
        if iterPerEpochFound:
            break

    for line in lines:
        if (line[:8]=='top1_acc'):
            top1.append(float(line[-7:]))
        elif (line[:8]=='top5_acc'):
            top5.append(float(line[-7:]))
    
    X = [validationInterval*iterPerEpoch*i for i in range(len(top1))]

    return {'top1':top1,'top5':top5,'X':X}

def plot_val(topk,valData,ax):
    Y=valData[topk]
    if topk == 'top1':
        label='val_top1'
    elif topk == 'top5':
        label='val_top5'
    else:
        raise KeyError('Only top1 and top5 are available for validation')

    plt.plot(valData['X'],Y,'#e63946',label=label,linewidth=1.8)


def plot_curve(log_dicts, args):
    if args.backend is not None:
        plt.switch_backend(args.backend)
#    sns.set_style(args.style)
    # if legend is None, use {filename}_{key} as legend
    legend = args.legend
    if legend is None:
        legend = []
        for json_log in args.json_logs:
            for metric in args.keys:
                legend.append(f'{json_log}_{metric}')
    assert len(legend) == (len(args.json_logs) * len(args.keys))
    metrics = args.keys

    num_metrics = len(metrics)
    for i, log_dict in enumerate(log_dicts):
        epochs = list(log_dict.keys())
        for j, metric in enumerate(metrics):
            if metric == 'top1':
                metric = 'top1_acc'
            if metric == 'top5':
                metric = 'top5_acc'
            print(f'plot curve of {args.json_logs[i]}, metric is {metric}')
            if metric not in log_dict[epochs[0]]:
                raise KeyError(
                    f'{args.json_logs[i]} does not contain metric {metric}')
            xs = []
            ys = []
            num_iters_per_epoch = log_dict[epochs[0]]['iter'][-1]
            for epoch in epochs:
                iters = log_dict[epoch]['iter']
                if log_dict[epoch]['mode'][-1] == 'val':
                    iters = iters[:-1]
                xs.append(np.array(iters) + (epoch - 1) * num_iters_per_epoch)
                ys.append(np.array(log_dict[epoch][metric][:len(iters)]))
            xs = np.concatenate(xs)
            ys = np.concatenate(ys)

            fig, ax = plt.subplots(figsize=(6.5, 5.5))

            # Set axis ranges; by default this will put major ticks every 25.
            xScaleOrder = getScaleOrder(xs[-1])
            # Below, it gives a little empty space before the y axis and it adjusts to a bit more than the xs length.
            ax.set_xlim(-(10**int((math.log10(xScaleOrder)-1))), xScaleOrder)

            # Change major ticks to show every 20.
            if (xScaleOrder/10**int(math.log10(xScaleOrder))<4):
                ax.xaxis.set_major_locator(MultipleLocator((10**int(math.log10(xScaleOrder)))/2))
            else:
                ax.xaxis.set_major_locator(MultipleLocator(10**int(math.log10(xScaleOrder))))

            # Change minor ticks to show every 5. (20/4 = 5)
            ax.xaxis.set_minor_locator(AutoMinorLocator(10))

            # Turn grid on for both major and minor ticks and style minor slightly
            # differently.
            ax.grid(which='major', color='#CCCCCC', linestyle='--')
            ax.grid(which='minor', color='#CCCCCC', linestyle=':')

            plt.xlabel('iter')
            if (legend[0][:3]=='top'): # Assumed that loss and top acc are not asked to be shown together
                plt.plot(xs, ys, '#023e8a', label=legend[i * num_metrics + j], linewidth=0.5)
                ax.set_ylim(0, 1)
                ax.yaxis.set_minor_locator(AutoMinorLocator(5))
                ax.yaxis.set_major_locator(MultipleLocator(0.1))
                if args.val:
                    if not osp.exists(args.json_logs[0][:-5]):
                        raise KeyError('There must be a .log file with the same name as the .log.json file in order to plot validation accuracy')
                    valData = getValAccuracy(args.json_logs[0][:-5])
                    plot_val(metric[:4],valData,ax)
            else:
                plt.plot(xs, ys, '#023e8a', label=legend[i * num_metrics + j], linewidth=0.5)
                ax.set_ylim(0, 2)
                ax.yaxis.set_minor_locator(AutoMinorLocator(4))
                ax.yaxis.set_major_locator(MultipleLocator(0.2))

            plt.legend()
            plt.grid(True)
        if args.title is not None:
            plt.title(args.title)
    if args.out is None:
        plt.show()
    else:
        print(f'save curve to: {args.out}')
        plt.savefig(args.out)
        plt.cla()


def add_plot_parser(subparsers):
    parser_plt = subparsers.add_parser(
        'plot_curve', help='parser for plotting curves')
    parser_plt.add_argument(
        'json_logs',
        type=str,
        nargs='+',
        help='path of train log in json format')
    parser_plt.add_argument(
        '--keys',
        type=str,
        nargs='+',
        default=['top1_acc'],
        help='the metric that you want to plot')
    parser_plt.add_argument('--title', type=str, help='title of figure')
    parser_plt.add_argument(
        '--legend',
        type=str,
        nargs='+',
        default=None,
        help='legend of each plot')
    parser_plt.add_argument(
        '--backend', type=str, default=None, help='backend of plt')
    parser_plt.add_argument(
        '--style', type=str, default='dark', help='style of plt')
    parser_plt.add_argument('--out', type=str, default=None)
    parser_plt.add_argument('--val', action='store_true')


def add_time_parser(subparsers):
    parser_time = subparsers.add_parser(
        'cal_train_time',
        help='parser for computing the average time per training iteration')
    parser_time.add_argument(
        'json_logs',
        type=str,
        nargs='+',
        help='path of train log in json format')
    parser_time.add_argument(
        '--include-outliers',
        action='store_true',
        help='include the first value of every epoch when computing '
        'the average time')


def parse_args():
    parser = argparse.ArgumentParser(description='Analyze Json Log')
    # currently only support plot curve and calculate average train time
    subparsers = parser.add_subparsers(dest='task', help='task parser')
    add_plot_parser(subparsers)
    add_time_parser(subparsers)
    args = parser.parse_args()
    return args


def load_json_logs(json_logs):
    # load and convert json_logs to log_dict, key is epoch, value is a sub dict
    # keys of sub dict is different metrics, e.g. memory, top1_acc
    # value of sub dict is a list of corresponding values of all iterations
    log_dicts = [dict() for _ in json_logs]
    for json_log, log_dict in zip(json_logs, log_dicts):
        with open(json_log, 'r') as log_file:
            for line in log_file:
                log = json.loads(line.strip())
                # skip lines without `epoch` field
                if 'epoch' not in log:
                    continue
                epoch = log.pop('epoch')
                if epoch not in log_dict:
                    log_dict[epoch] = defaultdict(list)
                for k, v in log.items():
                    log_dict[epoch][k].append(v)
    return log_dicts


def main():
    args = parse_args()

    json_logs = args.json_logs
    for json_log in json_logs:
        assert json_log.endswith('.json')

    log_dicts = load_json_logs(json_logs)

    eval(args.task)(log_dicts, args)


if __name__ == '__main__':
    main()
