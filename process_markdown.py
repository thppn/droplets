import os
import re

def parse_markdown(markdown_content):
    # Split the content into sections based on # headings
    sections = re.split(r'^#\s+.+$', markdown_content, flags=re.MULTILINE)
    headings = re.findall(r'^#\s+(.+)$', markdown_content, flags=re.MULTILINE)

    # If there are no sections, return empty results
    if not headings:
        return [], []

    # Parse each section to extract files and commands
    folders = []
    files = []
    commands = []

    for i, section in enumerate(sections[1:]):  # Skip the first split (empty or content before the first #)
        # Extract all ### filenames and commands in this section
        file_matches = re.findall(r'^###\s+(.+)$', section, flags=re.MULTILINE)
        command_matches = re.findall(r'```bash\n([\s\S]*?)\n```', section, flags=re.MULTILINE)

        # Ensure the number of files matches the number of commands
        if len(file_matches) != len(command_matches):
            raise ValueError(f"Mismatch between files and commands in section: {headings[i]}")

        # Add the folder, files, and commands to the results
        folders.append(headings[i])
        files.append(file_matches)
        commands.append(command_matches)

    return folders, files, commands

def create_bash_files(master_folder, folders, files, commands):
    # Create the master folder if it doesn't exist
    if not os.path.exists(master_folder):
        os.makedirs(master_folder)

    # Iterate through each folder and its corresponding files/commands
    for folder, folder_files, folder_commands in zip(folders, files, commands):
        # Create the subfolder under the master folder
        subfolder_path = os.path.join(master_folder, folder)
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)

        # Create each file in the subfolder
        for file, command in zip(folder_files, folder_commands):
            file_path = os.path.join(subfolder_path, file)
            with open(file_path, 'w') as f:
                f.write("#!/bin/bash\n")
                f.write(command.strip() + "\n")

            # Make the file executable
            os.chmod(file_path, 0o755)

def main(markdown_file):
    # Derive the master folder name from the markdown file name
    master_folder = os.path.splitext(os.path.basename(markdown_file))[0]

    # Read the markdown file
    with open(markdown_file, 'r') as f:
        content = f.read()

    # Parse the markdown content
    folders, files, commands = parse_markdown(content)

    # Create the bash files and folders
    create_bash_files(master_folder, folders, files, commands)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python process_markdown.py <markdown_file>")
        sys.exit(1)

    markdown_file = sys.argv[1]
    main(markdown_file)