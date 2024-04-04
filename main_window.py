from PyQt6.QtWidgets import QMainWindow, QTableView, QVBoxLayout, QWidget, QPushButton, QFileDialog, QLineEdit, QHBoxLayout, QTabWidget
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from PyQt6.QtCore import Qt, QSortFilterProxyModel
from xml_parser import parse_xml_file
from database import create_table, insert_data, update_data
from new_names_tab import NewNamesTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Popular Names of Acts in US Law")
        self.resize(800, 600)

        # Connect to the SQLite database
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("popular_names.db")
        if not self.db.open():
            print("Failed to open the database.")
            return

        # Create the popular_names table if it doesn't exist
        create_table(self.db)

        # Create a central widget and layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create a tab widget
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)

        # Create the main tab
        main_tab = QWidget()
        main_tab_layout = QVBoxLayout(main_tab)

        # Create a layout for the filter field and clear button
        filter_layout = QHBoxLayout()
        main_tab_layout.addLayout(filter_layout)

        # Create a line edit for filtering
        self.filter_edit = QLineEdit()
        self.filter_edit.setPlaceholderText("Filter")
        self.filter_edit.textChanged.connect(self.apply_filter)
        filter_layout.addWidget(self.filter_edit)

        # Create a clear button
        clear_button = QPushButton("x")
        clear_button.setFixedWidth(30)
        clear_button.clicked.connect(self.clear_filter)
        filter_layout.addWidget(clear_button)

        # Create a table view
        self.table_view = QTableView()
        self.table_view.setSortingEnabled(True)
        main_tab_layout.addWidget(self.table_view)

        # Create the new names tab
        self.new_names_tab = NewNamesTab(self.db)
        self.tab_widget.addTab(self.new_names_tab, "New Popular Names")

        # Add the main tab to the tab widget
        self.tab_widget.addTab(main_tab, "Popular Names (final)")

        # Load data from the database into the table view
        self.load_data()

    def load_data(self):
        self.model = QSqlTableModel(self, self.db)
        self.model.setTable("popular_names")
        self.model.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)
        self.model.setFilter("final = 1")
        self.model.select()

        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.proxy_model.setFilterKeyColumn(-1)  # Filter on all columns
        self.proxy_model.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.proxy_model.setSortRole(Qt.ItemDataRole.DisplayRole)
        self.proxy_model.setSortCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.proxy_model.sort(0, Qt.SortOrder.AscendingOrder)

        self.table_view.setModel(self.proxy_model)
        self.table_view.resizeColumnsToContents()

    def apply_filter(self, text):
        self.proxy_model.setFilterFixedString(text)

    def clear_filter(self):
        self.filter_edit.clear()

    def closeEvent(self, event):
        self.db.close()
        super().closeEvent(event)

def custom_sort_key(value):
    if value.isdigit():
        return (0, int(value))
    else:
        return (1, value.lower())

QSortFilterProxyModel.lessThan = lambda self, left, right: custom_sort_key(str(left.data())) < custom_sort_key(str(right.data()))