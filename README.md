# Solus Appstream Generation

## Usage
### Initial Setup
These directions will guide you through configuring your system to generate appstream data. You should only need to do this once.
> [!NOTE]
> This assumes you have already completed the [Prepare for Packaging](https://help.getsol.us/docs/packaging/prepare-for-packaging) steps listed in the help center. You will need a fully-configured git setup for this tooling to work.
> Additionally, your GitHub account must have push access to this repository (should be true for all staff).
1. Ensure that your local clone of this repository is set up to be able to push (Cloning via GitHub CLI recommended).
2. Ensure that your account on `teaparty` has sudo access.
3. Ensure that your SSH configuration specifies the correct username for connecting to `packages.getsol.us`. [This issue](https://github.com/getsolus/solus-team-docs/issues/60) in our team docs repo is where we are discussing how to document this for our infrastructure.
3. Ensure you have `go-task` installed. All interaction with this tooling should be possible through the `Taskfile.yml` in this repository.
4. Run `go-task appstream-init`. This task will install `pyyaml` and `ansible` on your system, and then install the necessary ansible collection.
### Generating Appstream Data
This is the actual process of generating appstream metadata from our repository, which should ideally be done each week (after deprecations, but before sync). Make sure you've correctly completed all the Initial Setup steps first. 
1. Run `go-task full-process` from this directory. 
2. When asked for your "BECOME password", enter your user's password on teaparty. 
3. After you enter your password, the playbook will automatically:
    - Generate appstream data,
    - Check it against the eopkg index,
    - Download new metadata to your local clone of the repo,
    - Commit the changes,
    - Add a new tag to the repository,
    - _and push the changes to github._ - Work in progress  
      Due to a [bug](https://github.com/getsolus/solus-appstream-data/issues/6), you will need to push the tags yourself with  
      `git push --tags`
> [!NOTE]
> This would be a good time to take a break and do something else. Just make sure your computer doesn't go to sleep. It takes a while (about 30 minutes).
5. Go to your clone of the packages monorepo and update the `appstream-data` package to use the newly-tagged version of this repository.  
You will need the tag from the output (just the number without the leading v).  
Also note the tarball URL, for example, https://github.com/getsolus/solus-appstream-data/archive/refs/tags/v60.tar.gz

```bash
gotopkg appstream-data
go-task update -- <tag> <url to tarball from GitHub>
go-task
```

_Example update command:_

```bash
go-task update -- 60 https://github.com/getsolus/solus-appstream-data/archive/refs/tags/v60.tar.gz
```

Follow standard packaging procedure to get those changes into the repository.

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
