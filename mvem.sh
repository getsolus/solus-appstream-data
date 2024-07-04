#!/usr/bin/env bash

if [[ ! -d "clones" ]]; then
    mkdir "clones"
fi

find . -name "*.delta.eopkg"|xargs rm -v

find unstable -name "*.eopkg" | grep -v "*.delta" | grep -v "\-dbginfo"|xargs -I{} ln -v {} clones/.
