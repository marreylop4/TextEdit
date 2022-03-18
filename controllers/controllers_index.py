from PySide2.QtCore import (QCoreApplication, QDir, QFile, QFileInfo, QMimeData,
                            QMimeDatabase, QUrl, Qt, Slot, QObject, QIODevice, QTranslator)

from PySide2.QtGui import ( QGuiApplication, QClipboard,
                           QCloseEvent, QFont, QFontDatabase, QFontInfo, QIcon,
                           QKeySequence, QPixmap, QTextBlockFormat,
                           QTextCharFormat, QTextCursor, QTextDocumentWriter,
                           QTextList, QTextListFormat, QTextDocument )
from PySide2.QtWidgets import (QApplication, QMainWindow, QColorDialog, QComboBox,
                               QDialog, QFileDialog, QFontComboBox, QStatusBar, QAction, QActionGroup,
                               QTextEdit, QToolBar, QMenu, QMenuBar, QMessageBox, QWidget, QSplitter, QFrame, QHBoxLayout)


from views.view_index import Index
from controllers.main_window import TextEditWindow

class IndexWindow(QWidget, Index):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle(QCoreApplication.applicationName())
        self.newFile.clicked.connect(self.file_new)
        self.openFile.clicked.connect(self.file_open)
        self.Information.clicked.connect(self.about)

    @Slot()
    def file_open(self):
        """
        This function loads a file in our text editor, being able 
        to load markdown and text type files.

        """
        window = TextEditWindow(self)
        file_dialog = QFileDialog(self, "Open File...")
        file_dialog.setAcceptMode(QFileDialog.AcceptOpen)
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setMimeTypeFilters(["text/markdown", "text/plain"])
        if file_dialog.exec() != QDialog.Accepted:
            return
        fn = file_dialog.selectedFiles()[0]
        native_fn = QDir.toNativeSeparators(fn)
        load = True 
        

        if not QFile.exists(fn):
            load = False
        file = QFile(fn)
        if not file.open(QFile.ReadOnly):
            load = False

        data = file.readAll()
        file_info= QFileInfo(file)
        window.set_current_file_format( file_info.suffix())
        #db = QMimeDatabase()
        #mime_type_name = db.mimeTypeForFileNameAndData(fn, data).name()
        text = data.data().decode('utf8')
        #if mime_type_name == "text/markdown":
        #    window._text_edit.setPlainText(text)
        #else:
        window._text_edit.setPlainText(text)

        window.set_current_file_name(fn)
        load = True
    
        if load:
            window.statusBar().showMessage(f'Opened "{native_fn}"')
        else:
            window.statusBar().showMessage(f'Could not open "{native_fn}"')
        window.show()

    @Slot()
    def file_new(self):
        """
        This function open the text editor with a new file

        
        """ 
        window= TextEditWindow(self)
        window.show()
     
    @Slot()       
    def about(self):
        """
        This function creates a message box with information about what you can do in the application
        
        """ 
        
        QMessageBox.about(self, "About", """""".join(["""<p>This is a markdown text editor with preview. The
                     uploaded or created files can be saved in different formats 
                     such as HTML. If you want to know more about markdown here is a link about it:</p>
                     <a href = https://www.markdownguide.org/basic-syntax/#html>Markdown Guide</a> """])
)
