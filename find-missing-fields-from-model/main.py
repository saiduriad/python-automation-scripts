import csv
import argparse
import logging
import sys

# ANSI color codes
COLOR_RESET = "\033[0m"
COLOR_CYAN = "\033[96m"
COLOR_YELLOW = "\033[93m"
COLOR_RED = "\033[91m"
COLOR_GREEN = "\033[92m"

# Setup color-coded logging
def setup_logging():
    class ColorFormatter(logging.Formatter):
        def format(self, record):
            level_color = {
                'INFO': COLOR_CYAN,
                'WARNING': COLOR_YELLOW,
                'ERROR': COLOR_RED
            }.get(record.levelname, COLOR_RESET)
            message = super().format(record)
            return f"{level_color}[{record.levelname}]{COLOR_RESET} {message.split('] ', 1)[-1]}"
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(ColorFormatter("[%(levelname)s] %(message)s"))

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.handlers = [handler]
    return logger

# Function to read a CSV file into a list of dictionaries
def read_csv(file_path):
    logger.info(f'Reading CSV file: {file_path}')
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = list(reader)
        logger.info(f'Loaded {len(data)} rows from {file_path}')
        return data

# Function to find missing fields
def find_missing_fields(source_csv, destination_csv):
    logger.info('Extracting destination field names...')
    destination_field_names = {row['Field Name'].strip() for row in destination_csv if row.get('Model')}
    logger.info(f'Total destination fields with model: {len(destination_field_names)}')

    logger.info('Finding missing fields from source...')
    missing_fields = []
    for row in source_csv:
        field_name = row['Field Name'].strip()
        model = row['Model'].strip() if 'Model' in row else ''
        if not field_name or not model:
            continue
        if field_name not in destination_field_names:
            missing_fields.append(row)

    logger.info(f'Total missing fields identified: {len(missing_fields)}')
    return missing_fields, len(destination_field_names)

# Function to write the missing fields to a new CSV file
def write_csv(file_path, missing_fields, fieldnames):
    logger.info(f'Writing missing fields to CSV: {file_path}')
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(missing_fields)
    logger.info(f'CSV writing complete: {file_path}')

# Main function to execute the comparison and writing to CSV
def main():
    parser = argparse.ArgumentParser(description='Compare source and destination CSVs and find missing fields.')
    parser.add_argument('--source', required=True, help='Path to the source CSV file')
    parser.add_argument('--destination', required=True, help='Path to the destination CSV file')
    parser.add_argument('--out', required=True, help='Path to the output CSV file for missing fields')
    parser.add_argument('--sort', default='Field Name', help='Field name to sort output by')

    args = parser.parse_args()
    global logger
    logger = setup_logging()

    try:
        source_csv = read_csv(args.source)
        destination_csv = read_csv(args.destination)
    except FileNotFoundError as e:
        logger.error(f'Error: {e}')
        return

    if not source_csv or not destination_csv:
        logger.error('One or both files are empty.')
        return

    missing_fields, destination_field_count = find_missing_fields(source_csv, destination_csv)

    # Sort if the field exists
    if args.sort and args.sort in source_csv[0]:
        logger.info(f'Sorting missing fields by: {args.sort}')
        missing_fields = sorted(missing_fields, key=lambda x: x.get(args.sort, '').lower())

    if not missing_fields:
        logger.warning('No missing fields found. All fields in source are in destination.')
        return

    fieldnames = source_csv[0].keys()
    write_csv(args.out, missing_fields, fieldnames)

    source_count = len([r for r in source_csv if r.get("Model")])
    missing_count = len(missing_fields)

    logger.info(f'{COLOR_GREEN}🎉 Output written to: {args.out}{COLOR_RESET}')
    logger.info(f'{COLOR_CYAN}📊 Overview:{COLOR_RESET}')
    
    table = f"""
+------------------------+----------------+
|        Metric          |     Count      |
+------------------------+----------------+
| Source total fields    | {str(source_count).rjust(14)} |
| Destination fields     | {str(destination_field_count).rjust(14)} |
| Missing fields found   | {str(missing_count).rjust(14)} |
+------------------------+----------------+
""".strip("\n")

    print(COLOR_CYAN + table + COLOR_RESET)

if __name__ == '__main__':
    main()
