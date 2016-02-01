#!/bin/bash

if [[ ! -d "clones" ]]; then
    mkdir "clones"
fi

find unstable -name "*.eopkg" | grep -v "*.delta" | grep -v "\-dbginfo"|xargs -I{} ln -v {} clones/.
