import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
import docx2txt


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "Simplified_MS_Word"
        self.setWindowTitle(self.title)

        self.editor = QTextEdit(self) 
        self.setCentralWidget(self.editor)

        self.create_menu_bar()
        self.create_toolbar()

        font = QFont('Times', 12)
        self.editor.setFont(font)
        self.editor.setFontPointSize(12)

        self.path = ''

    def create_menu_bar(self):
        menu_bar = QMenuBar(self)

        app_icon = menu_bar.addMenu(QIcon("doc_icon.png"), "icon")

        file_menu = QMenu("File", self)
        menu_bar.addMenu(file_menu)

        save_action = QAction('Save', self)
        save_action.triggered.connect(self.file_save)
        file_menu.addAction(save_action)

        open_action = QAction('Open', self)
        open_action.triggered.connect(self.file_open)
        file_menu.addAction(open_action)

        rename_action = QAction('Rename', self)
        rename_action.triggered.connect(self.file_save_as)
        file_menu.addAction(rename_action)

        pdf_action = QAction("Save as PDF", self)
        pdf_action.triggered.connect(self.save_pdf)
        file_menu.addAction(pdf_action)

        edit_menu = QMenu("Edit", self)
        menu_bar.addMenu(edit_menu)

        paste_action = QAction('Paste', self)
        paste_action.triggered.connect(self.editor.paste)
        edit_menu.addAction(paste_action)

        clear_action = QAction('Clear', self)
        clear_action.triggered.connect(self.editor.clear)
        edit_menu.addAction(clear_action)

        select_action = QAction('Select All', self)
        select_action.triggered.connect(self.editor.selectAll)
        edit_menu.addAction(select_action)

        view_menu = QMenu("View", self)
        menu_bar.addMenu(view_menu)

        full_screen_action = QAction('Full Screen View', self)
        full_screen_action.triggered.connect(lambda: self.showFullScreen())
        view_menu.addAction(full_screen_action)

        normal_screen_action = QAction('Normal View', self)
        normal_screen_action.triggered.connect(lambda: self.showNormal())
        view_menu.addAction(normal_screen_action)

        minimum_screen_action = QAction('Minimize', self)
        minimum_screen_action.triggered.connect(lambda: self.showMinimized())
        view_menu.addAction(minimum_screen_action)

        self.setMenuBar(menu_bar)

    def create_toolbar(self):
        tool_bar = QToolBar("Tools", self)

        undo_action = QAction(QIcon("undo.png"), 'Undo', self)
        undo_action.triggered.connect(self.editor.undo)
        tool_bar.addAction(undo_action)

        redo_action = QAction(QIcon("redo.png"), 'Redo', self)
        redo_action.triggered.connect(self.editor.redo)
        tool_bar.addAction(redo_action)

        tool_bar.addSeparator()

        copy_action = QAction(QIcon("copy.png"), 'Copy', self)
        copy_action.triggered.connect(self.editor.copy)
        tool_bar.addAction(copy_action)

        cut_action = QAction(QIcon("cut.png"), 'Cut', self)
        cut_action.triggered.connect(self.editor.cut)
        tool_bar.addAction(cut_action)

        paste_action = QAction(QIcon("paste.png"), 'Paste', self)
        paste_action.triggered.connect(self.editor.paste)
        tool_bar.addAction(paste_action)

        tool_bar.addSeparator()
        tool_bar.addSeparator()

        self.font_combo = QComboBox(self)
        self.font_combo.addItems(["Courier Std", "Hellentic Typewriter Regular", "Helvetica", "Arial", "SansSerif", "Helvetica", "Times", "Monospace"])
        self.font_combo.activated.connect(self.set_font)
        tool_bar.addWidget(self.font_combo)

        self.font_size = QSpinBox(self)   
        self.font_size.setValue(12)  
        self.font_size.valueChanged.connect(self.set_font_size)
        tool_bar.addWidget(self.font_size)

        tool_bar.addSeparator()

        bold_action = QAction(QIcon("bold.png"), 'Bold', self)
        bold_action.triggered.connect(self.bold_text)
        tool_bar.addAction(bold_action)

        underline_action = QAction(QIcon("underline.png"), 'Underline', self)
        underline_action.triggered.connect(self.underline_text)
        tool_bar.addAction(underline_action)

        italic_action = QAction(QIcon("italic.png"), 'Italic', self)
        italic_action.triggered.connect(self.italic_text)
        tool_bar.addAction(italic_action)

        tool_bar.addSeparator()

        right_alignment_action = QAction(QIcon("right-align.png"), 'Align Right', self)
        right_alignment_action.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignRight))
        tool_bar.addAction(right_alignment_action)

        left_alignment_action = QAction(QIcon("left-align.png"), 'Align Left', self)
        left_alignment_action.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignLeft))
        tool_bar.addAction(left_alignment_action)

        justification_action = QAction(QIcon("justification.png"), 'Center/Justify', self)
        justification_action.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignCenter))
        tool_bar.addAction(justification_action)

        tool_bar.addSeparator()

        zoom_in_action = QAction(QIcon("zoom-in.png"), 'Zoom in', self)
        zoom_in_action.triggered.connect(self.editor.zoomIn)
        tool_bar.addAction(zoom_in_action)

        zoom_out_action = QAction(QIcon("zoom-out.png"), 'Zoom out', self)
        zoom_out_action.triggered.connect(self.editor.zoomOut)
        tool_bar.addAction(zoom_out_action)

        tool_bar.addSeparator()
        
        self.addToolBar(tool_bar)

    def italic_text(self):
        state = self.editor.fontItalic()
        self.editor.setFontItalic(not state)

    def underline_text(self):
        state = self.editor.fontUnderline()
        self.editor.setFontUnderline(not state)

    def bold_text(self):
        if self.editor.fontWeight() != QFont.Bold:
            self.editor.setFontWeight(QFont.Bold)
            return
        self.editor.setFontWeight(QFont.Normal)

    def set_font(self):
        font = self.font_combo.currentText()
        self.editor.setCurrentFont(QFont(font))

    def set_font_size(self):
        value = self.font_size.value()
        self.editor.setFontPointSize(value)

    def file_open(self):
        self.path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Text documents (*.text);Text documents (*.txt);All files (*.*)")
        try:
            text = docx2txt.process(self.path)
        except Exception as e:
            print(e)
        else:
            self.editor.setText(text)
            self.update_title()

    def file_save(self):
        print(self.path)
        if self.path == '':
            self.file_saveas()

        text = self.editor.toPlainText()

        try:
            with open(self.path, 'w') as f:
                f.write(text)
                self.update_title()
        except Exception as e:
            print(e)

    def file_save_as(self):
        self.path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "text documents (*.text);Text documents (*.txt);All files (*.*)")

        if self.path == '':
            return

        text = self.editor.toPlainText()

        try:
            with open(path, 'w') as f:
                f.write(text)
                self.update_title()
        except Exception as e:
            print(e)

    def update_title(self):
        self.setWindowTitle(self.title + ' ' + self.path)

    def save_pdf(self):
        f_name, _ = QFileDialog.getSaveFileName(self, "Export PDF", None, "PDF files (.pdf);;All files()")
        print(f_name)

        if f_name != '':
           printer = QPrinter(QPrinter.HighResolution)
           printer.setOutputFormat(QPrinter.PdfFormat)
           printer.setOutputFileName(f_name)
           self.editor.document().print_(printer)
    

app = QApplication(sys.argv)
window = MainApp()
window.show()
sys.exit(app.exec_())
