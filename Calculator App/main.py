# Importing dependencies
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QFont

class CalculatorApp(QWidget):
    def __init__(self):
        super().__init__()
        # Main App Settings
        self.setWindowTitle('Calculator App')
        self.resize(250, 300)

        # All objects/widgets
        self.text_box = QLineEdit()
        self.text_box.setFont(QFont('Helvetica', 20))
        self.grid = QGridLayout()
        self.buttons = ['7', '8', '9', '/', 
                        '4', '5', '6', '*', 
                        '1', '2', '3', '-', 
                        '0', '.', '=', '+']
        self.clear_btn = QPushButton('C')
        self.delete_btn = QPushButton('<--')    
        
        row = 0
        col = 0

        # Loop for creating buttons
        for text in self.buttons:
            button = QPushButton(text)
            button.clicked.connect(self.button_click)
            button.setStyleSheet("QPushButton {font-size: 25pt Comic Sans MS; padding: 10px}")
            self.grid.addWidget(button, row, col)
            col += 1
            if col == 4:
                col = 0
                row += 1
        
        # Design
        self.clear_btn.setStyleSheet("QPushButton {font-size: 25pt Comic Sans MS; padding: 10px}")
        self.delete_btn.setStyleSheet("QPushButton {font-size: 25pt Comic Sans MS; padding: 10px}")

        master_layout = QVBoxLayout()
        master_layout.addWidget(self.text_box)
        master_layout.addLayout(self.grid)
        
        button_row = QHBoxLayout()
        button_row.addWidget(self.clear_btn)
        button_row.addWidget(self.delete_btn)
        master_layout.addLayout(button_row)
        master_layout.setContentsMargins(25, 25, 25, 25)
        
        self.setLayout(master_layout)
        
        # Connect buttons
        self.clear_btn.clicked.connect(self.button_click)
        self.delete_btn.clicked.connect(self.button_click)

    # Events and functionality
    def button_click(self):
        button = self.sender()
        text = button.text()

        if text == '=':
            expression = self.text_box.text()
            try:
                result = eval(expression)
                self.text_box.setText(str(result))
            except Exception as e:
                self.text_box.setText('Error')
        
        elif text == 'C':
            self.text_box.clear()
        
        elif text == '<--':
            current_value = self.text_box.text()
            self.text_box.setText(current_value[:-1])
        
        else:
            current_value = self.text_box.text()
            self.text_box.setText(current_value + text)

# Show/Execute app
if __name__ == "__main__":
    app = QApplication([])
    main_window = CalculatorApp()
    main_window.setStyleSheet('QWidget {background-color: #f0f0f8}')
    main_window.show()
    app.exec_()