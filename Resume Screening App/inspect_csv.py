import csv
with open("data/Resume.csv", newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    print("Header:", header)
    categories = set()
    cat_idx = header.index("Category") if "Category" in header else 0 # guess
    for row in reader:
        if row:
            categories.add(row[cat_idx])
    print("Categories:", sorted(list(categories)))
