#!/bin/bash
set -e
set -x

if [[ ! -d "work" ]]; then
    mkdir work
fi

pushd work

for dname in output cache logs icons ; do
    if [[ ! -d "${dname}" ]]; then
        mkdir "${dname}" -v
    fi
done

appstream-builder --packages-dir=../clones --output-dir=./output \
                  --cache-dir=./cache --max-threads=4  \
                  --log-dir=./logs --enable-hidpi -v --api-version=0.8 \
                  --include-failed --add-cache-id --basename=solus-1 --origin=solus


appstream-util mirror-screenshots \
    output/solus-1.xml.gz https://archive.solus-project.com/screenshots \
    ./cache ./output
