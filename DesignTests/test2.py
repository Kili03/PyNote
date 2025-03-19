import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *


class AdvancedOneNoteUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced PyNote")
        self.setGeometry(100, 100, 1400, 900)
        self.setup_ui()

    def setup_ui(self):
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create ribbon
        self.create_ribbon(main_layout)

        # Create main content area
        content_layout = QHBoxLayout()
        main_layout.addLayout(content_layout)

        # Create advanced sidebar
        self.create_advanced_sidebar(content_layout)

        # Create notebook area
        self.create_notebook_area(content_layout)

        # Apply styling
        self.apply_advanced_styles()

    def create_ribbon(self, parent_layout):
        # Ribbon container
        ribbon = QWidget()
        ribbon.setFixedHeight(120)
        parent_layout.addWidget(ribbon)

        # Ribbon layout
        ribbon_layout = QVBoxLayout(ribbon)
        ribbon_layout.setContentsMargins(0, 0, 0, 0)

        # Ribbon tabs
        tab_bar = QTabBar()
        tab_bar.addTab("Home")
        tab_bar.addTab("Insert")
        tab_bar.addTab("Draw")
        tab_bar.addTab("View")
        ribbon_layout.addWidget(tab_bar)

        # Ribbon content area
        ribbon_content = QWidget()
        ribbon_content.setFixedHeight(90)
        ribbon_layout.addWidget(ribbon_content)

        # Home tab content
        home_layout = QHBoxLayout(ribbon_content)
        home_layout.setContentsMargins(10, 5, 10, 5)

        # Clipboard section
        clipboard_group = self.create_ribbon_group("Clipboard", ["Paste", "Cut", "Copy", "Format Painter"])
        home_layout.addWidget(clipboard_group)

        # Basic Text section
        text_group = self.create_ribbon_group("Basic Text", ["Bold", "Italic", "Underline", "Font"])
        home_layout.addWidget(text_group)

        # Tags section
        tags_group = self.create_ribbon_group("Tags", ["To Do", "Important", "Question", "Customize"])
        home_layout.addWidget(tags_group)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        home_layout.addWidget(spacer)

    def create_ribbon_group(self, title, buttons):
        group = QWidget()
        layout = QVBoxLayout(group)

        # Title
        label = QLabel(title)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # Buttons
        btn_layout = QHBoxLayout()
        for btn_text in buttons:
            btn = QToolButton()
            btn.setText(btn_text)
            btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            btn.setIcon(QApplication.style().standardIcon(QStyle.SP_FileIcon))
            btn.setFixedSize(80, 60)
            btn_layout.addWidget(btn)

        layout.addLayout(btn_layout)
        return group

    def create_advanced_sidebar(self, parent_layout):
        sidebar = QDockWidget("Navigation", self)
        sidebar.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetClosable)
        sidebar.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        sidebar.setFixedWidth(300)

        # Container widget
        container = QWidget()
        splitter = QSplitter(Qt.Vertical)

        # Notebooks section
        notebook_tree = QTreeWidget()
        notebook_tree.setHeaderHidden(True)
        notebook_tree.setObjectName("notebookTree")

        # Add sample notebooks
        personal = QTreeWidgetItem(notebook_tree, ["Personal Notebook"])
        personal.addChild(QTreeWidgetItem(["Chapter 1"]))
        personal.addChild(QTreeWidgetItem(["Chapter 2"]))

        work = QTreeWidgetItem(notebook_tree, ["Work Notebook"])
        work.addChild(QTreeWidgetItem(["Projects"]))
        work.addChild(QTreeWidgetItem(["Meetings"]))

        # Pages section
        page_list = QListWidget()
        page_list.setObjectName("pageList")
        page_list.addItems(["Daily Notes", "Meeting Minutes", "Ideas Board", "Tasks"])

        # Add to splitter
        splitter.addWidget(notebook_tree)
        splitter.addWidget(page_list)
        splitter.setSizes([200, 200])

        container_layout = QVBoxLayout(container)
        container_layout.addWidget(splitter)
        sidebar.setWidget(container)
        self.addDockWidget(Qt.LeftDockWidgetArea, sidebar)

    def create_notebook_area(self, parent_layout):
        # Main notebook container
        notebook_container = QWidget()
        layout = QVBoxLayout(notebook_container)
        layout.setContentsMargins(0, 0, 0, 0)

        # Page header
        header = QWidget()
        header.setFixedHeight(40)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(10, 0, 10, 0)

        title_label = QLabel("Daily Notes")
        title_label.setObjectName("pageTitle")
        date_label = QLabel(QDate.currentDate().toString("dddd, MMMM d, yyyy"))
        date_label.setObjectName("pageDate")

        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(date_label)

        # Content area
        content = QTextEdit()
        content.setPlaceholderText("Start typing your notes here...")

        layout.addWidget(header)
        layout.addWidget(content)
        parent_layout.addWidget(notebook_container)

    def apply_advanced_styles(self):
        accent_color = "#5C2D91"  # OneNote purple
        hover_color = "#E1D5E7"  # Light purple
        selected_color = "#F3F0F5"  # Very light purple

        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: #FFFFFF;
            }}
            QTabBar::tab {{
                background: #F5F5F5;
                color: #333333;
                border: 1px solid #DDDDDD;
                padding: 8px 12px;
                margin-right: 2px;
                font-weight: bold;
            }}
            QTabBar::tab:selected {{
                background: {accent_color};
                color: white;
                border-color: {accent_color};
            }}
            QDockWidget {{
                titlebar-close-icon: url(none);
                titlebar-normal-icon: url(none);
                border: 1px solid #DDDDDD;
            }}
            QTreeWidget, QListWidget {{
                border: none;
                background: white;
            }}
            QTreeWidget::item, QListWidget::item {{
                padding: 8px;
                border-bottom: 1px solid #EEEEEE;
            }}
            QTreeWidget::item:hover, QListWidget::item:hover {{
                background: {hover_color};
            }}
            QTreeWidget::item:selected, QListWidget::item:selected {{
                background: {selected_color};
                color: #333333;
                border-left: 4px solid {accent_color};
            }}
            #pageTitle {{
                font-size: 18px;
                font-weight: bold;
                color: {accent_color};
            }}
            #pageDate {{
                font-size: 14px;
                color: #666666;
            }}
            QTextEdit {{
                background: white;
                border: none;
                padding: 15px;
                font-size: 14px;
            }}
            QToolButton {{
                background: transparent;
                border: 1px solid transparent;
                padding: 5px;
                color: #333333;
                border-radius: 4px;
            }}
            QToolButton:hover {{
                background: {hover_color};
                border: 1px solid #CCCCCC;
            }}
            QToolButton:pressed {{
                background: {selected_color};
            }}
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = AdvancedOneNoteUI()
    window.show()
    sys.exit(app.exec())