# Keep to Notes Converter

A Python script to convert Google Keep JSON files to Evernote ENEX format for importing into Apple Notes.

![Python Tests](https://github.com/username/keep-to-notes/actions/workflows/python-tests.yml/badge.svg)

## Features

- Converts Google Keep JSON export files to Evernote ENEX format
- Preserves formatting and HTML content
- Maintains creation and modification timestamps
- Handles titles and content properly
- Supports batch processing of multiple files
- Preserves checklist items as native Apple Notes checkboxes
- Maintains note colors and styling
- Extracts hashtags as tags
- Supports splitting large exports into multiple files

## Requirements

- Python 3.8+
- Required packages listed in `requirements.txt`

## Installation

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Place your Google Keep JSON files in a directory
2. Run the converter:
```bash
python keep_to_notes.py --input-dir /path/to/json/files --output-dir /path/to/output
```

3. For large collections, you can split the output into multiple files:
```bash
python keep_to_notes.py --input-dir /path/to/json/files --output-dir /path/to/output --split
```

4. Import the generated .enex files into Apple Notes:
   - Open Apple Notes
   - File > Import Notes...
   - Select the generated .enex file

## Testing

Run the tests using pytest:
```bash
pytest
```

For test coverage report:
```bash
pytest --cov=.
```

## Continuous Integration

This project uses GitHub Actions for continuous integration. The workflow:
- Runs on Python 3.8, 3.9, and 3.10
- Executes all tests
- Generates test coverage reports

## Notes Format

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