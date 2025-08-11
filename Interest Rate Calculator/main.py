# Importing dependencies
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QTreeView, QMainWindow, QMessageBox, QFileDialog
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import os

class FinanceApp(QMainWindow):
    def __init__(self):
        super(FinanceApp, self).__init__()
        self.setWindowTitle('InterestUser')
        self.resize(800, 600)

        main_window = QWidget()

        self.rate_text = QLabel("Interest Rate (%): ")
        self.rate_input = QLineEdit()

        self.inital_text = QLabel("Initial Investment: ")
        self.inital_input = QLineEdit()

        self.years_text = QLabel("Years to Invest: ")
        self.years_input = QLineEdit()

        # Creating TreeView
        self.model = QStandardItemModel()
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.model)

        self.calc_button = QPushButton('Calculate')
        self.clear_button = QPushButton('Clear')
        self.save_button = QPushButton('Save Data')

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        self.master_layout = QVBoxLayout()
        self.row1 = QHBoxLayout()
        self.row2 = QHBoxLayout()
        self.col1 = QVBoxLayout()
        self.col2 = QVBoxLayout()

        self.row1.addWidget(self.rate_text)
        self.row1.addWidget(self.rate_input)
        self.row1.addWidget(self.inital_text)
        self.row1.addWidget(self.inital_input)
        self.row1.addWidget(self.years_text)
        self.row1.addWidget(self.years_input)

        self.col1.addWidget(self.tree_view)
        self.col1.addWidget(self.calc_button)
        self.col1.addWidget(self.clear_button)
        self.col1.addWidget(self.save_button)

        self.col2.addWidget(self.canvas)

        self.row2.addLayout(self.col1, 30)
        self.row2.addLayout(self.col2, 70)

        self.master_layout.addLayout(self.row1)
        self.master_layout.addLayout(self.row2)

        main_window.setLayout(self.master_layout)
        self.setCentralWidget(main_window)

        self.calc_button.clicked.connect(self.calc_interest)
        self.clear_button.clicked.connect(self.reset)
        self.save_button.clicked.connect(self.save_data)

    def calc_interest(self):
        initial_investment = None
        try:
            interest_rate = float(self.rate_input.text())
            initial_investment = float(self.inital_input.text())
            years = int(self.years_input.text())
        except ValueError:
            QMessageBox.warning(self, 'Error', 'Please enter valid numbers')
            return
        
        total = initial_investment
        for year in range(1, years + 1):
            total += total * (interest_rate / 100)
            item_year = QStandardItem(f'Year {year}')
            item_total = QStandardItem(f'${total:.2f}')
            self.model.appendRow([item_year, item_total])
        
        self.figure.clear()
        ax = self.figure.subplots()
        years = list(range(1, years + 1))
        totals = [initial_investment * (1 + interest_rate / 100) ** year for year in years]

        ax.plot(years, totals)
        ax.set_xlabel('Years')
        ax.set_ylabel('Total')
        ax.set_title('Interest Over Time')
        self.canvas.draw()

    def save_data(self):
        dir_path = QFileDialog.getExistingDirectory(self, 'Select Directory')
        if dir_path:
            folder_path = os.path.join(dir_path, 'Saved data')
            os.makedirs(folder_path, exist_ok=True)
    
            file_path = os.path.join(folder_path, 'results_data.csv')
            with open(file_path, 'w') as file:
                file.write('Year,Total\n')  # Fixed: single string argument
                for row in range(self.model.rowCount()):
                    year = self.model.item(row, 0).text()
                    total = self.model.item(row, 1).text()
                    file.write(f'{year},{total}\n')
            
            # Save graph to the selected directory
            self.figure.savefig(os.path.join(folder_path, "graph.png"))
            
            QMessageBox.information(self, 'Success', 'Data was saved successfully!')
        else:
            QMessageBox.warning(self, 'Save Results', 'Please select a directory')

    def reset(self):
        self.rate_input.clear()
        self.inital_input.clear()
        self.years_input.clear()
        self.model.clear()

if __name__ == '__main__':
    app = QApplication([])
    window = FinanceApp()
    window.show()
    app.exec_()