# 🧩 Odoo Missing Module Finder CLI

This script scans a custom Odoo addons directory and compares it to an exported `ir.module.module` CSV to find missing modules. It then outputs two CSV files: one for missing modules and one for found modules (sorted by author or any other field).

---

## 📦 Features

* Reads `Technical Name` from the exported CSV.
* Checks if corresponding folders exist in the addons path.
* Finds and exports missing modules to a new CSV.
* Exports found modules (along with directories) to a new CSV.
* Sorts output by any field (default: `Author`).
* Uses **color-coded logging** (INFO, WARNING, ERROR) without any third-party libs.
* Easy to use via command-line with arguments.
* **No total row** in the subdirectory breakdown.

---

## 🚀 Usage

```bash
python main.py \
  --addons /path/to/your/addons \
  --csv /path/to/ir.module.module.csv \
  --out-missing /path/to/output/missing_modules.csv \
  --out-found /path/to/output/found_modules.csv \
  --sort Author
```

### 🔧 CLI Arguments

| Argument        | Required | Description                                    |
| --------------- | -------- | ---------------------------------------------- |
| `--addons`      | ✅ Yes    | Path to your custom Odoo addons directory      |
| `--csv`         | ✅ Yes    | Path to the exported `ir.module.module.csv`    |
| `--out-missing` | ✅ Yes    | Output path for the missing modules CSV        |
| `--out-found`   | ✅ Yes    | Output path for the found modules CSV          |
| `--sort`        | No       | Field name to sort output by (default: Author) |

---

## 🖍️ Output

The script creates two CSV files:

* **missing\_modules.csv**: Lists modules **that are missing in your addons folder** based on what's listed in the exported CSV.
* **found\_modules.csv**: Lists modules **that are found** in the directories, along with the directories they were located in.

---

## 🎨 Logging (Color-Coded)

This script uses Python's built-in `logging` module with ANSI colors—**no extra install needed**.

* **INFO**: Process updates, paths, status (in Cyan)
* **WARNING**: No modules found, minor issues (in Yellow)
* **ERROR**: Critical problems like bad paths (in Red)

---

## 🔄 Logging Example

```bash
[INFO] Scanning directory: /path/to/your/addons
[WARNING] No missing modules found. All synced up, Bhai 💅
[ERROR] Addons path not found: /wrong/path
```

---

## 🧪 Example

```bash
python find_missing_modules.py \
  --addons /odoo/custom/14.0/odoo-addons \
  --csv ./ir.module.module.csv \
  --out-missing ./missing_modules.csv \
  --out-found ./found_modules.csv
```

This will export two CSVs:

* **missing\_modules.csv**: Modules listed in the CSV but not found in the addons directory.
* **found\_modules.csv**: Modules listed in the CSV and found in one or more directories.

---

## 🎨 What It Does

* Reads all folder names (modules) in your Odoo custom addons directory.
* Parses the exported module list from `ir.module.module.csv`.
* Finds modules listed in the CSV but **not present** in the folder.
* Sorts them by the column of your choice (default: `Author`).
* Exports the missing modules to a new CSV.
* Exports the found modules to a new CSV.
* Prints colorful logs and helpful suggestions. Yes, it’s dramatic.

---

## 📝 Notes

* The CSV **must** include a `Technical Name` column.
* Uses only Python’s standard library—no need to install anything.
* Terminal color output works best on Linux/macOS.

---

## 🛑 Troubleshooting

* **“Addons path not found”**
  → Check your path, maybe a typo? Make sure the folder exists.

* **“Exported CSV not found”**
  → Ensure the file is exported from Odoo properly and path is correct.

* **No missing modules found?**
  → You might be fully synced 💅 Or maybe check for typos in folder names.

---

## 💡 Tips

* Run `--help` to see all options:

  ```bash
  python find_missing_modules.py --help
  ```

* Missing everything? Double-check paths and CSV format.

---

## 💖 Author

You! And your fabulous CLI Bhai 🥂
