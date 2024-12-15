from aqt.qt import *
from . import utils

class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = utils.get_config()
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Anki-Assistant Configuration")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # API Key section
        api_group = QGroupBox("API Settings") 
        api_layout = QVBoxLayout() 
        
        # API Key input
        key_layout = QHBoxLayout()
        self.api_key = QLineEdit()
        self.api_key.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key.setText(self.config.get('api_key', ''))
        self.api_key.setPlaceholderText("Enter your Anthropic API key")
        
        show_key = QPushButton("👁")
        show_key.setFixedWidth(30)
        show_key.clicked.connect(self.toggle_key_visibility)
        
        key_layout.addWidget(QLabel("API Key:"))
        key_layout.addWidget(self.api_key)
        key_layout.addWidget(show_key)
        
        # Model selection
        model_layout = QHBoxLayout()
        self.model_select = QComboBox()
        models = ["claude-3-5-sonnet-latest (Most Powerful)", "claude-3-5-haiku-latest (Lightweight)", "claude-3-opus-20240229 (Older, Cheaper)"]
        self.model_select.addItems(models)
        current_model = self.config.get('model_id', 'claude-3-sonnet-20240229')
        self.model_select.setCurrentText(current_model)
        
        model_layout.addWidget(QLabel("Model:"))
        model_layout.addWidget(self.model_select)
        
        # Temperature slider
        temp_layout = QHBoxLayout()
        self.temp_slider = QSlider()
        self.temp_slider.setOrientation(Qt.Orientation.Horizontal)
        self.temp_slider.setMinimum(0)
        self.temp_slider.setMaximum(100)
        self.temp_slider.setValue(int(self.config.get('temperature', 0.7) * 100))
        
        self.temp_label = QLabel(f"Temperature: {self.temp_slider.value()/100:.2f}")
        self.temp_slider.valueChanged.connect(self.update_temp_label)
        
        temp_layout.addWidget(self.temp_label)
        temp_layout.addWidget(self.temp_slider)
        
        # Add all to API layout
        api_layout.addLayout(key_layout)
        api_layout.addLayout(model_layout)
        api_layout.addLayout(temp_layout)
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
    
    def update_temp_label(self):
        self.temp_label.setText(f"Temperature: {self.temp_slider.value()/100:.2f}")
    
    def toggle_key_visibility(self):
        if self.api_key.echoMode() == QLineEdit.EchoMode.Password:
            self.api_key.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.api_key.setEchoMode(QLineEdit.EchoMode.Password)
            
    def save_config(self):
        self.config['api_key'] = self.api_key.text()
        self.config['model_id'] = self.model_select.currentText()
        self.config['temperature'] = self.temp_slider.value() / 100
        if utils.save_config(self.config):
            self.accept()