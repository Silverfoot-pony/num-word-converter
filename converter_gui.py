""" 
Quick converter for string numbers in words to ints and vice versa. In QT6.
Copyright (C) 2026  Silverfoot

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QPushButton, QRadioButton, QGroupBox, QMessageBox
)
from PyQt6.QtCore import Qt
from word2number import w2n
from num2words import num2words

class ConverterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize the GUI layout."""
        self.setWindowTitle("Num-Word Converter")
        self.resize(400, 350)
        
        # Set background to match the general theme slightly if possible, 
        # though Qt handles this automatically based on the theme
        self.setStyleSheet("QGroupBox { font-weight: bold; border: 1px solid #ccc; border-radius: 5px; margin-top: 10px; } QLabel { font-size: 14px; } QLineEdit { padding: 5px; } QPushButton { padding: 5px; min-width: 80px; }")

        layout = QVBoxLayout()

        # --- Mode Selection ---
        mode_group = QGroupBox("Conversion Mode")
        mode_layout = QVBoxLayout()
        
        self.radio_words = QRadioButton("Text (Words) -> Number")
        self.radio_number = QRadioButton("Number -> Text (Words)")
        
        self.radio_words.setChecked(True) # Default selection
        self.radio_words.toggled.connect(self.toggle_input_hint)

        mode_layout.addWidget(self.radio_words)
        mode_layout.addWidget(self.radio_number)
        mode_group.setLayout(mode_layout)
        layout.addWidget(mode_group)

        # --- Input Area ---
        layout.addWidget(QLabel("Input:"))
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type here...")
        layout.addWidget(self.input_field)

        # --- Action Area ---
        self.convert_btn = QPushButton("Convert")
        self.convert_btn.clicked.connect(self.perform_conversion)
        layout.addWidget(self.convert_btn)

        # --- Output Area ---
        layout.addWidget(QLabel("Output:"))
        self.output_field = QLineEdit()
        self.output_field.setReadOnly(True) # Output is read-only
        layout.addWidget(self.output_field)

        self.setLayout(layout)
        self.toggle_input_hint()

    def toggle_input_hint(self):
        """Update placeholder text based on selected mode."""
        if self.radio_words.isChecked():
            self.input_field.setPlaceholderText("e.g. 'one hundred twenty-three'")
        else:
            self.input_field.setPlaceholderText("e.g. '123'")

    def perform_conversion(self):
        """Handle the button click logic."""
        text = self.input_field.text().strip()
        
        if not text:
            QMessageBox.warning(self, "Input Error", "Please enter some text or a number.")
            return

        try:
            result = ""
            if self.radio_words.isChecked():
                # Text to Number
                try:
                    result = w2n.word_to_num(text)
                except w2n.w2n_errors.WordNotDigitError:
                    result = "Error: Invalid text format."
            else:
                # Number to Text
                try:
                    result = num2words(int(text))
                except ValueError:
                    result = "Error: Not a valid integer."
            
            self.output_field.setText(str(result))
            
        except Exception as e:
            self.output_field.setText("Error: " + str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Use a nice font for the app to look native
    font = app.font()
    font.setPointSize(10)
    app.setFont(font)
    
    window = ConverterWindow()
    window.show()
    sys.exit(app.exec())
