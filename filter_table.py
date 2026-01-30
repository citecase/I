import sys
import os

def filter_arbitration_rows(input_file, output_file):
    """
    Reads a Markdown table and creates a new file containing only the header 
    and rows that include the keyword 'civil procedure'.
    """
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            # Read all lines and strip trailing whitespace/newlines
            lines = [line for line in f.readlines() if line.strip()]

        if len(lines) < 2:
            print("Table is empty or invalid (not enough lines for header).")
            return

        # Keep the header and separator rows (first two lines)
        header = lines[0]
        separator = lines[1]
        
        filtered_rows = []
        keyword = "civil procedure"

        # Process each row starting from line 3
        for line in lines[2:]:
            # Case-insensitive check for the keyword
            # We check the whole line so it catches 'civil procedure' in name, citation, or note
            if keyword.lower() in line.lower():
                # Ensure the line ends with a single newline
                clean_line = line.strip() + "\n"
                filtered_rows.append(clean_line)

        if filtered_rows:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(header.strip() + "\n")
                f.write(separator.strip() + "\n")
                f.writelines(filtered_rows)
            print(f"Successfully filtered {len(filtered_rows)} rows into {output_file}")
        else:
            print(f"No rows found containing '{keyword}'. Output file not updated/created.")
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Usage: python filter_table.py cases_table.md arbitration_cases.md
    if len(sys.argv) > 2:
        filter_arbitration_rows(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python filter_table.py <input_table.md> <output_file.md>")
