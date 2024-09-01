import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QFileDialog, QMessageBox, \
    QHBoxLayout, QLineEdit
from PyQt5.QtGui import QIcon, QFont, QTextCursor, QTextCharFormat, QColor


class TextEditorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Text File Editor')
        self.setGeometry(100, 100, 800, 600)  # Set the window size

        # Set a stylesheet for the window
        self.setStyleSheet("""
            QWidget {
                background-color: #2c3e50;
                color: #ecf0f1;
            }
            QPushButton {
                background-color: #2980b9;
                color: white;
                border-radius: 10px;
                padding: 15px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #3498db;
            }
            QTextEdit {
                background-color: #34495e;
                border: 2px solid #2980b9;
                color: white;
                font-family: 'Courier New', monospace;
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
            }
            QLineEdit {
                background-color: #ecf0f1;
                border: 2px solid #2980b9;
                color: #2c3e50;
                font-size: 14px;
                padding: 5px;
                border-radius: 5px;
            }
        """)

        # Main layout
        main_layout = QVBoxLayout()

        # Create a text area for displaying and editing the file content
        self.text_area = QTextEdit(self)
        main_layout.addWidget(self.text_area)

        # Connect the text area's textChanged signal to a slot that checks if the text is empty
        self.text_area.textChanged.connect(self.check_text)

        # Add a search bar on top of the text area
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search...")
        search_layout.addWidget(self.search_input)

        # Search button to search in the text area
        search_button = QPushButton('Search')
        search_button.clicked.connect(self.search_text)
        search_layout.addWidget(search_button)

        main_layout.addLayout(search_layout)

        # Button layout at the bottom
        button_layout = QHBoxLayout()

        # Button to upload a file with an icon
        self.upload_button = QPushButton(' Upload Text File')
        self.upload_button.setIcon(QIcon('upload_icon.png'))  # Add an icon here if you have one
        self.upload_button.setFont(QFont('Arial', 12))
        self.upload_button.clicked.connect(self.upload_file)
        button_layout.addWidget(self.upload_button)

        # Button to save and export the modified content with an icon
        self.save_button = QPushButton(' Save and Export')
        self.save_button.setIcon(QIcon('save_icon.png'))  # Add an icon here if you have one
        self.save_button.setFont(QFont('Arial', 12))
        self.save_button.clicked.connect(self.save_file)
        self.save_button.setEnabled(False)  # Initially disable the save button
        button_layout.addWidget(self.save_button)

        main_layout.addLayout(button_layout)

        # Set the main layout for the window
        self.setLayout(main_layout)

    def upload_file(self):
        # Open a file dialog to select a text file
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open Text File', '', 'Text Files (*.txt)')

        if file_name:
            try:
                with open(file_name, 'r') as file:
                    content = file.read()
                    self.text_area.setText(content)
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Could not open file: {e}')

    def save_file(self):
        # Open a file dialog to select where to save the modified file
        file_name, _ = QFileDialog.getSaveFileName(self, 'Save File', '', 'Text Files (*.txt)')

        if file_name:
            try:
                content = self.text_area.toPlainText()
                with open(file_name, 'w') as file:
                    file.write(content)
                QMessageBox.information(self, 'Success', 'File saved successfully')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Could not save file: {e}')

    def check_text(self):
        # Enable or disable the save button based on whether there is text in the text area
        if self.text_area.toPlainText().strip():
            self.save_button.setEnabled(True)
        else:
            self.save_button.setEnabled(False)

    def search_text(self):
        search_term = self.search_input.text()
        text = self.text_area.toPlainText()

        # Clear previous selections
        self.text_area.moveCursor(QTextCursor.Start)
        self.text_area.setExtraSelections([])

        if search_term:
            cursor = self.text_area.textCursor()
            format = QTextCharFormat()
            format.setBackground(QColor("yellow"))  # Highlight with yellow color

            while True:
                cursor = self.text_area.document().find(search_term, cursor)
                if cursor.isNull():
                    break

                # Select the found text and apply the format
                cursor.mergeCharFormat(format)
                self.text_area.setTextCursor(cursor)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = TextEditorApp()
    editor.show()
    sys.exit(app.exec_())
