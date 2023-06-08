# Solus Appstream Generation

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

## Debugging Failures

### Understanding Failures

- Load up the `solus-1-failed.xml.gz` file and look through it for `<Veto>` reasons

- The most common failure is "Has No Icon". Generally this is due to the appstream xml file's desktop tag not matching the filename the .desktop file is installed under

  For example, the appstream xml file contains:

    `<launchable type="desktop-id">com.github.Flacon.desktop</launchable>`

    But the .desktop file is installed to

    `<Path fileType="data">/usr/share/applications/flacon.desktop</Path>`

    To fix this, the .desktop must simply be installed to `/usr/share/applications/com.github.Flacon.desktop`

  Another similar example using the legacy format:

    `<id type="desktop">com.abisource.AbiWord</id>`

    But the .desktop file is installed to

    `<Path fileType="data">/usr/share/applications/abiword.desktop</Path>`

    Once again, the .desktop must simply be installed to `/usr/share/applications/com.abisource.AbiWord.desktop`

- There may be other veto reasons of course, it's your job to look through the appstream xml file as well as desktop file to try and determine them.

### Testing Individual Packages

- Clone the package repo

- Build it or eopkg fetch pkgname

- Run `sudo eopkg it appstream-glib`, `appstream-builder --packages-dir=. --include-failed -v`

- Look in the `example-1-failed.xml.gz` file to see if the appstream generation failed

- Look in the `example-1.xml.gz` file to see if the appstream generation succeeded.

- Install the package and run `appstream-util validate /usr/share/metainfo/pkgname.xml`
