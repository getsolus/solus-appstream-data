#!/bin/bash

RSYNC_PASSWORD=mirror rsync -avzHL --exclude '*.delta.eopkg' mirror@packages.solus-project.com::packages/unstable .
