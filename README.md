## Initial documentation for regenerating appstream data (in-progress)

1. Install `appstream-glib`, `rsync`

2. Run `./clone.sh` to clone all packages from packages.getsol.us

3. Run `./mvem.sh` to remove unneccessary eopkgs for appstream-builder to chew through

4. Run `./do_stream.sh` to actually generate the appstream data

5. Run `./publish.sh` to copy the generated artefacts into the root directory

- Hint: Run `diff --stat` to get a general idea of the size differences
- Hint: Look through `solus-1-failed.xml.gz` to see if there any easily fixable failures

6. Run `./install.sh` to test out locally.

7. Upload `./work/output/mirror.tar` to `packages.getsol.us:/srv/www/screenshots/`, create a tar backup of the old screenshots and untar in place, make sure the folder permissions are 0755.

8. Load up software centre and check out some packages with metadata to confirm all is well

7. Git commit along with a new tag

8. Build `appstream-data` with the new tag and publish to the people.
