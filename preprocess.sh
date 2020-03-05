#!/usr/bin/env bash

set -ex

cd `dirname $0`

mkdir -p processed

for file in ./images/Original/*; do
  {
    python3.6 preprocessImage.py -in "./images/Original/${file##*/}" -mask "./images/Mask/${file##*/}" -out "./images/processed/${file##*/}"
  }
done



