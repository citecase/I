import re
import sys
import os

def convert_md_to_table(input_text):
    """
    Parses a Markdown file with case headers and notes, 
    converting it into a structured Markdown table.
    """
    lines = input_text.split('\n')
    
    # Header for the Markdown table
    table_header = "| Case Name | Neutral Citation | Note |\n| :--- | :--- | :--- |"
    table_rows = []
    
    current_case_link = ""
    current_citation = ""
    
    # Patterns
    # Matches [Name](URL)
    link_pattern = re.compile(r'\[(.*?)\]\((.*?)\)')
    # Matches Year + Upper Case Letters + Number (e.g., 2026 INSC 101)
    citation_pattern = re.compile(r'\d{4}\s+[A-Z]+\s+\d+')
    # Matches lines that are just symbols/punctuation/whitespace
    symbol_only_pattern = re.compile(r'^[ \t\W_]+$')

    for line in lines:
        stripped = line.strip()
        
        # Skip truly empty lines
        if not stripped:
            continue
            
        # Identify headers (Cases)
        if stripped.startswith('#'):
            # Extract Case Name with Link
            link_match = link_pattern.search(stripped)
            if link_match:
                current_case_link = f"[{link_match.group(1)}]({link_match.group(2)})"
            else:
                # Fallback: take header text without #
                clean_header = re.sub(r'^#+\s*', '', stripped)
                current_case_link = clean_header.split(' - ')[0]

            # Extract Citation (specifically looking for INSC or similar patterns)
            cit_match = citation_pattern.search(stripped)
            if cit_match:
                current_citation = cit_match.group(0)
            else:
                # If no neutral citation pattern is found, keep it blank
                current_citation = ""
        
        # Identify Notes
        elif current_case_link:
            # RULE: Ignore lines that are just symbols (e.g., "---", "***", "...")
            if symbol_only_pattern.match(stripped):
                continue
                
            # Clean list markers if they exist
            note_content = re.sub(r'^([-*+]|\d+\.)\s+', '', stripped)
            
            # Final check: if after cleaning list markers it's empty or just symbols, skip
            if not note_content or symbol_only_pattern.match(note_content):
                continue

            # Escape any pipe characters in the note to avoid breaking the table
            note_content = note_content.replace('|', '\\|')
            
            # Format as a table row
            row = f"| {current_case_link} | {current_citation} | {note_content} |"
            table_rows.append(row)

    if not table_rows:
        return None

    return f"{table_header}\n" + "\n".join(table_rows)

def main():
    # Check for command line arguments (useful for GitHub Actions)
    if len(sys.argv) > 2:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        
        if not os.path.exists(input_file):
            print(f"Error: {input_file} not found.")
            return

        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        result = convert_md_to_table(content)
        
        if result:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"Successfully converted {input_file} to {output_file}")
        else:
            print("No valid case data found to convert.")
    else:
        print("Usage: python converter.py <input_file.md> <output_file.md>")

if __name__ == "__main__":
    main()
