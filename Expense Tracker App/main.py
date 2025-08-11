# Importing Dependencies
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import (QApplication, QWidget, QLineEdit, QPushButton, 
                            QVBoxLayout, QHBoxLayout, QGridLayout, QComboBox, 
                            QDateEdit, QTableWidget, QLabel, QMessageBox,
                            QTableWidgetItem, QHeaderView)
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
import sys

# App class
class ExpenseApp(QWidget):
    def __init__(self):
        """Initialize the main window of the application"""
        super().__init__()
        
        # Set the size of the window (width, height)
        self.resize(800, 600)  # Set the size of the window
        self.setWindowTitle('Expense Tracker App')  # Set the title of the window

        # Create GUI elements
        self.date_box = QDateEdit()
        self.date_box.setDate(QDate.currentDate())
        self.dropdown = QComboBox()
        self.amount = QLineEdit()
        self.description = QLineEdit()

        self.add_button = QPushButton('Add Expense')
        self.delete_button = QPushButton('Remove Expense')

        self.table = QTableWidget()
        self.table.setColumnCount(5)  # Create columns for the table
        self.table.setHorizontalHeaderLabels(['ID', 'Date', 'Category', 'Amount', 'Description'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.sortByColumn(1, Qt.DescendingOrder)

        # Design the layout
        self.dropdown.addItems(['Food', 'Transport', 'Entertainment', 'Other', 'Utilities'])

        self.setStyleSheet("""
            QWidget {background-color: #91C8E4;}
            QLabel {color: #333;
                    font-size: 14px;}
            QLineEdit, QComboBox, QDateEdit {
                background-color: #91C8E4;
                color: #333;
                border: 1px solid #444;
                padding: 5px;
            }
            QTableWidget {
                background-color: #91C8E4;
                color: #333;
                border: 1px solid #444;
                selection-background-color: #ddd;
            }
            QPushButton {
                background-color: #4caf50;
                color: #fff;
                border: none;
                padding: 8px 16px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
                           """)

        self.master_layout = QVBoxLayout()
        self.row1 = QHBoxLayout()
        self.row2 = QHBoxLayout()
        self.row3 = QHBoxLayout()

        self.row1.addWidget(QLabel("Date: "))  # Add a label for the date
        self.row1.addWidget(self.date_box)  # Add a date picker
        self.row1.addWidget(QLabel("Category: "))  # Add a label for the category
        self.row1.addWidget(self.dropdown)  # Add a dropdown for selecting the category

        self.row2.addWidget(QLabel("Amount: "))  # Add a label for the amount
        self.row2.addWidget(self.amount)  # Add a text box for entering the amount
        self.row2.addWidget(QLabel("Description: "))  # Add a label for the description
        self.row2.addWidget(self.description)  # Add a text box for entering the description

        self.row3.addWidget(self.add_button)  # Add a button for adding an expense
        self.row3.addWidget(self.delete_button)  # Add a button for deleting an expense

        self.master_layout.addLayout(self.row1)  # Add the first row to the layout
        self.master_layout.addLayout(self.row2)  # Add the second row to the layout
        self.master_layout.addLayout(self.row3)  # Add the third row to the layout
        self.master_layout.addWidget(self.table)  # Add the table to the layout

        self.setLayout(self.master_layout)  # Set the layout of the window
        
        self.load_table()

        self.add_button.clicked.connect(self.add_expense)
        self.delete_button.clicked.connect(self.delete_expense)


    def load_table(self):
        self.table.setRowCount(0)

        query = QSqlQuery("SELECT * FROM expenses")
        row = 0
        while query.next():
            expense_id = query.value(0)
            date = query.value(1)
            category = query.value(2)
            amount = query.value(3)
            description = query.value(4)

            # Add values to table
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(expense_id)))
            self.table.setItem(row, 1, QTableWidgetItem(date))
            self.table.setItem(row, 2, QTableWidgetItem(category))
            self.table.setItem(row, 3, QTableWidgetItem(str(amount)))
            self.table.setItem(row, 4, QTableWidgetItem(description))

            row += 1
    
    def add_expense(self):
        date = self.date_box.date().toString('yyyy-MM-dd')
        category = self.dropdown.currentText()
        amount = self.amount.text()
        description = self.description.text()

        query = QSqlQuery()
        query.prepare("""
            INSERT INTO expenses (date, category, amount, description)
            VALUES (?, ?, ?, ?)
            """)

        query.addBindValue(date)
        query.addBindValue(category)
        query.addBindValue(amount)
        query.addBindValue(description)
        query.exec_()
        
        self.date_box.setDate(QDate.currentDate())
        self.dropdown.setCurrentIndex(0)
        self.amount.clear()
        self.description.clear()

        self.load_table()

    def delete_expense(self):
        selected = self.table.currentRow()
        if selected >= 0:
            expense_id = self.table.item(selected, 0).text()
            confirm = QMessageBox.question(self, 'Delete Expense', 'Are you sure you want to delete this expense?', QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.No:
                return 'Canceled'
            else:
                query = QSqlQuery()
                query.prepare("DELETE FROM expenses WHERE id = ?")
                query.addBindValue(expense_id)
                query.exec_()
                self.load_table()
                return 'Success'
        if selected == -1:
            QMessageBox.warning(self, 'Warning', 'Please select an expense to delete')


# Create a database
database = QSqlDatabase.addDatabase("QSQLITE")
database.setDatabaseName('expense.db')
if not database.open():
    QMessageBox.critical(None, 'Error', 'Could not open the database')
    sys.exit(1)

# Setup the database, structurizing it
query = QSqlQuery()
query.exec_("""
CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                category TEXT,
                amount REAL,
                description TEXT
            )
""")



if __name__ == '__main__':
    app = QApplication([])
    main_window = ExpenseApp()
    main_window.show()
    app.exec_()