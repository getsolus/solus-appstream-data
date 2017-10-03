#!/bin/bash

RSYNC_PASSWORD=mirror rsync -avzHL --exclude '*.delta.eopkg' mirror@archive.solus-project.com::packages/unstable . --delete
