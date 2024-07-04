#!/usr/bin/env bash
set -e
set -x

# Create backup of old screenshots
pushd /srv/www/screenshots/
    sudo tar --create --file=mirror.tar.backup $(ls -d */)
popd

sudo mv work/output/mirror.tar /srv/www/screenshots/

pushd /srv/www/screenshots
    # untar in place
    sudo tar -xvf mirror.tar --strip-components=1
    # Ensure directory permissions are correct
    chmod 0755 $(ls -d */)
popd
