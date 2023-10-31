#!/bin/bash
set -e
set -x

appstream-util status-html \
    ./solus-1.xml.gz   \
    ./solus.html
appstream-util status-html  \
    ./solus-1-failed.xml.gz \
    ./solus-failed.html
appstream-util matrix-html \
    ./solus-1.xml.gz   \
    ./solus-1-failed.xml.gz \
    ./solus-matrix.html
