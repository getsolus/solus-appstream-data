#!/usr/bin/env python3
import argparse
import gzip
import pathlib
from xml.etree import ElementTree


def main():
    parser = argparse.ArgumentParser(
        prog="check_packages_exist",
        description="Check to make sure all packages listed in appstream metainfo actually exist in the eopkg index",
    )
    parser.add_argument(
        "appstream_metainfo",
        action="store",
        help="Path to the appstream metainfo file to be checked. This must be a gzipped XML file.",
        type=pathlib.Path,
    )
    parser.add_argument(
        "eopkg_index",
        action="store",
        help="Path to the eopkg index file to be validated against. This must be an uncompressed XML file.",
        type=pathlib.Path,
    )
    args = parser.parse_args()
    appstream_components = get_components_from_appstream(args.appstream_metainfo)
    eopkg_packages = get_packages_from_solus_index(args.eopkg_index)
    failed_packages = get_failed_packages(appstream_components, eopkg_packages)
    if failed_packages:
        print(
            "The following packages were present in the provided appstream metainfo file, but not in the eopkg index."
            " They should be manually deleted from the repository files, and appstream metainfo regenerated."
        )
        for package in failed_packages:
            print(package)
        exit(1)
    else:
        print(
            "Success! No nonexistent packages were present in the provided appstream metainfo file."
        )
        exit(0)


def __init__():
    pass


def get_components_from_appstream(xml_path: pathlib.Path) -> iter:
    """
    Retrieves a list of components from an AppStream Data XML file. "component" is Appstream language for "Package".
    :param xml_path: Path to an XML AppStream Data File.
    :return: An iterable of all components listed in the provided metadata.
    """
    appstream_xml = gzip.open(xml_path, "r")
    tree = ElementTree.parse(appstream_xml)
    root = tree.getroot()
    components = [
        component.find("pkgname").text for component in root.findall("component")
    ]
    return components


def get_packages_from_solus_index(xml_path: pathlib.Path) -> iter:
    """
    Retrieves a list of packages from an eopkg index XML file.
    :param xml_path: Path to an eopkg index XML file.
    :return: An iterable of all packages listed in the provided eopkg index.
    """
    solus_xml = open(xml_path, "r")
    tree = ElementTree.parse(solus_xml)
    root = tree.getroot()
    packages = [package.find("Name").text for package in root.findall("Package")]
    return packages


def get_failed_packages(appstream_packages: iter, eopkg_packages: iter) -> iter:
    """
    Returns a list of packages which exist in appstream metadata and do *not* exist in the eopkg index.
    :param appstream_packages: Iterable of all packages listed in appstream metadata.
    :param eopkg_packages: Iterable of all packages listed in eopkg index.
    :return: Iterable of packages which were erroneously added to appstream metadata.
    """
    failed_packages = [
        package for package in appstream_packages if package not in eopkg_packages
    ]
    return failed_packages


if __name__ == "__main__":
    main()
