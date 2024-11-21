## Old process - Regenerating appstream data on your local machine
> [!WARNING]
> This process should still be functional, but is much more tedious and time-consuming than the new playbook method. These directions are kept around for historical purposes only.

1. Install `appstream-glib`, `rsync`

2. Run `./clone.sh` to clone all packages from packages.getsol.us

3. Run `./mvem.sh` to remove unneccessary eopkgs for appstream-builder to chew through

4. Run `./do_stream.sh` to actually generate the appstream data

5. Run `./publish.sh` to copy the generated artefacts into the root directory of the git repository

- Hint: Run `diff --stat` to get a general idea of the size differences
- Hint: Look through `solus-1-failed.xml.gz` to see if there any easily fixable failures
- Hint: Add
    ```
    [diff "gz"]
        textconv = gzip -dc
        binary = true
    ```
  to your git config to diff the .gz files.

6. Run `./install.sh` to test out locally.

7. Upload `./work/output/mirror.tar` to `packages.getsol.us:/srv/www/screenshots/`, create a tar backup of the old screenshots and untar in place, make sure the folder permissions are 0755.
8. Load up software centre and check out some packages with metadata to confirm all is well

7. Git commit along with a new tag

8. Build `appstream-data` with the new tag and publish to the people.

## Old Process - regenerating from teaparty server directly
> [!WARNING]
> This process should still be functional, but is much more tedious and time-consuming than the new playbook method. These directions are kept around for historical purposes only.

If you have ssh access to the teaparty repo server (you have if you've done a sync), you can regenerate the appstream data directly from there without the need to clone the binary repo first.

1. SSH into teaparty and go to `/srv/appstream-data` which is a shared directory of this repository.

2. Run `./do_stream_teaparty.sh` to actually generate the appstream data. Try to choose a quiet time when the server isn't under much load.

3. Run `./publish.sh` to copy the generated artefacts into the root directory of the git repository.

4. Installing screenshots:
  - Ensure the recently generated `mirror.tar` archive looks correct `tar -tvf ./work/output/mirror.tar`, it should contain screenshots
  - Create a backup of the previous screenshots: `pushd /srv/www/screenshots/; sudo tar --create --file=mirror.tar.backup $(ls -d */) && popd`
  - Move the screenshots archive to screenshots: `sudo mv work/output/mirror.tar /srv/www/screenshots/`
  - Untar in place, ensure permissions are correct: `pushd /srv/www/screenshots; sudo tar -xvf mirror.tar --strip-components=1 && chmod 0755 $(ls -d */); popd`

5. Sync the artefacts to this repo locally:
  - `rsync -avPHL user@packages.getsol.us:/srv/appstream-data/*.gz .`
  - `rsync -avPHL user@packages.getsol.us:/srv/appstream-data/*.tar .`

6. Run `./install.sh` to try out and load up the software centre and check out some packages with metadata to confirm all is well

7. Git commit along with a new tag

8. Build `appstream-data` with the new tag and publish to the people.

TODO:
  - Make appstream-builder ignore -devel and -dbginfo packages