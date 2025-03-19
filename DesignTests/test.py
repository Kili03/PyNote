import sys

from PySide6.QtCore import Qt, QSize, QPoint
from PySide6.QtGui import QIcon, QPainter, QPixmap, QPen, QFont
from PySide6.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,
                               QHBoxLayout, QTreeWidget, QTreeWidgetItem,
                               QSplitter, QLabel, QPushButton, QComboBox,
                               QScrollArea, QFrame, QLineEdit)


class Canvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(800, 600)
        self.setAttribute(Qt.WA_StaticContents)
        self.modified = False
        self.scribbling = False
        self.myPenWidth = 1
        self.myPenColor = Qt.black
        self.image = QPixmap(self.size())
        self.image.fill(Qt.white)
        self.lastPoint = QPoint()

    def setPenColor(self, color):
        self.myPenColor = color

    def setPenWidth(self, width):
        self.myPenWidth = width

    def clearImage(self):
        self.image.fill(Qt.white)
        self.modified = True
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.lastPoint = event.position().toPoint()
            self.scribbling = True

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) and self.scribbling:
            painter = QPainter(self.image)
            painter.setPen(QPen(self.myPenColor, self.myPenWidth,
                                Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.lastPoint, event.position().toPoint())
            self.modified = True
            self.lastPoint = event.position().toPoint()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.scribbling:
            self.scribbling = False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.image)

    def resizeEvent(self, event):
        if self.width() > self.image.width() or self.height() > self.image.height():
            newWidth = max(self.width(), self.image.width())
            newHeight = max(self.height(), self.image.height())
            newImage = QPixmap(newWidth, newHeight)
            newImage.fill(Qt.white)
            painter = QPainter(newImage)
            painter.drawPixmap(QPoint(0, 0), self.image)
            self.image = newImage


class RibbonButton(QPushButton):
    def __init__(self, text="", icon_path=None, parent=None):
        super().__init__(text, parent)
        self.setMinimumSize(64, 64)
        self.setMaximumSize(80, 80)
        self.setStyleSheet("""
            QPushButton {
                border: none;
                border-radius: 4px;
                padding: 5px;
                text-align: center;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #E5F3FF;
            }
            QPushButton:pressed {
                background-color: #CCE4F7;
            }
        """)
        self.setCursor(Qt.PointingHandCursor)

        if icon_path:
            self.setIcon(QIcon(icon_path))
            self.setIconSize(QSize(32, 32))

        # Set text alignment to bottom
        self.setStyleSheet(self.styleSheet() + "QPushButton { text-align: bottom; }")


class RibbonGroup(QFrame):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setMaximumHeight(90)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(2)

        self.buttonsLayout = QHBoxLayout()
        self.buttonsLayout.setSpacing(2)
        layout.addLayout(self.buttonsLayout)

        titleLabel = QLabel(title)
        titleLabel.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
        titleLabel.setStyleSheet("color: #707070; font-size: 10px;")
        layout.addWidget(titleLabel)

        self.setStyleSheet("""
            RibbonGroup {
                background-color: transparent;
                border-right: 1px solid #E0E0E0;
                padding-right: 8px;
                margin-right: 2px;
            }
        """)

    def addButton(self, text, icon_path=None):
        button = RibbonButton(text, icon_path)
        self.buttonsLayout.addWidget(button)
        return button


class OneNoteApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OneNote Clone")
        self.resize(1200, 800)

        # Set application-wide font
        self.setupFonts()

        # Apply app-wide stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #FFFFFF;
            }
            QSplitter::handle {
                background-color: #F0F0F0;
            }
            QTreeWidget {
                border: none;
                background-color: #F9F9F9;
                selection-background-color: #E6F2FA;
                selection-color: #333333;
            }
            QTabWidget::pane {
                border-top: 1px solid #DDDDDD;
                background-color: #FAFAFA;
            }
            QTabBar::tab {
                background-color: #F0F0F0;
                border: 1px solid #DDDDDD;
                border-bottom: none;
                min-width: 80px;
                padding: 5px 10px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: #FFFFFF;
                border-bottom: 1px solid #FFFFFF;
            }
            QScrollBar:vertical {
                border: none;
                background: #F0F0F0;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #CDCDCD;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #DDDDDD;
                border-radius: 4px;
            }
            QPushButton {
                background-color: #F0F0F0;
                border: 1px solid #DDDDDD;
                border-radius: 4px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #E8E8E8;
            }
            QPushButton:pressed {
                background-color: #D8D8D8;
            }
        """)

        # Create central widget and layout
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.mainLayout = QVBoxLayout(self.centralWidget)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

        # Create and set up the ribbon
        self.setupRibbon()

        # Create main content area
        self.contentSplitter = QSplitter(Qt.Horizontal)

        # Create notebook navigation panel
        self.setupNotebookPanel()

        # Create main content area with canvas
        self.setupContentArea()

        # Add the splitter to the main layout
        self.mainLayout.addWidget(self.contentSplitter)

        # Set up status bar
        self.statusBar().showMessage("Ready")
        self.statusBar().setStyleSheet("QStatusBar { background-color: #F5F5F5; border-top: 1px solid #DDDDDD; }")

    def setupFonts(self):
        # Use system font or load custom ones
        font = QFont("Segoe UI", 10)  # Good for Windows
        QApplication.setFont(font)

    def setupRibbon(self):
        # Create tab widget for ribbon
        self.ribbon = QTabWidget()
        self.ribbon.setFixedHeight(130)
        self.ribbon.setTabPosition(QTabWidget.North)
        self.ribbon.setDocumentMode(True)

        # File tab (styled differently)
        fileTab = QWidget()
        fileLayout = QHBoxLayout(fileTab)
        fileTab.setStyleSheet("background-color: #7719AA;")
        fileBtn = QPushButton("File")
        fileBtn.setStyleSheet("color: white; font-size: 14px; background-color: transparent; border: none;")
        fileLayout.addWidget(fileBtn)
        fileLayout.addStretch()

        # Home tab
        homeTab = QWidget()
        homeLayout = QHBoxLayout(homeTab)
        homeLayout.setContentsMargins(10, 5, 10, 5)
        homeLayout.setSpacing(0)

        # Create styled ribbon groups
        clipboardGroup = RibbonGroup("Clipboard")
        clipboardGroup.addButton("Cut")
        clipboardGroup.addButton("Copy")
        clipboardGroup.addButton("Paste")

        basicTextGroup = RibbonGroup("Basic Text")
        basicTextGroup.addButton("Bold")
        basicTextGroup.addButton("Italic")
        basicTextGroup.addButton("Underline")
        basicTextGroup.addButton("Font")

        paragraphGroup = RibbonGroup("Paragraph")
        paragraphGroup.addButton("Left")
        paragraphGroup.addButton("Center")
        paragraphGroup.addButton("Right")
        paragraphGroup.addButton("Bullets")

        # Create pen tools group
        penGroup = RibbonGroup("Pens")
        penGroup.addButton("Pen")
        penGroup.addButton("Highlighter")
        penGroup.addButton("Eraser")

        # Add color selector
        colorCombo = QComboBox()
        colorCombo.addItems(["Black", "Blue", "Red", "Green"])
        colorCombo.setFixedWidth(80)
        colorCombo.setStyleSheet("""
            QComboBox {
                border: 1px solid #DDDDDD;
                border-radius: 3px;
                padding: 3px;
            }
        """)
        penGroup.layout().addWidget(colorCombo)

        # Add groups to Home tab
        homeLayout.addWidget(clipboardGroup)
        homeLayout.addWidget(basicTextGroup)
        homeLayout.addWidget(paragraphGroup)
        homeLayout.addWidget(penGroup)
        homeLayout.addStretch()

        # Insert tab
        insertTab = QWidget()
        insertLayout = QHBoxLayout(insertTab)

        tablesGroup = RibbonGroup("Tables")
        tablesGroup.addButton("Table")

        imagesGroup = RibbonGroup("Images")
        imagesGroup.addButton("Picture")
        imagesGroup.addButton("Online Picture")

        linksGroup = RibbonGroup("Links")
        linksGroup.addButton("Link")
        linksGroup.addButton("Attachment")

        insertLayout.addWidget(tablesGroup)
        insertLayout.addWidget(imagesGroup)
        insertLayout.addWidget(linksGroup)
        insertLayout.addStretch()

        # Draw tab
        drawTab = QWidget()
        drawLayout = QHBoxLayout(drawTab)

        toolsGroup = RibbonGroup("Tools")
        toolsGroup.addButton("Pen")
        toolsGroup.addButton("Marker")
        toolsGroup.addButton("Highlighter")
        toolsGroup.addButton("Eraser")

        shapesGroup = RibbonGroup("Shapes")
        shapesGroup.addButton("Rectangle")
        shapesGroup.addButton("Circle")
        shapesGroup.addButton("Line")
        shapesGroup.addButton("Arrow")

        drawLayout.addWidget(toolsGroup)
        drawLayout.addWidget(shapesGroup)
        drawLayout.addStretch()

        # View tab
        viewTab = QWidget()
        viewLayout = QHBoxLayout(viewTab)

        viewsGroup = RibbonGroup("Views")
        viewsGroup.addButton("Normal")
        viewsGroup.addButton("Page Width")
        viewsGroup.addButton("Full Page")

        zoomGroup = RibbonGroup("Zoom")
        zoomGroup.addButton("Zoom In")
        zoomGroup.addButton("Zoom Out")
        zoomGroup.addButton("100%")

        viewLayout.addWidget(viewsGroup)
        viewLayout.addWidget(zoomGroup)
        viewLayout.addStretch()

        # Add tabs to ribbon
        self.ribbon.addTab(fileTab, "File")
        self.ribbon.addTab(homeTab, "Home")
        self.ribbon.addTab(insertTab, "Insert")
        self.ribbon.addTab(drawTab, "Draw")
        self.ribbon.addTab(viewTab, "View")

        # Style the selected tab differently
        self.ribbon.setCurrentIndex(1)  # Select Home tab by default

        # Add ribbon to main layout
        self.mainLayout.addWidget(self.ribbon)

    def setupNotebookPanel(self):
        # Create notebook panel
        self.notebookPanel = QWidget()
        self.notebookPanel.setMinimumWidth(250)
        self.notebookPanel.setMaximumWidth(350)
        self.notebookPanel.setStyleSheet("""
            QWidget {
                background-color: #F5F5F5;
            }
        """)

        notebookLayout = QVBoxLayout(self.notebookPanel)
        notebookLayout.setContentsMargins(10, 10, 10, 10)
        notebookLayout.setSpacing(10)

        # Search bar
        searchBox = QLineEdit()
        searchBox.setPlaceholderText("Search all notebooks")
        searchBox.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #DDDDDD;
                border-radius: 4px;
                background-color: white;
            }
        """)
        notebookLayout.addWidget(searchBox)

        # Create notebook tree
        self.notebookTree = QTreeWidget()
        self.notebookTree.setHeaderHidden(True)
        self.notebookTree.setAnimated(True)
        self.notebookTree.setIndentation(20)
        self.notebookTree.setStyleSheet("""
            QTreeWidget {
                border: none;
                background-color: #F5F5F5;
                selection-background-color: #E1EFFA;
                selection-color: #333333;
                font-size: 12px;
            }
            QTreeWidget::item {
                height: 28px;
                padding-left: 4px;
                border-radius: 4px;
            }
            QTreeWidget::item:hover {
                background-color: #EAF6FF;
            }
            QTreeWidget::item:selected {
                background-color: #CCE8FF;
            }
        """)

        # Add sample notebooks with icons
        notebooks = {
            "Personal": ["Daily Notes", "Ideas", "Projects"],
            "Work": ["Meetings", "Tasks", "Research"],
            "School": ["Physics", "Math", "Biology"]
        }

        for notebook, sections in notebooks.items():
            notebookItem = QTreeWidgetItem([notebook])
            # notebookItem.setIcon(0, self.style().standardIcon(QApplication.style().SP_DirIcon))
            self.notebookTree.addTopLevelItem(notebookItem)

            # Add sections to notebooks
            for section in sections:
                sectionItem = QTreeWidgetItem([section])
                # sectionItem.setIcon(0, self.style().standardIcon(QApplication.style().SP_FileDialogDetailView))
                notebookItem.addChild(sectionItem)

                # Add pages to sections
                for i in range(1, 4):
                    pageItem = QTreeWidgetItem([f"Page {i}"])
                    # pageItem.setIcon(0, self.style().standardIcon(QApplication.style().SP_FileDialogContentsView))
                    sectionItem.addChild(pageItem)

        self.notebookTree.expandAll()
        notebookLayout.addWidget(self.notebookTree)

        # Add "+ Add page" button
        addPageBtn = QPushButton("+ Add page")
        addPageBtn.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;
                color: #7719AA;
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                padding: 8px;
                font-weight: bold;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #F9F9F9;
            }
        """)
        notebookLayout.addWidget(addPageBtn)

        # Add to splitter
        self.contentSplitter.addWidget(self.notebookPanel)

    def setupContentArea(self):
        # Create content area
        self.contentArea = QWidget()
        contentLayout = QVBoxLayout(self.contentArea)
        contentLayout.setContentsMargins(20, 20, 20, 20)

        # Page title
        pageTitleLayout = QHBoxLayout()
        pageTitle = QLineEdit("Untitled Page")
        pageTitle.setStyleSheet("""
            QLineEdit {
                font-size: 24px;
                font-weight: bold;
                color: #7719AA;
                border: none;
                background-color: transparent;
            }
            QLineEdit:focus {
                border-bottom: 1px solid #7719AA;
            }
        """)
        pageTitleLayout.addWidget(pageTitle)
        pageTitleLayout.addStretch()
        contentLayout.addLayout(pageTitleLayout)

        # Create timestamp
        dateLabel = QLabel("Created: March 19, 2025 • Last Edited: Just now")
        dateLabel.setStyleSheet("color: #707070; font-size: 11px;")
        contentLayout.addWidget(dateLabel)
        contentLayout.addSpacing(20)

        # Canvas for drawing/writing
        self.canvas = Canvas()
        self.canvas.setStyleSheet("""
            Canvas {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 4px;
            }
        """)

        # Create scroll area for canvas
        scrollArea = QScrollArea()
        scrollArea.setWidget(self.canvas)
        scrollArea.setWidgetResizable(True)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scrollArea.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #F0F0F0;
            }
        """)
        contentLayout.addWidget(scrollArea, 1)

        # Add to splitter
        self.contentSplitter.addWidget(self.contentArea)

        # Set stretch factors for splitter
        self.contentSplitter.setStretchFactor(0, 0)  # Notebook panel doesn't stretch
        self.contentSplitter.setStretchFactor(1, 1)  # Content area stretches


def main():
    app = QApplication(sys.argv)
    window = OneNoteApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()