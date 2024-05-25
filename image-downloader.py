import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import requests
import os


def create_folder(folder_path):
    try:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Folder created successfully: {folder_path}")
        else:
            print(f"The folder {folder_path} already exists.")
    except Exception as e:
        print(f"An error occurred while creating the folder: {e}")


def download_image(url, file_path):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(file_path, 'wb') as file:
                file.write(response.content)
            print(f"Image successfully downloaded: {file_path}")
        else:
            print(f"Failed to retrieve the image. HTTP Status Code: {
                  response.status_code}")
    except Exception as e:
        print(f"An error occurred while downloading the image: {e}")


class ImageDownloaderApp(toga.App):

    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=10))

        self.num_images_input = toga.TextInput(
            placeholder='Number of Images', style=Pack(flex=1))
        self.width_input = toga.TextInput(
            placeholder='Width', style=Pack(flex=1))
        self.height_input = toga.TextInput(
            placeholder='Height', style=Pack(flex=1))

        self.download_button = toga.Button(
            'Download Images', on_press=self.start_download, style=Pack(padding=10))

        main_box.add(self.num_images_input)
        main_box.add(self.width_input)
        main_box.add(self.height_input)
        main_box.add(self.download_button)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def start_download(self, widget):
        try:
            no = int(self.num_images_input.value)
            sizex = int(self.width_input.value)
            sizey = int(self.height_input.value)
            direc = f"{sizex}x{sizey}"

            target_folder = os.path.join("stockimages", direc)
            create_folder(target_folder)

            for i in range(no):
                image_url = f"https://picsum.photos/{sizex}/{sizey}"
                save_path = os.path.join(target_folder, f"downloaded_{
                                         i + 1}_image_{direc}.jpg")
                download_image(image_url, save_path)

            self.show_message("Success", f"Downloaded {
                              no} images of size {sizex}x{sizey}")
        except ValueError:
            self.show_message(
                "Input Error", "Please enter valid numerical values for dimensions and number of images.")

    def show_message(self, title, message):
        toga.Alert(message, title=title, app=self).show()


def main():
    return ImageDownloaderApp('Image Downloader', 'org.beeware.imagedownloader')


if __name__ == '__main__':
    main().main_loop()
