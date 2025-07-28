import json
from deep_translator import GoogleTranslator
from tqdm import tqdm

# ⚠️ Bu anahtarlar varsa çeviri yapılmaz
SKIP_KEYS = ['icon', 'image', 'logo', 'url', 'href', 'src', 'route', 'file', 'path', 'asset']

# 🔍 JSON içindeki tüm çevirilecek metinleri (string) listelemek için
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

# Anahtar adı bir atlanacak listeye giriyorsa true döndür
def is_skipped_key(key):
    return any(skip in key.lower() for skip in SKIP_KEYS)

# 🌍 Çeviri işlemi (filtreli)
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
            pbar.write(f"⚠️ Hata oluştu: {e} → {data[:30]}...")
            return data
    else:
        return data

# 📂 JSON dosyasını oku
with open("en.json", "r", encoding="utf-8") as f:
    en_data = json.load(f)

# 📊 Toplam çevrilecek metin sayısını göster
flat_items = flatten_json(en_data)
total_texts = len(flat_items)
print(f"Toplam çevrilecek metin sayısı: {total_texts}\n")

# 🌐 Çeviri başlatılıyor: İngilizce → İtalyanca
translator = GoogleTranslator(source="en", target="it")

with tqdm(total=total_texts, desc="İtalyanca çeviri") as pbar:
    translated_data = translate_json(en_data, translator, pbar)

# 💾 Çevrilen JSON'u kaydet
with open("it.json", "w", encoding="utf-8") as f:
    json.dump(translated_data, f, ensure_ascii=False, indent=2)

print("\n✅ Çeviri tamamlandı: it.json dosyası oluşturuldu.")
