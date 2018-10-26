#!/bin/bash

RSYNC_PASSWORD=mirror rsync -avzHL --exclude '*.delta.eopkg' mirrors.rit.edu::solus/packages/unstable . --delete
