import sys
import re
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QFileDialog, QTextEdit, QMessageBox
)
from PyQt5.QtCore import Qt  # Import Qt from PyQt5.QtCore

class ChatFilterApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('WhatsApp Chat Filter')
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        # File selection layout
        file_layout = QHBoxLayout()
        self.file_label = QLabel('Chat file:')
        self.file_path = QLineEdit()
        self.file_path.setReadOnly(True)
        self.browse_button = QPushButton('Browse...')
        self.browse_button.clicked.connect(self.browse_file)
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.file_path)
        file_layout.addWidget(self.browse_button)
        layout.addLayout(file_layout)

        # Usernames input layout
        user_layout = QHBoxLayout()
        self.user_label = QLabel('Usernames (comma separated):')
        self.user_input = QLineEdit()
        user_layout.addWidget(self.user_label)
        user_layout.addWidget(self.user_input)
        layout.addLayout(user_layout)

        # Output display
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        layout.addWidget(self.output_text)

        # Filter and Save button
        self.filter_button = QPushButton('Filter and Save Messages')
        self.filter_button.clicked.connect(self.filter_and_save_messages)
        layout.addWidget(self.filter_button)

        # Copyright label
        self.copyright_label = QLabel('© 2024 by Ibnul')
        self.copyright_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.copyright_label)

        self.setLayout(layout)

    def browse_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open Chat File', '', 'Text Files (*.txt);;All Files (*)')
        if file_name:
            self.file_path.setText(file_name)

    def filter_and_save_messages(self):
        file_name = self.file_path.text()
        if not file_name:
            QMessageBox.warning(self, 'Error', 'Please select a chat file.')
            return

        user_names = self.user_input.text().split(',')
        user_names = [name.strip() for name in user_names if name.strip()]

        if not user_names:
            QMessageBox.warning(self, 'Error', 'Please enter at least one username.')
            return

        try:
            with open(file_name, 'r', encoding='utf-8') as file:
                chat_lines = file.readlines()

            user_messages = [line for line in chat_lines if any(user_name in line for user_name in user_names)]

            # Open a Save As dialog to specify the output file
            save_file_name, _ = QFileDialog.getSaveFileName(self, 'Save Filtered Messages As', '', 'Text Files (*.txt);;All Files (*)')
            if save_file_name:
                with open(save_file_name, "w", encoding="utf-8") as output_file:
                    output_file.writelines(user_messages)
                self.output_text.setText(''.join(user_messages))
                QMessageBox.information(self, 'Success', f'Messages from {", ".join(user_names)} have been exported to {save_file_name}')
            else:
                QMessageBox.warning(self, 'Error', 'No file selected to save messages.')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'An error occurred:\n{e}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ChatFilterApp()
    ex.show()
    sys.exit(app.exec_())
