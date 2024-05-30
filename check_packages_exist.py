import gzip
import sys
import subprocess
from xml.etree import ElementTree

if len(sys.argv) > 1:
    xml_path = sys.argv[1]
else:
    xml_path = "solus-1.xml.gz"

appstream_xml = gzip.open(xml_path, "r")
tree = ElementTree.parse(appstream_xml)
root = tree.getroot()
components = root.findall("component")

failed_packages = []

print(f'Checking all packages in {xml_path}...')
for component in components:
    package_name = component.find("pkgname").text
    output = subprocess.run(["pkcon", "resolve", package_name], capture_output=True)
    if output.returncode != 0:
        failed_packages.append(package_name)

print('The following packages failed to resolve, and should likely be removed:')
for package_name in failed_packages:
    print(package_name)
