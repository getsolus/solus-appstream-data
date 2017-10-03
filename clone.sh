#!/bin/bash

RSYNC_PASSWORD=mirror rsync -avzHL --exclude '*.delta.eopkg' mirror.math.princeton.edu::pub/solus-packages/unstable . --delete
