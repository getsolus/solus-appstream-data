# Solus Appstream Generation

## Regenerating appstream data

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

## Regenerating from teaparty server directly

If you have ssh access to the teaparty repo server (you have if you've done a sync), you can regenerate the appstream data directly from there without the need to clone the binary repo first.

1. SSH into teaparty and go to `/srv/appstream-data` which is a shared directory of this repository.

2. Run `./do_stream_teaparty.sh` to actually generate the appstream data. Try to choose a quiet time when the server isn't under much load.

3. Run `./publish.sh` to copy the generated artefacts into the root directory of the git repository.

4. Installing screenshots:
  - Ensure the recently generated `mirror.tar` archive looks correct `tar -tvf ./work/output/mirror.tar`, it should contain screenshots
  - Run `./install_screenshots_teaparty.sh`. You will need administrator access

5. Sync the artefacts to this repo locally:
  - `rsync -avPHL user@packages.getsol.us:/srv/appstream-data/*.gz .`
  - `rsync -avPHL user@packages.getsol.us:/srv/appstream-data/*.tar .`

6. Run `./install.sh` to try out and load up the software centre and check out some packages with metadata to confirm all is well

7. Git commit along with a new tag

8. Build `appstream-data` with the new tag and publish to the people.

TODO:
  - Make appstream-builder ignore -devel and -dbginfo packages

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

  Appstream generation generally also fails when the xml file specifies a icon, see: https://github.com/hughsie/appstream-glib/issues/243#issuecomment-397224098

    `<icon type="remote" width="128" height="128">https://raw.githubusercontent.com/tkashkin/GameHub/e380a848b89498904e96e73fa72a07aa823151ce/data/icon/128.svg?</icon>`

    Simply, removing the icon tag from the xml file and ensuring the desktop id matches the desktop filename on disk will generally fix the generation.

  Appstream generation can also fail if the icon is symlinked from another path to one of the icon paths appstream-builder is expecting.

    appstream-builder expects icons in the following paths: /usr/share/pixmaps/*, /usr/share/icons/*, /usr/share/icons/hicolor/*/apps/*, or /usr/share/${app_name}/icons/*.

    If an icon is symlinked to one of those paths from another directory, appstream-builder will fail to find the icon. Install the icon to one of the expected paths directly

    E.g. `ln -s %libdir%/thunderbird/chrome/icons/default/default256.png $installdir/usr/share/pixmaps/thunderbird.png` <- appstream-builder will fail to find the icon

- There may be other veto reasons of course, it's your job to look through the appstream xml file as well as desktop file to try and determine them.

### Testing Individual Packages

- Clone the package repo

- Build it or eopkg fetch pkgname

- Run `sudo eopkg it appstream-glib`, `appstream-builder --packages-dir=. --include-failed -v`

- Look in the `example-failed.xml.gz` file to see if the appstream generation failed

- Look in the `example.xml.gz` file to see if the appstream generation succeeded.

- Install the package and run `appstream-util validate /usr/share/metainfo/pkgname.xml`
