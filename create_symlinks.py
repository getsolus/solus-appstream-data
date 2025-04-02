# Create a directory of symlinks to optimize and correct the appstream build

import pathlib
import argparse
import os
from xml.etree import ElementTree


def main():
    parser = argparse.ArgumentParser(
        prog='create_symlinks',
        description='Create symbolic links to eopkg files to optimize and correct our appstream build'
    )
    parser.add_argument(
        "eopkg_index",
        action="store",
        help="Path to the eopkg index file to be validated against. This must be an uncompressed XML file.",
        type=pathlib.Path,
    )
    parser.add_argument(
        "packages_directory",
        action="store",
        help="Path to the packages (input) directory.",
        type=pathlib.Path,
    )
    parser.add_argument(
        "symlinks_directory",
        action="store",
        help="Path to the symlinks (output) directory.",
        type=pathlib.Path,
    )
    args = parser.parse_args()
    eopkg_packages = get_packages_from_eopkg_index(args.eopkg_index)
    symlinks_created = 0
    for package_file in args.packages_directory.glob('**/*.eopkg'):
        if check_file(package_file, eopkg_packages):
            # Create a symlink for this package, we like it
            os.symlink(package_file, pathlib.Path.joinpath(args.symlinks_directory, pathlib.Path(package_file.name)))
            symlinks_created += 1
    print(f'Created {symlinks_created} symlinks.')


def get_packages_from_eopkg_index(xml_path: pathlib.Path) -> dict:
    solus_xml = open(xml_path, 'r')
    tree = ElementTree.parse(solus_xml)
    root = tree.getroot()
    packages = {
        package.find("Name").text: package.find("History").findall("Update")[0].attrib['release']
        for package in root.findall("Package")
    }
    return packages


def parse_package_filename(package_filename: str) -> dict:
    package_split = package_filename.rsplit('-', 4)
    output = {
        'name': package_split[0],
        'release': package_split[2],
        'dbginfo': package_split[0].endswith('-dbginfo'),
        'devel':  package_split[0].endswith('-devel'),
    }
    return output


def check_file(path: pathlib.Path, eopkg_packages: dict) -> bool:
    eopkg_info = parse_package_filename(path.name)
    if (eopkg_info['name'] in eopkg_packages.keys() and eopkg_info['release'] == eopkg_packages[eopkg_info['name']])\
        and not eopkg_info['dbginfo']\
        and not eopkg_info['devel']\
        :
        return True
    else:
        return False


if __name__ == '__main__':
    main()