#!/usr/bin/env bash

if [[ ! -d "work/output" ]]; then
    echo "No output directory found, have you ran appstream-builder?"
fi

pushd work/output

if [[ ! -d "mirror/source" ]]; then
    mkdir -p mirror/source
fi

for i in 112x63  224x126 1248x702  624x351 1504x846 752x423; do
    cp -R $i mirror/.
done

pushd mirror/source
tar xf ../../*screenshots*.tar

popd

tar cvf mirror.tar mirror/