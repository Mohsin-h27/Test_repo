# Step 1- Converting modules to .md files using pydoc_markdown
import os
from pydoc_markdown import Context, PythonLoader, MarkdownRenderer
from collections import OrderedDict
import re
from typing import Set, List, Dict, Optional
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
import json

def convert_py_to_md_with_pydoc(source_folder: str, output_folder: str):
    """
    Converts Python files in the source folder to markdown documentation in the output folder using pydoc_markdown.

    Args:
    - source_folder (str): Path to the folder containing .py files.
    - output_folder (str): Path to the folder where the generated .md files will be saved.
    """
    # List of files to exclude from conversion (by filename)
    exclude_files = {'utils.py', 'db.py', 'init.py', '__init__.py'}

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Set up context for pydoc_markdown
    context = Context(directory=source_folder)

    # Initialize loader and renderer for generating markdown
    loader = PythonLoader(search_path=[source_folder])  # Load from the provided source folder
    renderer = MarkdownRenderer(render_module_header=False)

    # Initialize the components
    loader.init(context)
    renderer.init(context)

    # Get all Python files in the source folder (excluding excluded ones)
    python_files = [f for f in os.listdir(source_folder) if f.endswith('.py') and f not in exclude_files]

    # Load the Python modules (files) from the filtered list
    modules = loader.load()

    # Process each module and generate markdown documentation
    for module in modules:
        # Check if the module corresponds to an excluded file
        module_file_name = module.name + ".py"  # Convert module name to file name

        if module_file_name in exclude_files:
            print(f"Skipping {module_file_name} as it is in the exclusion list.")
            continue

        # Generate the output markdown file path
        output_file = os.path.join(output_folder, f"{module.name}.md")

        # Write the rendered markdown to the output file
        with open(output_file, "w", encoding="utf-8") as md_file:
            md_file.write(renderer.render_to_string([module]))

        print(f"Generated documentation for {module.name}: {output_file}")


#Step-2 Post processing the individual markdown modules

def clean_markdown_content(content):
    # Split content into lines
    lines = content.split('\n')
    cleaned_lines = []
    skip_mode = True  # Start in skip mode

    for line in lines:
        # Check for the end of introductory section
        if skip_mode:
            # Look for patterns that indicate the start of API documentation
            if (line.startswith('## ') or
                line.startswith('#### ') or
                '<a id="' in line or
                '```' in line):
                skip_mode = False
                cleaned_lines.append(line)
        else:
            cleaned_lines.append(line)

    # Join lines back together
    content = '\n'.join(cleaned_lines)

    # Remove HTML anchor tags
    content = re.sub(r'<a id="[^"]*"></a>', '', content)

    # Remove empty sections (headers with no content)
    content = re.sub(r'##\s*\n+##', '##', content)

    # Remove HTML anchor tags and their associated empty sections
    content = re.sub(r'<a id="[^"]*"></a>\s*\n\s*##\s*\n', '', content)

    # Remove empty text blocks
    content = re.sub(r'""\s*\n', '', content)
    content = re.sub(r'"[^"]*"\s*\n', '', content)

    # Remove standalone headers with no content
    content = re.sub(r'^##\s*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^####\s*$', '', content, flags=re.MULTILINE)

    # Remove redundant section markers
    content = re.sub(r'##\s*$', '', content, flags=re.MULTILINE)

    # Remove multiple consecutive empty lines
    content = re.sub(r'\n{3,}', '\n\n', content)

    # Remove leading/trailing whitespace from each line
    content = '\n'.join(line.strip() for line in content.splitlines())

    # Remove leading/trailing empty lines
    content = content.strip()

    # Remove duplicate sections
    lines = content.split('\n')
    seen_sections = OrderedDict()
    cleaned_lines = []

    for line in lines:
        if line.startswith('## '):
            section = line.strip()
            if section not in seen_sections:
                seen_sections[section] = True
                cleaned_lines.append(line)
        else:
            cleaned_lines.append(line)

    content = '\n'.join(cleaned_lines)

    # Final cleanup of any remaining empty lines
    content = re.sub(r'\n{3,}', '\n\n', content)
    content = content.strip()

    return content

def process_markdown_files(source_directory='.', output_directory=None):
    # If output directory is not specified, use the source directory
    if output_directory is None:
        output_directory = source_directory

    # Get all markdown files in the source directory
    markdown_files = list(Path(source_directory).glob('*.md'))

    for file_path in markdown_files:
        print(f"Processing {file_path}...")

        try:
            # Read the file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Clean the content
            cleaned_content = clean_markdown_content(content)

            # Create the output file path
            output_path = Path(output_directory) / file_path.name

            # Only write if content has changed
            if cleaned_content != content:
                # Create backup in the source directory
                backup_path = file_path.with_suffix('.md.bak')
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(content)

                # Write cleaned content to the output directory
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(cleaned_content)

                print(f"Cleaned {file_path} (backup created at {backup_path}, cleaned file saved to {output_path})")
            else:
                # If no changes, just copy the file to the output directory
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"No changes needed for {file_path} (copied to {output_path})")

        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")



class MarkdownCombiner:
    """
    Combines the content of all processed Markdown files into the output file.
    Also ensures no consecutive empty lines.
    """

    def __init__(self, input_directory: str = '.', output_filename: str = 'combined_documentation.md') -> None:
        """
        Initializes the MarkdownCombiner.

        Args:
            input_directory: The path to the directory containing the Markdown files (default: current directory).
            output_filename: The name of the output file (default: 'combined_documentation.md').
        """
        self.input_directory = Path(input_directory)
        self.output_path = Path(f"md_files/{output_filename}")
        self.ignored_files: Set[str] = {'README.md', 'db.md', 'init.md', '__init__.md', output_filename}

    def _find_markdown_files(self) -> List[Path]:
        """
        Finds all Markdown files in the input directory, excluding ignored files.

        Returns:
            A sorted list of Path objects representing the Markdown files.
            The sorting is primarily based on the number of dots in the filename (fewer dots first),
            and then alphabetically by filename.
        """
        markdown_files = [
            file for file in self.input_directory.glob('*.md') if file.name not in self.ignored_files
        ]
        print(f"Found Markdown files: {[f.name for f in markdown_files]}")
        return sorted(markdown_files, key=lambda f: (f.name.count('.'), f.name))

    def _format_filename_to_heading(self, filename: str) -> str:
        """
        Formats a filename (e.g., 'users.messages.md') into a level 1 heading
        (e.g., 'users.messages').

        Args:
            filename: The name of the Markdown file.

        Returns:
            The formatted level 1 heading string.
        """
        return filename.replace('.md', '')

    def _process_content(self, content: str) -> str:
        """
        Processes the content of a Markdown file,ensuring no consecutive empty lines remain,
        and explicitly removing lines containing 'save_state' or 'load_state'.

        Args:
            content: The raw content of the Markdown file.

        Returns:
            The processed content as a string.
        """
        lines = content.splitlines()
        processed_lines: List[str] = []
        h2_pattern = re.compile(r'^\s*##\s+.+$')
        forbidden_strings = {"save_state", "save\_state", "load_state", "load\_state"}

        for line in lines:
            if not h2_pattern.match(line) and not any(fs in line for fs in forbidden_strings):
                processed_lines.append(line)

        # Remove consecutive empty lines
        final_lines: List[str] = []
        previous_was_empty = False
        for line in processed_lines:
            is_empty = line.strip() == ''
            if not is_empty or not previous_was_empty:
                final_lines.append(line)
            previous_was_empty = is_empty

        return '\n'.join(final_lines)

    def combine_markdown(self) -> None:
        """
        Combines the content of all processed Markdown files into the output file.
        Each file's content is preceded by a level 1 heading derived from the filename.
        All level 2 headings and lines containing 'save_state' or 'load_state' within the files
        are removed, and there are no consecutive empty lines.
        """
        markdown_files = self._find_markdown_files()

        with self.output_path.open('w', encoding='utf-8') as outfile:
            for file in markdown_files:
                title = self._format_filename_to_heading(file.name)
                outfile.write(f"# {title}\n\n")

                raw_content = file.read_text(encoding='utf-8')
                processed_content = self._process_content(raw_content)

                outfile.write(processed_content)
                outfile.write("\n\n---\n\n")

        print(f"✅ Combined Markdown content to: {self.output_path}")



def update_md_files_to_drive(service, md_folder_path, drive_folder_id = '13XAvA5bFwvVlfCmnfeoPsluMjz6vEn10' ):
    """
    Update each file in md_files to corresponding file in Drive folder.
    """
    # List all files in local md_files folder
    for filename in os.listdir(md_folder_path):
        local_file_path = os.path.join(md_folder_path, filename)
        
        if not os.path.isfile(local_file_path):
            continue  # Skip if it's a folder
        
        # Find the matching file in Drive
        query = f"'{drive_folder_id}' in parents and name = '{filename}' and trashed = false"
        response = service.files().list(q=query, fields="files(id, name)").execute()
        files = response.get('files', [])

        if not files:
            print(f"❌ File '{filename}' not found in Drive folder.")
            continue
        
        file_id = files[0]['id']  # Take the first match

        # Update the file content
        media = MediaFileUpload(local_file_path, resumable=True)
        service.files().update(fileId=file_id, media_body=media).execute()
        
        print(f"✅ Updated '{filename}' in Drive.")


def authenticate():
    """Authenticate using service account."""
    creds_dict = json.loads(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
    creds = service_account.Credentials.from_service_account_info(
        creds_dict,
        scopes=["https://www.googleapis.com/auth/drive"]
    )
    return build("drive", "v3", credentials=creds)


# step 1

for name in os.listdir('APIs'):
    if os.path.isdir(os.path.join('APIs', name)):
        API_name = name

        source_folder = os.path.abspath(os.path.join('APIs', API_name))  # Absolute path
        output_folder = f'APIs_docs/{API_name}_modularized_docs'

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        convert_py_to_md_with_pydoc(source_folder, output_folder)

        # Specify the source folder containing markdown files
        source_folder = output_folder

        # Specify the output folder where cleaned files will be saved
        output_dir = f'{output_folder}/final'
        # Ensure the output folder exists
        os.makedirs(output_dir, exist_ok=True)

        # Process the markdown files in the source folder and save cleaned versions to the output folder
        process_markdown_files(source_folder, output_dir)

        print(f"Markdown files from '{source_folder}' have been processed and saved to '{output_dir}'.")


        # step 3

        output_dir =  f'{output_folder}/final'
        os.makedirs('md_files', exist_ok=True)
        combiner = MarkdownCombiner(input_directory=output_dir, output_filename=f"{API_name.split('APISimulation')[0]}NLDescription.md")
        combiner.combine_markdown()


service = authenticate()

md_folder_path = "md_files"

update_md_files_to_drive(service, md_folder_path)
