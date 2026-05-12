import os
import datetime
import string
import random
import re
from typing import Optional

def generate_filename():
    # Get the current date in YYYYMMDD format
    current_date = datetime.datetime.now().strftime("%Y%m%d")

    # Generate a random 5-character string
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=5))

    # Create the filename
    filename = f"{current_date}-{random_string}.txt"

    return filename

def write_to_file(content):
	# Specify the file name
	file_name = generate_filename()

	# Open the file in write mode
	with open(file_name, "w") as file:
	    # Write the text content to the file
	    file.write(content)


def join_files_with_prefix(prefix, dir: Optional[str] = None):
    # Get a list of all files in the given/current directory
    if dir is None:
        current_dir = os.getcwd()
    else:
        current_dir = dir
    files = os.listdir(current_dir)
    # print(files)
    # Filter files based on the prefix
    filtered_files = [file for file in files if file.startswith(prefix) and file.endswith('.txt')]
    # print(filtered_files)
    # Create the output file name
    output_file = prefix + '.txt'

    # Open the output file in write mode
    with open(output_file, 'w') as outfile:
        # Iterate over the filtered files
        for file in filtered_files:
            # Open each file in read mode
            file = dir + "/" + file
            # print(file)
            with open(file, 'r') as infile:
                # Read the content of the file
                content = infile.read()

                # Write the content to the output file
                outfile.write(content)

                # Add a newline character for separation
                outfile.write('\n')

    print(f"Files with prefix '{prefix}' joined successfully into '{output_file}'.")


def extract_domain(url):
    # The regular expression pattern to find domain
    pattern = r'(https?|chrome)://([A-Za-z0-9.-]+)'

    match = re.search(pattern, url)
    if match:
        return match.group(2)

    print("[WARN] No regex match for " + url)
    return None

# map from domain -> tabs for/under that domain
def create_domain_keyed_tab_store(tabs):
	store = {}
	for tab in tabs:
		# print(f"- {tab.url}")
		# print(f"  {tab.title}")
		# print(f"  {tab.domain}")

		if tab.domain not in store:
			store[tab.domain] = []

		store[tab.domain].append(tab)
	return store

def read_file(file_path: str) -> Optional[str]:
    """
    Reads the contents of a file in the project directory.
    Returns None if the file does not exist.
    """
    if os.path.isfile(file_path):
        with open(file_path, "r") as f:
            contents = f.read()
        return contents
    else:
        print(f"File '{file_path}' wasn't found")
        return None

def write_file(file_path: str, content: str) -> None:
    """
    Writes the given content to a file in the project directory.
    Creates any missing directories in the file path.
    """
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(file_path, "w") as f:
        f.write(content)
    print(f"Wrote to file '{file_path}'")
