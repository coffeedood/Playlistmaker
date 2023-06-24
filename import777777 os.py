import os
import hashlib

def get_file_checksum(file_path):
    # Calculate the MD5 checksum of the file
    with open(file_path, 'rb') as f:
        md5_hash = hashlib.md5()
        while chunk := f.read(8192):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()

def delete_duplicates(source_directory, check_directory):
    # Dictionary to store file names, sizes, and corresponding paths
    files = {}

    # Traverse the source directory
    for root, dirs, files_list in os.walk(source_directory):
        for file_name in files_list:
            source_file_path = os.path.join(root, file_name)

            # Calculate the size of the file
            size = os.path.getsize(source_file_path)

            # Add the filename, size, and source file path to the dictionary
            files[(file_name, size)] = source_file_path

    # Traverse the check directory
    for root, dirs, files_list in os.walk(check_directory):
        for file_name in files_list:
            check_file_path = os.path.join(root, file_name)

            # Calculate the size of the file
            size = os.path.getsize(check_file_path)

            if (file_name, size) in files:
                source_file_path = files[(file_name, size)]

                # Calculate the checksum of the check file
                check_checksum = get_file_checksum(check_file_path)

                # Calculate the checksum of the source file
                source_checksum = get_file_checksum(source_file_path)

                # Check if both the filename and file content are identical
                if check_checksum == source_checksum:
                    # Delete the duplicate file from the check directory
                    os.remove(check_file_path)
                    print(f'Deleted duplicate file: {check_file_path}')
            else:
                # Add the filename, size, and check file path to the dictionary
                files[(file_name, size)] = check_file_path

# Select the source directory and the directory to check for duplicates
source_directory = '/media/riley/Expansion/Media/Music'
check_directory = '/media/riley/BACKUP PLUS/09'

# Call the function to delete duplicate files
delete_duplicates(source_directory, check_directory)
