#!/usr/bin/env bash

if ! command -v rsync > /dev/null
	then
	echo "rsync not found. Installing now."
	sudo eopkg install rsync -y
fi

rsync -avPHL --exclude '*.delta.eopkg' --exclude '*-dbginfo-*.eopkg' packages.getsol.us::soluspackages/unstable . --delete
