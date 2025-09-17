#!/bin/bash
bdir="build"
pdir="python"

# scrpt parameter
algorithms=("mult_basic")

echo "initializing..."
rm -r tests
mkdir -p tests/input
mkdir -p tests/output
mkdir -p tests/result
echo "initialization done"

echo "generating testcases..."
python3 $pdir/gen_tcases.py
echo "generation done"

echo "testing..."
for FILE in tests/input/*; do
    echo "- $FILE"
    $bdir/compare < $FILE > tests/result/${FILE##*/}
done
echo "testing done"

python3 $pdir/plot.py