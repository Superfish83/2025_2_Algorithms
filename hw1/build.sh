#!/bin/bash
sdir="src"
bdir="build"

rm -rf $bdir
mkdir -p $bdir

echo "compiling..."
g++ -std=c++11 -Wall -Wextra -Werror -O1 $sdir/*.cpp -o $bdir/compare
echo "compilation done"