# Keep to Notes Converter

A Python script to convert Google Keep JSON files to Evernote ENEX format for importing into Apple Notes.

## Features

- Converts Google Keep JSON export files to Evernote ENEX format
- Preserves formatting and HTML content
- Maintains creation and modification timestamps
- Handles titles and content properly
- Supports batch processing of multiple files

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

3. Import the generated .enex files into Apple Notes:
   - Open Apple Notes
   - File > Import Notes...
   - Select the generated .enex file

## Testing

Run the tests using pytest:
```bash
pytest
```

## Notes Format

### Google Keep JSON Format
```json
{
    "title": "Note Title",
    "textContent": "Plain text content",
    "textContentHtml": "HTML formatted content",
    "createdTimestampUsec": 1234567890000000,
    "userEditedTimestampUsec": 1234567890000000
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
    </note>
</en-export>
``` 