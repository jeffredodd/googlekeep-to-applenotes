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

## 📥 Complete Installation Guide (for Beginners)

### Step 1: Install Python

If you don't have Python installed:

#### Windows:
1. Download the installer from [python.org](https://www.python.org/downloads/)
2. Run the installer, making sure to check "Add Python to PATH"
3. Verify installation by opening Command Prompt and typing:
   ```
   python --version
   ```

#### macOS:
1. Install [Homebrew](https://brew.sh/) if you don't have it:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
2. Install Python:
   ```bash
   brew install python
   ```
3. Verify installation:
   ```bash
   python3 --version
   ```

#### Linux:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
python3 --version
```

### Step 2: Clone the Repository

1. Install Git if you don't have it:
   - Windows: Download from [git-scm.com](https://git-scm.com/download/win)
   - macOS: `brew install git`
   - Linux: `sudo apt install git`

2. Clone the repository:
   ```bash
   git clone https://github.com/jeffredodd/googlekeep-to-applenotes.git
   cd googlekeep-to-applenotes
   ```

### Step 3: Set Up a Virtual Environment

A virtual environment keeps your project dependencies isolated from other Python projects.

#### Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

You'll know the virtual environment is active when you see `(venv)` at the beginning of your command prompt.

### Step 4: Install Dependencies

With the virtual environment activated:

```bash
pip install -r requirements.txt
```

### Step 5: Verify Installation

Run a simple test to make sure everything is working:

```bash
python -m pytest
```

If the tests pass, you're all set!

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

## ❓ Troubleshooting

### Common Issues

#### "Command not found: python"
- Make sure Python is installed and added to your PATH
- On macOS/Linux, try using `python3` instead of `python`

#### "No module named 'xyz'"
- Make sure you've activated your virtual environment
- Try reinstalling dependencies: `pip install -r requirements.txt`

#### "Permission denied" when running the script
- Make the script executable: `chmod +x keep_to_notes.py`

#### Virtual Environment Issues
- If you're having trouble with the virtual environment, you can also install dependencies globally:
  ```bash
  pip install -r requirements.txt
  ```
  (Note: This is not recommended for development work, but can be a quick solution for just running the tool) 