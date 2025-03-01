import pytest
from keep_to_notes import KeepToNotesConverter
from pathlib import Path
import json
import tempfile
import os
from datetime import datetime

@pytest.fixture
def converter():
    return KeepToNotesConverter()

@pytest.fixture
def sample_keep_note():
    return {
        "title": "Test Note",
        "textContent": "This is a test note",
        "textContentHtml": "<p>This is a test note</p>",
        "createdTimestampUsec": 1582955199253000,
        "userEditedTimestampUsec": 1582955199253000,
        "isTrashed": False
    }

def test_convert_timestamp(converter):
    timestamp = 1582955199253000  # microseconds
    expected = "20200229T075319Z"
    assert converter._convert_timestamp(timestamp) == expected

def test_clean_html(converter):
    html = '''<p dir="ltr" style="line-height:1.38;margin-top:0.0pt;margin-bottom:0.0pt;">
              <span style="font-family:'Google Sans';font-size:16.0pt;">Test content</span></p>'''
    cleaned = converter._clean_html(html)
    assert 'font-family' not in cleaned
    assert 'font-size' not in cleaned
    assert 'Test content' in cleaned

def test_convert_note(converter, sample_keep_note):
    note_xml = converter.convert_note(sample_keep_note)
    assert '<title>Test Note</title>' in note_xml
    assert 'This is a test note' in note_xml
    assert '<created>20200229T075319Z</created>' in note_xml
    assert '<updated>20200229T075319Z</updated>' in note_xml

def test_convert_note_without_html(converter):
    note = {
        "title": "Plain Text Note",
        "textContent": "Just plain text",
        "createdTimestampUsec": 1582955199253000,
        "userEditedTimestampUsec": 1582955199253000
    }
    note_xml = converter.convert_note(note)
    assert '<title>Plain Text Note</title>' in note_xml
    assert '<div>Just plain text</div>' in note_xml

def test_convert_trashed_note(converter, tmp_path):
    trashed_note = {
        "title": "Trashed Note",
        "textContent": "This note is in trash",
        "isTrashed": True
    }
    
    # Create a temporary JSON file
    note_file = tmp_path / "trashed.json"
    with open(note_file, 'w') as f:
        json.dump(trashed_note, f)
    
    result = converter.convert_file(note_file)
    assert result is None

def test_convert_directory(converter, tmp_path):
    # Create test input directory
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    
    # Create test notes
    notes = [
        {
            "title": f"Note {i}",
            "textContent": f"Content {i}",
            "createdTimestampUsec": 1582955199253000,
            "userEditedTimestampUsec": 1582955199253000
        }
        for i in range(3)
    ]
    
    # Write test notes to files
    for i, note in enumerate(notes):
        with open(input_dir / f"note{i}.json", 'w') as f:
            json.dump(note, f)
    
    # Convert notes
    converter.convert_directory(input_dir, output_dir)
    
    # Check output
    output_file = output_dir / "keep_notes_export.enex"
    assert output_file.exists()
    
    with open(output_file, 'r') as f:
        content = f.read()
        assert all(f"<title>Note {i}</title>" in content for i in range(3))
        assert all(f"<div>Content {i}</div>" in content for i in range(3)) 