#!/usr/bin/env bash

cd ../
python build_rawframes.py ../../data/soccernet/videos/ ../../data/soccernet/rawframes/ --ext mp4 --task rgb --level 2 --flow-type tvl1 --num-worker 8 --resume --use-opencv
echo "Raw frames (RGB and Flow) Generated"
cd soccernet/
