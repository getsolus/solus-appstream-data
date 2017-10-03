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
                  --cache-dir=./cache --max-threads=8  \
                  --log-dir=./logs --enable-hidpi -v \
                  --include-failed --add-cache-id --basename=solus-1 --origin=solus


appstream-util mirror-screenshots \
    output/solus-1.xml.gz https://packages.solus-project.com/screenshots \
    ./cache ./output
