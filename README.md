# 📝 Keep to Notes Converter

> 🔄 Seamlessly convert your Google Keep notes to Apple Notes via Evernote ENEX format


![Python Tests](https://github.com/jeffredodd/googlekeep-to-applenotes/actions/workflows/python-tests.yml/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features
- 🔄 Converts Google Keep JSON export files to Evernote ENEX format
- 🎨 Preserves formatting and HTML content
- 🕒 Maintains creation and modification timestamps
- 📋 Preserves checklist items as native Apple Notes checkboxes
- 🌈 Maintains note colors and styling
- 🏷️ Extracts hashtags as tags
- 📦 Supports batch processing of multiple files
- 📚 Supports splitting large exports into multiple files

## 🚀 Why Use Keep to Notes?

Switching from Google Keep to Apple Notes? This tool makes the transition painless by:
- Preserving your note formatting and structure
- Maintaining your checklists as interactive items
- Keeping your original timestamps
- Converting your hashtags to searchable tags
- Handling large note collections efficiently

## ⚠️ Limitations

This tool is not:
- A direct Google Keep to Apple Notes API connector (requires export/import steps)
- A solution for preserving Google Keep reminders or collaborators
- A tool for converting attachments or images (these may require manual handling)
- A two-way sync solution (it's a one-time conversion)

## 🔧 Requirements

- Python 3.8+
- Required packages listed in `requirements.txt`

## 📥 Installation

1. Clone this repository:
```bash
git clone https://github.com/jeffredodd/googlekeep-to-applenotes.git
cd googlekeep-to-applenotes
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 📋 Usage

### 1️⃣ Export your Google Keep notes
- Go to [Google Takeout](https://takeout.google.com/)
- Select only "Keep" and export your data
- Extract the ZIP file to get your JSON files

### 2️⃣ Convert your notes
```bash
python keep_to_notes.py --input-dir /path/to/json/files --output-dir /path/to/output
```

### 3️⃣ For large collections, split the output:
```bash
python keep_to_notes.py --input-dir /path/to/json/files --output-dir /path/to/output --split
```

### 4️⃣ Import to Apple Notes:
- Open Apple Notes
- File > Import Notes...
- Select the generated .enex file

## 🧪 Testing

Run the tests using pytest:
```bash
pytest
```

For test coverage report:
```bash
pytest --cov=.
```

## 🔄 Continuous Integration

This project uses GitHub Actions for continuous integration. The workflow:
- 🐍 Runs on Python 3.12
- ✅ Executes all tests
- 📊 Generates test coverage reports

## 📝 Notes Format

### Google Keep JSON Format
```json
{
    "title": "Note Title",
    "textContent": "Plain text content",
    "textContentHtml": "HTML formatted content",
    "createdTimestampUsec": 1234567890000000,
    "userEditedTimestampUsec": 1234567890000000,
    "listContent": [
        {
            "text": "Task item",
            "isChecked": false
        }
    ]
}
```

### Evernote ENEX Format
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE en-export SYSTEM "http://xml.evernote.com/pub/evernote-export3.dtd">
<en-export>
    <note>
        <title>Note Title</title>
        <content>
            <![CDATA[<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">
            <en-note>HTML Content</en-note>]]>
        </content>
        <created>YYYYMMDDTHHmmssZ</created>
        <updated>YYYYMMDDTHHmmssZ</updated>
        <tags>
            <tag>tag1</tag>
        </tags>
    </note>
</en-export>
```

## 👥 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute to this project.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- Thanks to all contributors who have helped improve this tool
- Inspired by the need for a better migration path between note-taking platforms 