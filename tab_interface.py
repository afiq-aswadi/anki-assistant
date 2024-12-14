from aqt.qt import *
from typing import Optional

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
            # Generate new suggestions based on user input
            self.text1 = f"New Field 1: Based on '{user_input}'"
            self.text2 = f"New Field 2: Modified with '{user_input}'"
            
            # Update display with new suggestions
            self.text_display1.setPlainText(self.text1)
            self.text_display2.setPlainText(self.text2)
            
            # Dialog stays open for another accept/reject cycle
    


