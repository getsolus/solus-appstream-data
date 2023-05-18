#!/bin/bash

rsync -avPHL --exclude '*.delta.eopkg' packages.getsol.us::soluspackages/unstable . --delete
