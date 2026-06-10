import json

def mask_email(email):
    if "@" not in email:
        return email
    parts = email.split('@')
    return parts[0][0] + "***@" + parts[1]


def clean_data(input_file, output_file):
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: {input_file} not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from {input_file}.")
        return

    seen_ids = set()
    sanitized_data = []

    for item in data:

        # --- 1. DEDUP ---
        item_id = item.get("id")
        if item_id in seen_ids:
            continue

        # --- 2 & 3. PRICE CHECK ---
        price = item.get("price", 0)

        # skip nếu price không hợp lệ
        if not isinstance(price, (int, float)):
            continue

        if price > 5000:
            continue

        if price < 0:
            continue

        # --- 4. PII MASKING ---
        if "name" in item:
            del item["name"]

        if "email" in item:
            item["email"] = mask_email(item["email"])

        # lưu id đã thấy
        seen_ids.add(item_id)

        sanitized_data.append(item)

    # Save file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(sanitized_data, f, indent=4, ensure_ascii=False)

    print(f"Successfully sanitized data. Output saved to {output_file}")
    print(f"Original records: {len(data)}")
    print(f"Sanitized records: {len(sanitized_data)}")


if __name__ == "__main__":
    INPUT_PATH = "toxic_sample.json"
    OUTPUT_PATH = "sanitized_sample.json"
    clean_data(INPUT_PATH, OUTPUT_PATH)