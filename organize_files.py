import os
import sys

# Get the path of the folder to organize
folder_to_organize = sys.argv[1]

# Get the list of files and folders in the given folder
file_list = os.listdir(folder_to_organize)

# Go through the list of files and folders
for file in file_list:
    # Get the file name and its extension
    file_name, file_ext = os.path.splitext(file)
    # Get the path of the folder to organize
    folder_to_organize_path = os.path.join(os.getcwd(), folder_to_organize)
    # Get the path of the folder for the given file extension
    folder_for_ext_path = os.path.join(folder_to_organize_path, file_ext[1:].upper())
    # If the folder for the file extension does not exist, create it
    if not os.path.exists(folder_for_ext_path):
        os.makedirs(folder_for_ext_path)
    # Move the file to the folder for its extension
    os.rename(os.path.join(folder_to_organize_path, file), os.path.join(folder_for_ext_path, file))
