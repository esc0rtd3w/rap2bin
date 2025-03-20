# rap2bin 20241123

import os
import struct

# Root directory of the script
root_directory = os.path.dirname(os.path.abspath(__file__))

# Directory containing the .rap files
rap_directory = os.path.join(root_directory, "exdata")

# Output binary file
output_bin_file = os.path.join(root_directory, "rap.bin")

# Log file
log_file = os.path.join(root_directory, "rap_log.txt")

# Magic number to prepend for each entry, followed by 12 bytes of padding
MAGIC_NUMBER = b"\xFA\xF0\xFA\xF0" + b"\x00" * 12

# Padding after CONTENT_ID
CONTENT_ID_PADDING = b"\x00" * 12

# Read 16-byte content from each .rap file and write to a binary file
def create_rap_bin(rap_directory, output_bin_file, log_file):
    with open(output_bin_file, "wb") as bin_file, open(log_file, "w") as log:
        for root, _, files in os.walk(rap_directory):
            for filename in files:
                if filename.endswith(".rap") or filename.endswith(".RAP"):
                    rap_path = os.path.join(root, filename)
                    try:
                        with open(rap_path, "rb") as rap_file:
                            rap_content = rap_file.read(16)
                            content_id = filename.replace(".rap", "").replace(".RAP", "")
                            if len(rap_content) == 16:
                                if len(content_id) == 0x24:
                                    # Prepare binary entry with magic number, padding, CONTENT_ID, padding, and 16 bytes of content
                                    entry = MAGIC_NUMBER + content_id.encode() + CONTENT_ID_PADDING + rap_content
                                    bin_file.write(entry)
                                    # Log in the format: CONTENT_ID:16 byte value in hex
                                    log.write(f"{content_id}:{rap_content.hex()}\n")
                                else:
                                    log.write(f"Error: {filename} CONTENT_ID length is not 0x24\n")
                            else:
                                log.write(f"Error: {filename} does not contain 16 bytes of data\n")
                    except Exception as e:
                        log.write(f"Error processing {filename}: {e}\n")

# Create the rap.bin file
create_rap_bin(rap_directory, output_bin_file, log_file)
