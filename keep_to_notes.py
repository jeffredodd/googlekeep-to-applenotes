#!/usr/bin/env python3

import json
import os
import argparse
from datetime import datetime
from bs4 import BeautifulSoup
import logging
from pathlib import Path
import re
import hashlib

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class KeepToNotesConverter:
    def __init__(self):
        self.enex_header = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE en-export SYSTEM "http://xml.evernote.com/pub/evernote-export3.dtd">
<en-export export-date="{}" application="keep-to-notes" version="1.0">'''
        
        self.note_template = '''
    <note>
        <title>{}</title>
        <content>
            <![CDATA[<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">
<en-note style="{}">
{}
</en-note>]]>
        </content>
        <created>{}</created>
        <updated>{}</updated>
        <note-attributes>
            <source>Google Keep</source>
            <source-url></source-url>
            {}
        </note-attributes>
        {}
    </note>'''

        # Color mapping from Google Keep to CSS
        self.color_map = {
            'DEFAULT': {'bg': '#ffffff', 'border': '#e0e0e0', 'text': '#000000'},
            'RED': {'bg': '#f28b82', 'border': '#d84c3b', 'text': '#5c1e18'},
            'ORANGE': {'bg': '#fbbc04', 'border': '#d69100', 'text': '#5c4001'},
            'YELLOW': {'bg': '#fff475', 'border': '#f2c600', 'text': '#5c4a00'},
            'GREEN': {'bg': '#ccff90', 'border': '#7cb342', 'text': '#2e4014'},
            'TEAL': {'bg': '#a7ffeb', 'border': '#00bfa5', 'text': '#004c41'},
            'BLUE': {'bg': '#cbf0f8', 'border': '#4fc3f7', 'text': '#0b5e7c'},
            'DARK_BLUE': {'bg': '#aecbfa', 'border': '#4285f4', 'text': '#0d2c6b'},
            'PURPLE': {'bg': '#d7aefb', 'border': '#ab47bc', 'text': '#42174d'},
            'PINK': {'bg': '#fdcfe8', 'border': '#f06292', 'text': '#6e1b3c'},
            'BROWN': {'bg': '#e6c9a8', 'border': '#b57d4f', 'text': '#4c2b15'},
            'GRAY': {'bg': '#e8eaed', 'border': '#9aa0a6', 'text': '#3c4043'}
        }

    def _convert_timestamp(self, usec_timestamp):
        """Convert microsecond timestamp to Evernote format."""
        dt = datetime.fromtimestamp(usec_timestamp / 1000000)
        return dt.strftime("%Y%m%dT%H%M%SZ")

    def _clean_html(self, html_content):
        """Clean and format HTML content for Evernote compatibility."""
        if not html_content:
            return ""
        
        soup = BeautifulSoup(html_content, 'lxml')
        
        # Remove any existing DOCTYPE or xml declarations
        if soup.contents and hasattr(soup.contents[0], 'name'):
            if soup.contents[0].name == '[document]':
                soup.contents[0].hidden = True

        # Enhance formatting for better appearance
        for tag in soup.find_all(True):
            # Improve heading styles
            if tag.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                if 'style' not in tag.attrs:
                    tag['style'] = ''
                tag['style'] += 'margin-top: 1.2em; margin-bottom: 0.8em;'
            
            # Improve paragraph spacing
            elif tag.name == 'p':
                if 'style' not in tag.attrs:
                    tag['style'] = ''
                tag['style'] += 'margin-bottom: 0.8em;'
            
            # Clean up Google-specific styles but keep important formatting
            if 'style' in tag.attrs:
                styles = tag['style'].split(';')
                cleaned_styles = []
                for s in styles:
                    s = s.strip()
                    if not s:
                        continue
                    # Keep important styles, remove Google-specific ones
                    if not s.startswith(('font-family', 'font-size')):
                        cleaned_styles.append(s)
                
                if cleaned_styles:
                    tag['style'] = '; '.join(cleaned_styles) + ';'
                else:
                    del tag['style']

        # Convert URLs to clickable links
        for text_node in soup.find_all(string=True):
            if text_node.parent.name not in ['a', 'script', 'style']:
                url_pattern = r'(https?://[^\s]+)'
                new_text = re.sub(url_pattern, r'<a href="\1">\1</a>', str(text_node))
                if new_text != str(text_node):
                    new_soup = BeautifulSoup(new_text, 'lxml')
                    text_node.replace_with(new_soup)

        return str(soup.body.decode_contents()) if soup.body else ""

    def _convert_list_content(self, list_items, color):
        """Convert Google Keep list items to a format that Apple Notes recognizes as a checklist."""
        bg_color = self.color_map.get(color, self.color_map['DEFAULT'])['bg']
        border_color = self.color_map.get(color, self.color_map['DEFAULT'])['border']
        
        # Create a styled container for the checklist
        html = [f'<div style="background-color: {bg_color}; border: 1px solid {border_color}; border-radius: 8px; padding: 12px; margin-bottom: 15px;">']
        
        # Format that Apple Notes recognizes as a to-do list
        for item in list_items:
            checked = item.get('isChecked', False)
            item_text = item.get('text', '').strip()
            if not item_text:
                continue
            
            # Use item's HTML content if available, otherwise use plain text
            item_content = self._clean_html(item.get('textHtml', '')) or item_text
            
            # Format specifically for Apple Notes
            if checked:
                # Checked item
                html.append(f'<div>☑ {item_content}</div>')
            else:
                # Unchecked item
                html.append(f'<div>☐ {item_content}</div>')
        
        html.append('</div>')
        return '\n'.join(html)

    def _get_color_style(self, color):
        """Get CSS styles for a note based on its color."""
        color_info = self.color_map.get(color, self.color_map['DEFAULT'])
        return f"background-color: {color_info['bg']}; color: {color_info['text']}; border: 1px solid {color_info['border']};"

    def _get_note_content(self, keep_note):
        """Extract and format note content based on type with enhanced styling."""
        content = []
        color = keep_note.get('color', 'DEFAULT')

        # Handle list content
        if 'listContent' in keep_note:
            content.append(self._convert_list_content(keep_note['listContent'], color))
        
        # Handle text content
        elif 'textContentHtml' in keep_note:
            cleaned_html = self._clean_html(keep_note['textContentHtml'])
            content.append(f'<div style="padding: 8px;">{cleaned_html}</div>')
        elif 'textContent' in keep_note:
            # Convert plain text to paragraphs with proper spacing
            paragraphs = keep_note['textContent'].split('\n')
            formatted_text = []
            for p in paragraphs:
                if p.strip():
                    formatted_text.append(f'<p style="margin-bottom: 0.8em;">{p}</p>')
                else:
                    formatted_text.append('<br/>')
            content.append(f'<div style="padding: 8px;">{" ".join(formatted_text)}</div>')

        return '\n'.join(content)

    def _get_note_attributes(self, keep_note):
        """Generate note attributes XML with enhanced metadata."""
        attrs = []
        
        # Add note state information
        if keep_note.get('isPinned', False):
            attrs.append('<pinned>true</pinned>')
        if keep_note.get('isArchived', False):
            attrs.append('<archived>true</archived>')
        
        # Add color as a tag
        color = keep_note.get('color', 'DEFAULT')
        if color != 'DEFAULT':
            attrs.append(f'<tag>color-{color.lower()}</tag>')
        
        # Add note type as a tag
        if 'listContent' in keep_note:
            attrs.append('<tag>list</tag>')
        else:
            attrs.append('<tag>note</tag>')
        
        return '\n            '.join(attrs)

    def _get_tags(self, keep_note):
        """Extract tags from note content and generate tags XML."""
        tags = []
        
        # Add color as a tag
        color = keep_note.get('color', 'DEFAULT')
        if color != 'DEFAULT':
            tags.append(f'<tag>color-{color.lower()}</tag>')
        
        # Add note type as a tag
        if 'listContent' in keep_note:
            tags.append('<tag>list</tag>')
        else:
            tags.append('<tag>note</tag>')
        
        # Extract hashtags from content
        content = keep_note.get('textContent', '')
        hashtags = re.findall(r'#(\w+)', content)
        for tag in hashtags:
            tags.append(f'<tag>{tag.lower()}</tag>')
        
        if tags:
            return '\n        '.join(tags)
        return ''

    def convert_note(self, keep_note):
        """Convert a single Google Keep note to Evernote format with enhanced styling."""
        title = keep_note.get('title', 'Untitled')
        color = keep_note.get('color', 'DEFAULT')
        note_style = self._get_color_style(color)
        content = self._get_note_content(keep_note)
        created = self._convert_timestamp(keep_note.get('createdTimestampUsec', 0))
        updated = self._convert_timestamp(keep_note.get('userEditedTimestampUsec', 0))
        attributes = self._get_note_attributes(keep_note)
        tags = self._get_tags(keep_note)
        
        tags_xml = f"<tags>\n        {tags}\n    </tags>" if tags else ""
        
        return self.note_template.format(title, note_style, content, created, updated, attributes, tags_xml)

    def convert_file(self, input_file):
        """Convert a single Keep JSON file to ENEX format."""
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                keep_note = json.load(f)
            
            if keep_note.get('isTrashed', False):
                logging.info(f"Skipping trashed note: {input_file}")
                return None
                
            note_content = self.convert_note(keep_note)
            logging.info(f"Successfully converted note: {keep_note.get('title', 'Untitled')}")
            return note_content
        except Exception as e:
            logging.error(f"Error converting file {input_file}: {str(e)}")
            return None

    def convert_directory(self, input_dir, output_dir, split_files=False):
        """Convert all Keep JSON files in a directory to ENEX files."""
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        all_notes = []
        file_count = 0
        
        for json_file in input_path.glob('*.json'):
            note_content = self.convert_file(json_file)
            if note_content:
                all_notes.append(note_content)
                file_count += 1
        
        if not all_notes:
            logging.warning("No valid notes found to convert")
            return
        
        # Create the ENEX file(s)
        export_date = datetime.now().strftime("%Y%m%dT%H%M%SZ")
        
        if split_files and len(all_notes) > 50:
            # Split into multiple files if there are many notes
            chunks = [all_notes[i:i + 50] for i in range(0, len(all_notes), 50)]
            for i, chunk in enumerate(chunks):
                output_file = output_path / f"keep_notes_export_{i+1}.enex"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(self.enex_header.format(export_date))
                    for note in chunk:
                        f.write(note)
                    f.write("\n</en-export>")
                logging.info(f"Created file {output_file} with {len(chunk)} notes")
        else:
            # Create a single file
            output_file = output_path / "keep_notes_export.enex"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(self.enex_header.format(export_date))
                for note in all_notes:
                    f.write(note)
                f.write("\n</en-export>")
            logging.info(f"Successfully converted {len(all_notes)} notes to {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Convert Google Keep JSON files to Evernote ENEX format')
    parser.add_argument('--input-dir', required=True, help='Directory containing Keep JSON files')
    parser.add_argument('--output-dir', required=True, help='Directory to save ENEX files')
    parser.add_argument('--split', action='store_true', help='Split output into multiple files if there are many notes')
    args = parser.parse_args()
    
    converter = KeepToNotesConverter()
    converter.convert_directory(args.input_dir, args.output_dir, args.split)

if __name__ == '__main__':
    main() 