#!/bin/bash
sdir="src"
bdir="build"

rm -rf $bdir
mkdir -p $bdir

echo "compiling..."
g++ -std=c++11 -Wall -Wextra -Werror -O3 $sdir/*.cpp -o $bdir/run_algo
echo "compilation done"