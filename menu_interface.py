from aqt.qt import *
from . import utils

class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = utils.get_config()
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Anki-Copilot Configuration")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout()
        
        # API Key section
        api_group = QGroupBox("API Settings")
        api_layout = QVBoxLayout()
        
        # API Key input
        key_layout = QHBoxLayout()
        self.api_key = QLineEdit()
        self.api_key.setEchoMode(QLineEdit.EchoMode.Password)  # Fixed constant name
        self.api_key.setText(self.config.get('api_key', ''))
        self.api_key.setPlaceholderText("Enter your Anthropic API key")
        
        show_key = QPushButton("👁")
        show_key.setFixedWidth(30)
        show_key.clicked.connect(self.toggle_key_visibility)
        
        key_layout.addWidget(QLabel("API Key:"))
        key_layout.addWidget(self.api_key)
        key_layout.addWidget(show_key)
        
        api_layout.addLayout(key_layout)
        api_group.setLayout(api_layout)
        
        # Buttons
        button_box = QHBoxLayout()
        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")
        
        save_btn.clicked.connect(self.save_config)
        cancel_btn.clicked.connect(self.reject)
        
        button_box.addStretch()
        button_box.addWidget(save_btn)
        button_box.addWidget(cancel_btn)
        
        layout.addWidget(api_group)
        layout.addStretch()
        layout.addLayout(button_box)
        
        self.setLayout(layout)
    
    def toggle_key_visibility(self):
        if self.api_key.echoMode() == QLineEdit.EchoMode.Password:
            self.api_key.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.api_key.setEchoMode(QLineEdit.EchoMode.Password)
            
    def save_config(self):
        self.config['api_key'] = self.api_key.text()
        utils.save_config(self.config)
        self.accept()