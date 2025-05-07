import os
import csv
import argparse
import logging
from collections import defaultdict

# ANSI color codes
RESET = '\033[0m'
COLORS = {
    'DEBUG': '\033[90m',
    'INFO': '\033[36m',
    'WARNING': '\033[33m',
    'ERROR': '\033[31m',
    'CRITICAL': '\033[41m',
}

class ColorFormatter(logging.Formatter):
    def format(self, record):
        color = COLORS.get(record.levelname, '')
        record.msg = f"{color}{record.msg}{RESET}"
        return super().format(record)

# Configure logger
logger = logging.getLogger("module_finder")
handler = logging.StreamHandler()
handler.setFormatter(ColorFormatter("[%(levelname)s] %(message)s"))
logger.addHandler(handler)
logger.setLevel(logging.INFO)

def validate_paths(root_path, csv_path):
    if not os.path.exists(root_path):
        logger.error(f"Root addons path not found: {root_path}")
        logger.warning("Check if the path is correct or if the folder exists!")
        raise FileNotFoundError(root_path)

    if not os.path.isfile(csv_path):
        logger.error(f"Exported CSV not found: {csv_path}")
        logger.warning("Ensure that your CSV file is properly exported and the path is correct!")
        raise FileNotFoundError(csv_path)

def get_directory_names(root_path, per_dir_counts):
    all_module_dirs = defaultdict(list)
    for sub in os.listdir(root_path):
        sub_path = os.path.join(root_path, sub)
        if os.path.isdir(sub_path):
            logger.info(f"Scanning subdirectory: {sub_path}")
            for item in os.listdir(sub_path):
                item_path = os.path.join(sub_path, item)
                if os.path.isdir(item_path):
                    all_module_dirs[item].append(sub)
                    per_dir_counts[sub] = per_dir_counts.get(sub, 0) + 1
    return all_module_dirs

def read_csv(filepath):
    with open(filepath, newline='') as csvfile:
        return list(csv.DictReader(csvfile))

def write_missing_modules(filepath, missing_modules):
    if missing_modules:
        fieldnames = missing_modules[0].keys()  # Dynamically get fieldnames
        with open(filepath, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(missing_modules)

def write_found_modules(filepath, found_modules):
    fieldnames = ['Technical Name', 'Repositories']
    with open(filepath, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for technical_name, repositories in found_modules.items():
            writer.writerow({
                'Technical Name': technical_name,
                'Repositories': ' '.join(repositories)
            })

def print_summary(exported_modules, missing_modules, per_dir_counts):
    total_searched = len(exported_modules)
    total_found = total_searched - len(missing_modules)
    total_missing = len(missing_modules)

    print('\n')
    logger.info("Overview Summary:")
    logger.info("+---------------------------+--------+")
    logger.info("| Metric                     | Count |")
    logger.info("+---------------------------+--------+")
    logger.info(f"| Modules found (installed)  | {total_found: <5} |")
    logger.info(f"| Missing modules            | {total_missing: <5} |")
    logger.info("+---------------------------+--------+")
    logger.info(f"| TOTAL                      | {total_searched: <5} |")
    logger.info("+---------------------------+--------+")

    if per_dir_counts:
        print('\n')
        logger.info("Breakdown by Subdirectory:")
        logger.info("+---------------------------+--------+")
        logger.info("| Subdirectory              | Modules|")
        logger.info("+---------------------------+--------+")
        for sub, count in per_dir_counts.items():
            logger.info(f"| {sub: <25} | {count: <6} |")
        logger.info("+---------------------------+--------+")

def main(root_path, csv_path, output_missing_path, output_found_path, sort_by):
    per_dir_counts = {}
    validate_paths(root_path, csv_path)

    logger.info(f"Scanning directory: {root_path}")
    module_locations = get_directory_names(root_path, per_dir_counts)

    logger.info(f"Reading exported modules: {csv_path}")
    exported_modules = read_csv(csv_path)

    missing = [
        row for row in exported_modules
        if row.get('Technical Name') and row['Technical Name'] not in module_locations
    ]

    found_modules = {
        module['Technical Name']: [] for module in exported_modules if module['Technical Name'] not in [m['Technical Name'] for m in missing]
    }

    for module_name in found_modules.keys():
        if module_name in module_locations:
            found_modules[module_name] = module_locations[module_name]

    # Write missing modules to CSV
    if missing:
        logger.info(f"Writing missing modules to: {output_missing_path}")
        write_missing_modules(output_missing_path, missing)
        logger.info("Done! Missing modules exported.")
    else:
        logger.warning("No missing modules found. All synced up, Bhai 💅")

    # Write found modules to CSV
    logger.info(f"Writing found modules to: {output_found_path}")
    write_found_modules(output_found_path, found_modules)
    logger.info("Done! Found modules exported.")

    print_summary(exported_modules, missing, per_dir_counts)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find and export missing Odoo modules based on CSV list.')
    parser.add_argument('--addons', required=True, help='Path to the root directory containing multiple addon dirs (e.g. 14.0)')
    parser.add_argument('--csv', required=True, help='Path to the exported ir.module.module CSV')
    parser.add_argument('--out-missing', required=True, help='Path to save the missing modules CSV')
    parser.add_argument('--out-found', required=True, help='Path to save the found modules CSV')
    parser.add_argument('--sort', default='Author', help='Column to sort the output CSV by (default: Author)')

    args = parser.parse_args()

    main(
        root_path=args.addons,
        csv_path=args.csv,
        output_missing_path=args.out_missing,
        output_found_path=args.out_found,
        sort_by=args.sort
    )
