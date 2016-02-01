#!/bin/bash

RSYNC_PASSWORD=mirror rsync -avzHL mirror@packages.solus-project.com::packages/unstable .
