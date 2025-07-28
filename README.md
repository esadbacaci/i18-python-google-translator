This Python script is designed to automatically translate JSON localization files from English into another language — in this case, Italian — using the Google Translate API via the deep_translator library. It's especially useful for internationalized web or mobile applications where translation files are structured in nested JSON formats.

🚀 Features
📁 Automatically scans and translates all translatable string values in a JSON file.

⚠️ Skips non-translatable keys like URLs, icons, file paths, routes, etc. (e.g., icon, image, url, src, file, etc.).

🔄 Fully recursive: handles deeply nested JSON structures.

📊 Displays a progress bar using tqdm during translation for better user feedback.

✅ Gracefully handles errors and prints warnings without breaking the process.

🧠 Purpose
This tool is ideal for projects that support multiple languages. Instead of manually translating each field, you can generate a full translated version of your existing JSON in seconds. It's especially helpful for developers maintaining internationalized UI/UX with large translation files.

🔧 How to Use
Place your source translation file in the root directory and name it en.json.

Run the script using Python:


pip install deep-translator tqdm
python translate_json.py
The translated file will be saved as it.json in the same directory.

📌 Notes
Only values of type string will be translated.

Keys containing terms like url, src, icon, etc. are automatically excluded from translation.

Be aware of Google Translate’s usage limits. For large files, rate limits or timeouts may occur.

🧩 Requirements
Python 3.6+

deep-translator

tqdm

🗺️ Future Improvements
Support for dynamic language selection via CLI arguments.

Logging of translation errors into a separate file.

Batch translation into multiple languages at once.
