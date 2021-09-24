 #!/usr/bin/env bash

cd ../../../

PYTHONPATH=. python tools/data/build_file_list.py soccernet data/soccernet/extractedFrames/ --level 2 --num-split 1 --format rawframes --shuffle
echo "Filelist for videos generated."

cd tools/data/soccernet/
