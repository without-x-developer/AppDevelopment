# Importing dependencies
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QListWidget, QFileDialog
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageFilter, ImageEnhance

# App Settings
app = QApplication([])
main_window = QWidget()
main_window.setWindowTitle('Image Editing App')
main_window.resize(900, 700)

# All app objects and widgets
btn_folder = QPushButton('Folder')
file_list = QListWidget()

btn_left = QPushButton('<<')
btn_right = QPushButton('>>')
mirror = QPushButton('Mirror')
sharpness = QPushButton('Sharpness')
gray = QPushButton('B/W')
saturation = QPushButton('Color')
contrast = QPushButton('Contrast')
blur = QPushButton('Blur')

# Dropdown box
filter_box = QComboBox()
filter_box.addItems(['Original', 'Mirror', 'Sharpness', 'B/W', 'Color', 'Contrast', 'Blur'])

picture_box = QLabel("Image will appear here")
picture_box.setAlignment(Qt.AlignCenter) 
picture_box.setStyleSheet("border: 1px solid gray;")

# App design 
main_layout = QHBoxLayout()  

# Instrument panel
left_column = QVBoxLayout()
left_column.addWidget(btn_folder)
left_column.addWidget(file_list)
left_column.addWidget(filter_box)

# Navigation group buttons
nav_buttons = QHBoxLayout()
nav_buttons.addWidget(btn_left)
nav_buttons.addWidget(btn_right)
left_column.addLayout(nav_buttons)

# Filter group buttons
filter_buttons = QVBoxLayout()
filter_buttons.addWidget(mirror)
filter_buttons.addWidget(sharpness)
filter_buttons.addWidget(gray)
filter_buttons.addWidget(saturation)
filter_buttons.addWidget(contrast)
filter_buttons.addWidget(blur)
left_column.addLayout(filter_buttons)

# Picture box
right_column = QVBoxLayout()
right_column.addWidget(picture_box)

# Adding to main layout
main_layout.addLayout(left_column, 1) 
main_layout.addLayout(right_column, 4)

main_window.setLayout(main_layout)

# Adding functionality to our app
working_directory = ''
result = []

# Filter files and extensions
def filter_files(files, extensions):
    filtered = []
    for file in files:
        for ext in extensions:
            if file.lower().endswith(ext):
                filtered.append(file)
    return filtered

# Choose the current working directory
def get_working_directory():
    global working_directory
    # Using raw string to get the path
    working_directory = QFileDialog.getExistingDirectory()
    if working_directory:
        extensions = ['.jpg', '.png', '.jpeg', '.svg']
        filenames = filter_files(os.listdir(working_directory), extensions)
        file_list.clear()
        for filename in filenames:
            file_list.addItem(filename)

# Editor class
class Editor():
    def __init__(self):
        self.image = None
        self.original = None 
        self.filename = None
        self.save_folder = 'edits'  

    def load_image(self, filename):
        self.filename = filename
        # Using os.path.join for correct path making
        full_name = os.path.join(working_directory, filename)
        self.image = Image.open(full_name)
        self.original = self.image.copy()

    def save_image(self):
        # Full path to the directory
        save_path = os.path.join(working_directory, self.save_folder)
        
        # Create a directory if it does not exist
        if not os.path.exists(save_path):
            os.makedirs(save_path)
            
        # Forming the full path
        full_name = os.path.join(save_path, self.filename)
        self.image.save(full_name)
        return full_name

    def show_image(self, path):
        picture_box.hide()
        try:
            image = QPixmap(path)
            if not image.isNull():
                w, h = picture_box.width(), picture_box.height()
                image = image.scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                picture_box.setPixmap(image)
            else:
                picture_box.setText("Failed to load image")
        except Exception as e:
            picture_box.setText(f"Error: {str(e)}")
        picture_box.show()

    # def gray(self):
    #     if self.image:
    #         self.image = self.image.convert('L')
    #         saved_path = self.save_image()
    #         self.show_image(saved_path)
    
    # def mirror(self):
    #     if self.image:
    #         self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
    #         saved_path = self.save_image()
    #         self.show_image(saved_path)
    
    # def sharpness(self):
    #     if self.image:
    #         self.image = self.image.filter(ImageFilter.SHARPEN)
    #         saved_path = self.save_image()
    #         self.show_image(saved_path)
    
    # def saturation(self):
    #     if self.image:
    #         enhancer = ImageEnhance.Color(self.image)
    #         self.image = enhancer.enhance(2.0)
    #         saved_path = self.save_image()
    #         self.show_image(saved_path)
    
    # def contrast(self):
    #     if self.image:
    #         enhancer = ImageEnhance.Contrast(self.image)
    #         self.image = enhancer.enhance(2.0)
    #         saved_path = self.save_image()
    #         self.show_image(saved_path)
    
    # def blur(self):
    #     if self.image:
    #         self.image = self.image.filter(ImageFilter.BLUR)
    #         saved_path = self.save_image()
    #         self.show_image(saved_path)


    
    def reset(self):
        if self.original:
            self.image = self.original.copy()
            saved_path = self.save_image()
            self.show_image(saved_path)

    def transformImage(self, transformation):
        transformations = {
            'B/W': lambda image: image.convert('L'),
            'Mirror': lambda image: image.transpose(Image.FLIP_LEFT_RIGHT),
            'Blur': lambda image: image.filter(ImageFilter.GaussianBlur(radius=3)),
            'Sharpen': lambda image: image.filter(ImageFilter.SHARPEN),
            'Color': lambda image: ImageEnhance.Color(image).enhance(2.0),
            'Contrast': lambda image: ImageEnhance.Contrast(image).enhance(2.0),
            '<<': lambda image: image.transpose(Image.ROTATE_90),
            '>>': lambda image: image.transpose(Image.ROTATE_270),
            'Reset': self.reset
        }
        transform_function = transformations.get(transformation)
        if transform_function:
            self.image = transform_function(self.image)
            self.save_image()
        self.save_image()
        image_path = os.path.join(working_directory, self.save_folder, self.filename)
        self.show_image()
        

    def apply_filter(self, filter_name):
        if filter_name == 'Original':
            self.image = self.original.copy()
        else:
            mapping = {
                'B/W': lambda image: image.convert('L'),
                'Mirror': lambda image: image.transpose(Image.FLIP_LEFT_RIGHT),
                'Blur': lambda image: image.filter(ImageFilter.GaussianBlur(radius=3)),
                'Sharpen': lambda image: image.filter(ImageFilter.SHARPEN),
                'Color': lambda image: ImageEnhance.Color(image).enhance(2.0),
                'Contrast': lambda image: ImageEnhance.Contrast(image).enhance(2.0),
                '<<': lambda image: image.transpose(Image.ROTATE_90),
                '>>': lambda image: image.transpose(Image.ROTATE_270),
                'Reset': self.reset
            }

            filter_function = mapping.get(filter_name)
            if filter_function:
                self.image = filter_function(self.image)
                self.save_image()
                image_path = os.path.join(working_directory, self.save_folder, self.filename)
                self.show_image(image_path)
            pass

        self.save_image()
        image_path = os.path.join(working_directory, self.save_folder, self.filename)
        self.show_image(image_path)


def handle_filter():
    if file_list.currentRow() >= 0:
        selected_filter = filter_box.currentText()
        main.apply_filter(selected_filter)

# Display Image correctly
def displayImage():
    if file_list.currentRow() >= 0 and working_directory:
        filename = file_list.currentItem().text()
        main.load_image(filename)
        image_path = os.path.join(working_directory, filename)
        main.show_image(image_path)

# Object
main = Editor()

btn_folder.clicked.connect(get_working_directory)
file_list.currentRowChanged.connect(displayImage)

# Events - connecting all buttons
gray.clicked.connect(lambda: main.transformImage('B/W'))
mirror.clicked.connect(lambda: main.transformImage('Mirror'))
sharpness.clicked.connect(lambda: main.transformImage('Sharpen'))
saturation.clicked.connect(lambda: main.transformImage('Color'))
contrast.clicked.connect(lambda: main.transformImage('Contrast'))
blur.clicked.connect(lambda: main.transformImage('Blur'))

filter_box.currentTextChanged.connect(handle_filter)

# Executing App
main_window.show()
app.exec_()