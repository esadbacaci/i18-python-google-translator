import json
from deep_translator import GoogleTranslator
from tqdm import tqdm

# ⚠️ If these keywords are found in a key, the value will not be translated
SKIP_KEYS = ['icon', 'image', 'logo', 'url', 'href', 'src', 'route', 'file', 'path', 'asset']

# 🔍 Flatten the JSON and list all translatable strings with their paths
def flatten_json(data, path=''):
    items = []
    if isinstance(data, dict):
        for k, v in data.items():
            new_path = f"{path}.{k}" if path else k
            items.extend(flatten_json(v, new_path))
    elif isinstance(data, list):
        for i, v in enumerate(data):
            new_path = f"{path}[{i}]"
            items.extend(flatten_json(v, new_path))
    elif isinstance(data, str):
        items.append((path, data))
    return items

# Returns True if the key should be skipped (based on SKIP_KEYS)
def is_skipped_key(key):
    return any(skip in key.lower() for skip in SKIP_KEYS)

# 🌍 Perform filtered translation of the JSON content
def translate_json(data, translator, pbar, parent_key=''):
    if isinstance(data, dict):
        return {
            k: translate_json(v, translator, pbar, parent_key=k) if not is_skipped_key(k) else v
            for k, v in data.items()
        }
    elif isinstance(data, list):
        return [translate_json(item, translator, pbar, parent_key=parent_key) for item in data]
    elif isinstance(data, str):
        if is_skipped_key(parent_key):
            return data
        try:
            translated = translator.translate(text=data)
            pbar.update(1)
            return translated
        except Exception as e:
            pbar.write(f"⚠️ Error occurred: {e} → {data[:30]}...")
            return data
    else:
        return data

# 📂 Load the source JSON file (English)
with open("en.json", "r", encoding="utf-8") as f:
    en_data = json.load(f)

# 📊 Show the total number of strings to be translated
flat_items = flatten_json(en_data)
total_texts = len(flat_items)
print(f"Total number of strings to translate: {total_texts}\n")

# 🌐 Start translation: English → Italian
translator = GoogleTranslator(source="en", target="it")

with tqdm(total=total_texts, desc="Translating to Italian") as pbar:
    translated_data = translate_json(en_data, translator, pbar)

# 💾 Save the translated JSON to file
with open("it.json", "w", encoding="utf-8") as f:
    json.dump(translated_data, f, ensure_ascii=False, indent=2)

print("\n✅ Translation completed: 'it.json' file has been created.")
