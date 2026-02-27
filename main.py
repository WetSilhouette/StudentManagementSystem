from idlelib.search import SearchDialog

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget, QGridLayout, QLineEdit,
                             QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, QDialogButtonBox,
                             QComboBox, QToolBar, QStatusBar, QVBoxLayout, QMessageBox)
import sys
import sqlite3

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(1000, 600)

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        add_student_action = QAction(QIcon("icons/add.png"), "Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)
        about_action.triggered.connect(self.about)

        search_student_action = QAction(QIcon("icons/search.png"), "Search Student", self)
        search_student_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_student_action)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['id', 'Name', 'Course', 'Mobile'])
        self.table.verticalHeader().hide()
        self.setCentralWidget(self.table)

        toolbar = QToolBar()
        toolbar.setMovable(True)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_student_action)
        self.addToolBar(toolbar)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Detect cell selection
        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.status_bar.removeWidget(child)

        self.status_bar.addWidget(edit_button)
        self.status_bar.addWidget(delete_button)
    def load_data(self):
        connection = sqlite3.connect('database.db')
        result = connection.execute("SELECT * FROM students")
        rows = result.fetchall()
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))
        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        dialog = SearchDialog()
        dialog.exec()

    def edit(self, row):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()

    def about(self):
        dialog = AboutDialog()
        dialog.exec()


class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        layout = QVBoxLayout()
        about_label = QLabel("This app was created to manage your school's student data.")
        about_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        about_label.setWordWrap(True)
        layout.addWidget(about_label)
        rows_label = QLabel(f"This table contains {window.table.rowCount()} rows.")
        layout.addWidget(rows_label)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button_box.accepted.connect(self.accept)
        layout.addWidget(button_box)
        self.setLayout(layout)


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Student Data")
        self.setFixedWidth(350)
        self.setFixedHeight(300)
        grid = QGridLayout()

        index = window.table.currentRow()
        self.student_id = window.table.item(index, 0).text()

        warning_label = QLabel("Are you sure you want to delete this record?")
        warning_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.accept)

        grid.addWidget(warning_label, 0, 0, 1, 2)
        grid.addWidget(delete_button, 1, 0, 1, 2)

        self.setLayout(grid)

    def accept(self):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("DELETE FROM students WHERE id=?", (self.student_id,))
        connection.commit()
        cursor.close()
        connection.close()
        window.load_data()
        self.close()


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edit Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        grid = QGridLayout()

        index = window.table.currentRow()
        student_name = window.table.item(index, 1).text()
        student_course = window.table.item(index, 2).text()
        student_mobile = window.table.item(index, 3).text()
        self.student_id = window.table.item(index, 0).text()

        name_label = QLabel("Name:")
        self.name_line_edit = QLineEdit()
        self.name_line_edit.setPlaceholderText(student_name)

        course_label = QLabel("Course:")
        self.course_line_edit = QComboBox()
        self.course_line_edit.addItems(["Math", "Physics", "Chemistry", "Biology",
                                        "Computer Science", "English", "History", "Astronomy"])
        self.course_line_edit.setCurrentText(student_course)

        mobile_label = QLabel("Mobile:")
        self.mobile_line_edit = QLineEdit()
        self.mobile_line_edit.setPlaceholderText(student_mobile)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        grid.addWidget(name_label, 0, 0)
        grid.addWidget(self.name_line_edit, 0, 1)
        grid.addWidget(course_label, 1, 0)
        grid.addWidget(self.course_line_edit, 1, 1)
        grid.addWidget(mobile_label, 2, 0)
        grid.addWidget(self.mobile_line_edit, 2, 1)
        grid.addWidget(button_box, 3, 0, 1, 2)

        self.setLayout(grid)

    def accept(self):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        name = self.name_line_edit.text() or self.name_line_edit.placeholderText()
        course = self.course_line_edit.currentText()
        mobile = self.mobile_line_edit.text() or self.mobile_line_edit.placeholderText()
        cursor.execute("UPDATE students SET name=?, course=?, mobile=? WHERE id=?",
                       (name, course, mobile, self.student_id))
        connection.commit()
        cursor.close()
        connection.close()
        window.load_data()
        self.close()

class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        grid = QGridLayout()

        name_label = QLabel("Name:")
        self.name_line_edit = QLineEdit()

        course_label = QLabel("Course:")
        self.course_line_edit = QComboBox()
        self.course_line_edit.addItems(["Math", "Physics", "Chemistry", "Biology",
                                        "Computer Science", "English", "History", "Astronomy"])
        mobile_label = QLabel("Mobile:")
        self.mobile_line_edit = QLineEdit()

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        grid.addWidget(name_label, 0, 0)
        grid.addWidget(self.name_line_edit, 0, 1)
        grid.addWidget(course_label, 1, 0)
        grid.addWidget(self.course_line_edit, 1, 1)
        grid.addWidget(mobile_label, 2, 0)
        grid.addWidget(self.mobile_line_edit, 2, 1)
        grid.addWidget(button_box, 3, 0, 1, 2)

        self.setLayout(grid)

    def accept(self):
        name = self.name_line_edit.text()
        course = self.course_line_edit.currentText()
        mobile = self.mobile_line_edit.text()
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",
                       (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        window.load_data()
        self.close()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        grid = QGridLayout()

        name_label = QLabel("Name:")
        self.name_line_edit = QLineEdit()

        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search)

        grid.addWidget(name_label, 0, 0)
        grid.addWidget(self.name_line_edit, 0, 1)
        grid.addWidget(search_button, 1, 0, 1, 2)

        self.setLayout(grid)

    def search(self):
        name = self.name_line_edit.text().strip().lower()
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students WHERE name=?", (name,))
        rows = result.fetchall()
        print(rows)
        items = window.table.findItems(name, Qt.MatchFlag.MatchExactly)
        for item in items:
            print(item.row(), item.column())
            window.table.item(item.row(), item.column()).setSelected(True)
        cursor.close()
        connection.close()
        self.close()


app = QApplication(sys.argv)
window = MainWindow()
window.load_data()
window.show()
sys.exit(app.exec())


