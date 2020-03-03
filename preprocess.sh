#!/usr/bin/env bash

set -ex

cd `dirname $0`

mkdir -p processed

python3.6 preprocessImage.py -in "$1" -out "./processed/$2"

#example: bash preprocess.sh test.jpg test.png