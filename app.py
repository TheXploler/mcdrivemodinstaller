import gdown
import os
import shutil
import zipfile
import time

default_destination = os.getenv('APPDATA')

def splash_screen():
    print("Welcome ToaFu's Assortments of Things Modpack Installer/Updater!")
    print("Script installer created by: Fandrest")
    print("IF YOU HAVE USED THIS PROGRAM BEFORE, PLEASE MAKE SURE YOU DELETE THE OLD ZIP FILE IN THE DIRECTORY BEFORE INSTALLING THE NEW ONE!")
    print("============================================")

#Setup minecraft folder location
def setup():
    print(" ")
    default_minecraft_destination = f"{default_destination}\.minecraft"
    print(f"Current minecraft folder destination: {default_minecraft_destination}")
    user_folder_destination = input("Custom folder destination (JUST HIT ENTER IF YOU WANT TO USE THE DEFAULT FOLDER ABOVE): ")
    if user_folder_destination == "":
        user_folder_destination = default_minecraft_destination
    else:
        print(" ")
        print(f"Current minecraft folder destination: {user_folder_destination}")
        user_folder_destination_confirm = input("Is this correct? (y/n): ")
        if user_folder_destination_confirm != "y":
            user_folder_destination = default_minecraft_destination
            setup()
    return user_folder_destination

#Remove folder
def remove_folder():
    if os.path.exists(f"{user_folder_destination}/mods"):
        print(" ")
        print(f"Backing up folder {user_folder_destination}/mods...")
        shutil.rmtree(f"{user_folder_destination}/mods")
        print(f"Removing folder {user_folder_destination}/config...")
        shutil.rmtree(f"{user_folder_destination}/config")
        print(f"Creating folder {user_folder_destination}/config...")
        os.mkdir(f"{user_folder_destination}/config")
    else:
        print(" ")
        print("No folder found to remove")

#Get zip filename
def get_zip_filename():
    directory = os.getcwd()
    for filename in os.listdir(directory):
        if filename.endswith(".zip"):
            return filename
    return None

#Download mod file
def download_mod_file():
    print(" ")
    download_file_input = input("Please insert the google drive ID (The long string of text after 'https://drive.google.com/file/d/'): ")
    download_file = f"https://drive.google.com/uc?id={download_file_input}"
    print(f"Now downloading {download_file}...")
    gdown.download(download_file)
    get_zip_filename()

#Unzip mod file
def unzip_mod_file(zip_file, destination):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(destination)

#Check if directory exists
def check_directory_exists(directory):
    if os.path.exists(directory):
        return True
    else:
        return False




#Start
splash_screen()
user_folder_destination = setup()

#Get zip filename and the raw zip filename (without extension)
zip_filename = get_zip_filename()
if zip_filename != None:
    raw_zip_filename = os.path.splitext(zip_filename)[0]

if zip_filename:

    #Check if there's an existing download file
    print(" ")
    print(f"It seems like you've downloaded the mod zip file before: {zip_filename}")
    zip_filename_confirm = input("Would you like to use it? (y/n): ")
    if zip_filename_confirm != "y":
        os.remove(zip_filename)
        download_mod_file()
        zip_filename = get_zip_filename()
        raw_zip_filename = os.path.splitext(zip_filename)[0]
        print(f"Unzipping {zip_filename}...")
        destination = os.getcwd()
        unzip_mod_file(zip_filename, destination)
    else:
        print(" ")
        print("Using cached downloads")

        #Check if the zip folder has been unzipped
        zip_filename = get_zip_filename()
        raw_zip_filename = os.path.splitext(zip_filename)[0]
        check_dir = check_directory_exists(raw_zip_filename)
        if check_dir == False:
            print(" ")
            print(f"Unzipping {zip_filename}...")
            destination = os.getcwd()
            unzip_mod_file(zip_filename, destination)
        else:
            print(" ")
            print(f"Skipping unzipping, folder with same name already exists from {zip_filename}: {raw_zip_filename}")
else:
    print(" ")
    print("No cached downloads found")
    download_mod_file()
    zip_filename = get_zip_filename()
    raw_zip_filename = os.path.splitext(zip_filename)[0]
    print(f"Unzipping {zip_filename}...")
    destination = os.getcwd()
    unzip_mod_file(zip_filename, destination)

#Install mods
print(" ")
print("Installing mods in 3 seconds... (Ctrl+C to abort)")
for i in range(3, 0, -1):
    print(f"{i}...")
    time.sleep(1)

#Remove existing folder on the minecraft directory (/mods and /config)
remove_folder()

#Define a new directory inside the target directory to hold the copied files
source_dir = f"{raw_zip_filename}/mods"
target_dir = f"{user_folder_destination}"
new_dir = os.path.join(target_dir, os.path.basename(source_dir))
print(" ")
print("Copying files...")

#Copy the entire directory to the new directory
shutil.copytree(source_dir, new_dir)
shutil.rmtree(f"{raw_zip_filename}")
print(" ")
print("All downloaded mods have been installed successfully!")