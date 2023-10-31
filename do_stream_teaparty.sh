#!/bin/bash
set -e
set -x

if ! command -v appstream-builder > /dev/null
	then
	echo "appstream-glib not found"
fi

if [[ ! -d "work" ]]; then
    mkdir work
fi

pushd work

for dname in output cache logs icons ; do
    if [[ ! -d "${dname}" ]]; then
        mkdir "${dname}" -v
    fi
done

appstream-builder --packages-dir=/srv/solus/packages/unstable --output-dir=./output \
                  --cache-dir=./cache --log-dir=./logs -v \
                  --include-failed --basename=solus-1 --origin=solus \
                  --veto-ignore=missing-parents

appstream-util mirror-screenshots \
    output/solus-1.xml.gz https://screenshots.getsol.us/ \
    ./cache ./output
