from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableView, QPushButton, QFileDialog, QHeaderView, QCheckBox, QStyledItemDelegate
from PyQt6.QtSql import QSqlTableModel
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QRegion
from PyQt6.QtSql import QSqlQuery
from xml_parser import parse_xml_file
from database import insert_data, update_data

class NewNamesTab(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.layout = QVBoxLayout(self)

        # Create a table view
        self.table_view = QTableView()
        self.table_view.setSortingEnabled(True)
        self.layout.addWidget(self.table_view)

        # Create a button to import XML data
        import_button = QPushButton("Import XML")
        import_button.clicked.connect(self.import_xml)
        self.layout.addWidget(import_button)
        
        # Create a button to delete the selected row
        delete_row_button = QPushButton("Delete Row")
        delete_row_button.clicked.connect(self.delete_row)
        self.layout.addWidget(delete_row_button)

        # Create a button to delete all rows
        delete_all_rows_button = QPushButton("Delete All Rows")
        delete_all_rows_button.clicked.connect(self.delete_all_rows)
        self.layout.addWidget(delete_all_rows_button) 

        # Load data from the database into the table view
        self.load_data()

    def load_data(self):
        self.model = QSqlTableModel(self, self.db)
        self.model.setTable("popular_names")
        self.model.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)
        self.model.setFilter("final = 0")  # Load only rows with 'final' as 0
        self.model.select()
        self.model.dataChanged.connect(self.on_data_changed)

        self.table_view.setModel(self.model)
        self.table_view.resizeColumnsToContents()

        # Add a checkbox column for finalizing items
        self.model.insertColumn(self.model.columnCount())
        self.model.setHeaderData(self.model.columnCount() - 1, Qt.Orientation.Horizontal, "Finalize")

        # Set the checkbox delegate for the finalize column
        delegate = CheckBoxDelegate(self.table_view)
        self.table_view.setItemDelegateForColumn(self.model.columnCount() - 1, delegate)

        # Connect the finalize all button to the toggle_finalize_all slot
        header = self.table_view.horizontalHeader()
        header.sectionClicked.connect(self.toggle_finalize_all)

    def on_data_changed(self, top_left, bottom_right):
        row_id = self.model.record(top_left.row()).value("id")
        column = self.model.record().fieldName(top_left.column())
        value = self.model.data(top_left)
        update_data(self.db, row_id, column, value)
    
    def delete_row(self):
        current_row = self.table_view.currentIndex().row()
        if current_row >= 0:
            record = self.model.record(current_row)
            row_id = record.value("id")
            self.model.removeRow(current_row)
            self.model.submitAll()
            query = QSqlQuery(self.db)
            query.prepare("DELETE FROM popular_names WHERE id = ?")
            query.addBindValue(row_id)
            query.exec()

    def delete_all_rows(self):
        self.model.removeRows(0, self.model.rowCount())
        self.model.submitAll()
        query = QSqlQuery(self.db)
        query.exec("DELETE FROM popular_names WHERE final = 0")

    def import_xml(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "Import XML", "", "XML Files (*.xml)")
        if file_path:
            popular_names = parse_xml_file(file_path)
            for name in popular_names:
                insert_data(self.db, name)
            self.load_data()

    def toggle_finalize_all(self, index):
        if index == self.model.columnCount() - 1:
            finalize = not self.model.headerData(index, Qt.Orientation.Horizontal)
            for row in range(self.model.rowCount()):
                self.model.setData(self.model.index(row, index), finalize, Qt.ItemDataRole.EditRole)
            self.model.setHeaderData(index, Qt.Orientation.Horizontal, finalize, Qt.ItemDataRole.EditRole)
            self.model.submitAll()

class CheckBoxDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        checked = index.data(Qt.ItemDataRole.EditRole)
        if checked is None:
            checked = False
        checkbox = QCheckBox(self.parent())
        checkbox.setChecked(checked)
        checkbox.rect = option.rect
        checkbox.setGeometry(option.rect)
        painter.save()
        painter.translate(option.rect.topLeft())
        checkbox.render(painter, QPoint(), QRegion(), QWidget.RenderFlag.DrawChildren)
        painter.restore()

    def createEditor(self, parent, option, index):
        return None

    def setEditorData(self, editor, index):
        pass

    def setModelData(self, editor, model, index):
        checked = not bool(index.data(Qt.ItemDataRole.EditRole))
        model.setData(index, checked, Qt.ItemDataRole.EditRole)