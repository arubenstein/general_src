#!/bin/bash

i=$1

weblogo -s large -F png -U probability -A protein -f $i -o ${i%.transfac}.png
