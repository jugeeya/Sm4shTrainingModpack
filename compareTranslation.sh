#!/bin/bash

python3 gameToEffectScript.py $1 > comparison.txt
diff -u comparison.txt $1 > diff.txt
rm comparison.txt
emacs diff.txt
