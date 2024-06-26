import requests
from tkinter import Tk, filedialog
from PIL import Image
import tempfile
import uuid
import os
from dotenv import load_dotenv
from tqdm import tqdm
import atexit

load_dotenv()
api_key = os.getenv('API_KEY')

def cleanup_temp_files(temp_file_path):
    """Cleanup function to remove temporary files."""
    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)

def remove_background(image_path, api_key):
    """Remove the background from an image using the remove.bg API."""
    url = 'https://api.remove.bg/v1.0/removebg'
    with open(image_path, 'rb') as image_file:
        files = {'image_file': image_file}
        data = {'size': 'auto'}
        
        print("Removing background...")
        with tqdm(total=100, position=0, leave=True) as pbar:
            response = requests.post(url, files=files, data=data, headers={'X-Api-Key': api_key})
            pbar.update(100)

    if response.status_code == requests.codes.ok:
        temp_fd, temp_file_path = tempfile.mkstemp(suffix='.png')
        atexit.register(cleanup_temp_files, temp_file_path)  # Register cleanup function
        with open(temp_fd, 'wb') as temp_file:
            temp_file.write(response.content)
        
        print('Background removed successfully!')
        return temp_file_path
    else:
        print(f'Error: {response.status_code}')
        print(response.text)
        return None

def add_flag(removed_bg_path, flag_path, stretch):
    """Overlay a flag image on top of a background-removed image."""
    try:
        print("Processing images...")
        removed_bg_image = Image.open(removed_bg_path).convert("RGBA")
        flag_image = Image.open(flag_path).convert("RGBA")

        with tqdm(total=100, position=0, leave=True) as pbar:
            if stretch:
                flag_image = flag_image.resize(removed_bg_image.size, Image.LANCZOS)
                pbar.update(50)
            else:
                flag_image.thumbnail(removed_bg_image.size, Image.LANCZOS)
                pbar.update(50)
                x = (removed_bg_image.width - flag_image.width) // 2
                y = (removed_bg_image.height - flag_image.height) // 2
                new_flag_image = Image.new("RGBA", removed_bg_image.size)
                new_flag_image.paste(flag_image, (x, y))
                flag_image = new_flag_image
            
            combined_image = Image.alpha_composite(flag_image, removed_bg_image)
            pbar.update(50)

        suggested_filename = f'output_{uuid.uuid4()}.png'
        save_path = filedialog.asksaveasfilename(defaultextension=".png", initialfile=suggested_filename,
                                                filetypes=[("PNG files", "*.png")])
        
        if save_path:
            try:
                combined_image.save(save_path, format="PNG")
                print(f'Image saved to {save_path}')
            except Exception as save_err:
                print(f'Error saving image: {save_err}')
        else:
            print('Save operation canceled.')

    except (FileNotFoundError, PIL.Image.DecompressionBombError, OSError) as e:
        print(f'Error processing images: {e}')
    except Exception as e:
        print(f'Unexpected error adding flag: {e}')

def get_flag_choice():
    """Prompt the user to select a flag."""
    print("\nChoose the flag:")
    print("1. Gay")
    print("2. Bisexual")
    print("3. Transgender")
    print("4. Lesbian")
    print("5. Asexual")
    print("6. Pansexual")
    print("7. Custom")

    flag_files = {
        '1': 'flags/gay.png',
        '2': 'flags/bisexual.png',
        '3': 'flags/transgender.png',
        '4': 'flags/lesbian.png',
        '5': 'flags/asexual.png',
        '6': 'flags/pansexual.png'
    }

    while True:
        choice = input("Choose an option (1-7): ")

        if choice in flag_files:
            return flag_files[choice]
        elif choice == '7':
            flag_path = filedialog.askopenfilename(title="Select a flag image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
            if flag_path:
                return flag_path
        else:
            print("Invalid choice. Please try again.")

def main():
    """Main function to execute the script."""
    root = Tk()
    root.withdraw()

    print("Choose image:")
    file_path = filedialog.askopenfilename(title="Select an image file", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        confirm = input(f"Do you want to remove the background from '{os.path.basename(file_path)}'? (yes/no): ")
        if confirm.lower() == 'yes':
            no_bg_path = remove_background(file_path, api_key)
            if no_bg_path:
                flag_path = get_flag_choice()
                if flag_path:
                    stretch_choice = input("Do you want the flag to stretch (s) or cover (c) the background? (s/c): ")
                    stretch = stretch_choice.lower() == 's'
                    add_flag(no_bg_path, flag_path, stretch)
                else:
                    print("No flag image selected.")
        else:
            flag_path = get_flag_choice()
            if flag_path:
                stretch_choice = input("Do you want the flag to stretch (s) or cover (c) the background? (s/c): ")
                stretch = stretch_choice.lower() == 's'
                add_flag(file_path, flag_path, stretch)
            else:
                print("No flag image selected.")
    else:
        print("No file selected.")

if __name__ == "__main__":
    main()
