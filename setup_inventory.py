import yaml
import argparse
import pathlib

def main():
    parser = argparse.ArgumentParser(
        prog='setup_inventory',
        description='Set up the Ansible inventory for Solus appstream data generation'
    )
    parser.add_argument(
        "inventory_file",
        action="store",
        help="Path to the desired location of the inventory file",
        type=pathlib.Path,
    )
    args = parser.parse_args()
    username = input("Your username on teaparty (must have sudo access): ")
    print(f'Writing Ansible inventory to {args.inventory_file}')
    inventory = {'teaparty': {'hosts': {'packages.getsol.us': {'ansible_user': username}}}}

    with open(args.inventory_file, 'w') as f:
        yaml.safe_dump(inventory, f)

if __name__ == '__main__':
    main()
