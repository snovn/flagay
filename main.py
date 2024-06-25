import requests
from tkinter import Tk, filedialog
from PIL import Image
import tempfile
import uuid
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('API_KEY')


def remove_background(image_path, api_key):
    """Remove the background from an image using the remove.bg API."""
    url = 'https://api.remove.bg/v1.0/removebg'
    with open(image_path, 'rb') as image_file:
        files = {'image_file': image_file}
        data = {'size': 'auto'}
        response = requests.post(url, files=files, data=data, headers={'X-Api-Key': api_key})
        
    if response.status_code == requests.codes.ok:
        # Create a temporary file and write the response content to it
        temp_fd, temp_file_path = tempfile.mkstemp(suffix='.png')
        with open(temp_fd, 'wb') as temp_file:
            temp_file.write(response.content)
        
        print('Background removed successfully!')
        return temp_file_path
    else:
        print(f'Error: {response.status_code}')
        print(response.text)
        return None

def add_flag(removed_bg_path, flag_path):
    """Overlay a flag image on top of a background-removed image."""
    try:
        removed_bg_image = Image.open(removed_bg_path).convert("RGBA")
        flag_image = Image.open(flag_path).convert("RGBA")
        
        flag_image = flag_image.resize(removed_bg_image.size, Image.LANCZOS)
        combined_image = Image.alpha_composite(flag_image, removed_bg_image)
        
        # Generate a suggested filename with UUID
        suggested_filename = f'output_{uuid.uuid4()}.png'
        
        # Prompt the user to choose where to save the file
        save_path = filedialog.asksaveasfilename(defaultextension=".png", initialfile=suggested_filename,
                                                filetypes=[("PNG files", "*.png")])
        
        if save_path:
            combined_image.save(save_path, format="PNG")
            print(f'Image saved to {save_path}')
        else:
            print('Save operation canceled.')
        
    except Exception as e:
        print(f'Error adding flag: {e}')

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

    choice = input("Choose an option (1-7): ")

    if choice in flag_files:
        return flag_files[choice]
    elif choice == '7':
        return filedialog.askopenfilename(title="Select a flag image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    else:
        print("Invalid choice. Please try again.")
        return None

def main():
    """Main function to execute the script."""
    root = Tk()
    root.withdraw()

    print("Choose image:")
    file_path = filedialog.askopenfilename(title="Select an image file", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        # Ask user for confirmation before removing background
        confirm = input(f"Do you want to remove the background from '{os.path.basename(file_path)}'? (yes/no): ")
        if confirm.lower() == 'yes':
            no_bg_path = remove_background(file_path, api_key)
            if no_bg_path:
                flag_path = get_flag_choice()
                if flag_path:
                    add_flag(no_bg_path, flag_path)
                else:
                    print("No flag image selected.")
                # Clean up the temporary file
                if os.path.exists(no_bg_path):
                    os.remove(no_bg_path)
        else:
            flag_path = get_flag_choice()
            if flag_path:
                add_flag(file_path, flag_path)
            else:
                print("No flag image selected.")
    else:
        print("No file selected.")

if __name__ == "__main__":
    main()
