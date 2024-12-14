from aqt.qt import *
from typing import Optional

from . import api_call

from prompts import BASE_PROMPT


class TextInputDialog(QDialog):
    def __init__(self, parent: Optional[QWidget]):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Enter Additional Instructions")
        layout = QVBoxLayout()
        
        # Text input area
        self.text_input = QTextEdit()
        layout.addWidget(self.text_input)
        
        # Submit button
        submit_btn = QPushButton("Submit")
        submit_btn.clicked.connect(self.accept)
        layout.addWidget(submit_btn)
        
        self.setLayout(layout)
        
    def get_text(self):
        return self.text_input.toPlainText()

class ExampleDialog(QDialog):
    def __init__(self, parent: Optional[QWidget], text1: str, text2: str, editor):
        super().__init__(parent)
        self.editor = editor
        self.text1 = text1
        self.text2 = text2
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Example Preview")
        layout = QVBoxLayout()
        
        # First text section
        label1 = QLabel("Field 1:")
        self.text_display1 = QTextEdit()
        self.text_display1.setPlainText(self.text1)
        self.text_display1.setReadOnly(True)
        layout.addWidget(label1)
        layout.addWidget(self.text_display1)
        
        # Second text section
        label2 = QLabel("Field 2:")
        self.text_display2 = QTextEdit()
        self.text_display2.setPlainText(self.text2)
        self.text_display2.setReadOnly(True)
        layout.addWidget(label2)
        layout.addWidget(self.text_display2)
        
        # Buttons
        button_box = QHBoxLayout()
        accept_btn = QPushButton("Accept")
        reject_btn = QPushButton("Reject")
        further_btn = QPushButton("Further Changes")
        
        accept_btn.clicked.connect(self.accept)
        reject_btn.clicked.connect(self.reject)
        further_btn.clicked.connect(self.on_further_changes)
        
        button_box.addWidget(accept_btn)
        button_box.addWidget(reject_btn)
        button_box.addWidget(further_btn)
        layout.addLayout(button_box)
        
        self.setLayout(layout)
    def on_further_changes(self):
        text_dialog = TextInputDialog(self)
        if text_dialog.exec():
            user_input = text_dialog.get_text()
            
            # Get new suggestions from Claude
            new_text1, new_text2 = api_call.get_suggestions_from_claude(
                {BASE_PROMPT}
                user_input, 
                self.text1, 
                self.text2
            )
            
            # Update display with new suggestions
            self.text1 = new_text1
            self.text2 = new_text2
            self.text_display1.setPlainText(self.text1)
            self.text_display2.setPlainText(self.text2)

class CustomInstructionDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()
        self.prompt = ""
        
    def setup_ui(self):
        self.setWindowTitle("Custom Instruction")
        layout = QVBoxLayout()
        
        # Instruction field
        self.instruction_input = QTextEdit()
        self.instruction_input.setPlaceholderText("Enter your instructions for improving the flashcard...")
        layout.addWidget(self.instruction_input)
        
        # Submit button
        submit_btn = QPushButton("Submit")
        submit_btn.clicked.connect(self.on_submit)
        layout.addWidget(submit_btn)
        
        self.setLayout(layout)
        
    def on_submit(self):
        self.prompt = self.instruction_input.toPlainText()
        self.accept()



