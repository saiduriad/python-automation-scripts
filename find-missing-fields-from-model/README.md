# 🧾 Odoo Field Comparison CLI

This CLI tool compares two CSV files—typically exported from Odoo—and tells you **which fields from the source are missing in the destination**. It logs every step (with colors, duh), sorts, and exports the missing fields to a new file. Slay your audits and data validations effortlessly 💅

---

## ⚙️ Features

* Compares `Field Name` + `Model` from the **source** CSV against the **destination** CSV.
* Identifies **missing fields** and exports them to a CSV.
* Also shows total fields from source and destination.
* Outputs a cute summary table with counts.
* **Sorts** the missing data by any column (default: `Field Name`).
* Color-coded logs (Cyan for INFO, Yellow for WARNING, Red for ERROR).
* Uses pure Python—**no extra packages**. Works out of the box.

---

## 🚀 Usage

```bash
python main.py \
  --source /path/to/source.csv \
  --destination /path/to/destination.csv \
  --out /path/to/missing_fields.csv \
  --sort Field\ Name
```

---

## 🛠️ CLI Arguments

| Argument        | Required | Description                                              |
| --------------- | -------- | -------------------------------------------------------- |
| `--source`      | ✅ Yes    | Path to source CSV file (contains all expected fields)   |
| `--destination` | ✅ Yes    | Path to destination CSV (contains existing fields)       |
| `--out`         | ✅ Yes    | Output path for the missing fields CSV                   |
| `--sort`        | No       | Column to sort missing fields by (default: `Field Name`) |

---

## 🖍️ Output

One lovely CSV gets created:

* **missing\_fields.csv**: Fields from the source that aren’t found in the destination (based on `Field Name` + `Model` combo).

Also shows a pretty stats table like:

```text
+------------------------+----------------+
|        Metric          |     Count      |
+------------------------+----------------+
| Source total fields    |            147 |
| Destination fields     |            125 |
| Missing fields found   |             22 |
+------------------------+----------------+
```

---

## ✨ Logging (with Colors)

No boring logs here. Every move is announced in style:

* **INFO** – What's happening rn (Cyan)
* **WARNING** – Chill issues, like “no missing fields” (Yellow)
* **ERROR** – Uh-ohs like bad paths (Red)

### 🧵 Example

```bash
[INFO] Reading CSV file: ./source.csv
[INFO] Loaded 150 rows from ./source.csv
[INFO] Extracting destination field names...
[INFO] Total destination fields with model: 123
[INFO] Total missing fields identified: 27
[INFO] Writing missing fields to CSV: ./missing_fields.csv
🎉 Output written to: ./missing_fields.csv
📊 Overview:
+------------------------+----------------+
| Source total fields    |            150 |
| Destination fields     |            123 |
| Missing fields found   |             27 |
+------------------------+----------------+
```

---

## 📎 Notes

* Both CSVs must contain `Field Name` and `Model` columns.
* Fields without a `Model` are ignored.
* Handles weird spaces or missing fields like a pro (thanks to `.strip()`).
* All logs are stdout-friendly and color-enhanced.

---

## 🛑 Troubleshooting

* **File not found?**
  → Check that the path is correct and file exists.

* **Empty file warning?**
  → Ensure both CSVs have data. Blank files won't work.

* **No missing fields?**
  → You're either perfect or comparing wrong files 😘

---

## 💡 Tips

* Use `--sort` to organize the missing fields however you like.
* Want to turn it into a GUI? Sis, go off—but this CLI’s already fabulous.
* Wrap it into your deployment or data QA pipelines to stay flawless.

---

## 💖 Author

Still you, with your iconic CLI Bhai backing you up 👑
