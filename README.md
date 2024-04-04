# Popular Names of Acts in US Law

This application is designed to display and manage the Popular Names of Acts in US law. It provides a user-friendly interface to view, edit, filter, sort, and save the popular names data.

## Usage

### Importing New Names

To import new names into the application, follow these steps:

1. Click on the "New Names" tab in the main window.
2. Click on the "Import XML" button.
3. In the file dialog, navigate to the XML file containing the new names data and select it.
4. Click "Open" to import the data into the application.

The imported names will be added to the "New Names" table, where they can be further edited and managed.

### Editing Names

To edit a name in the application, follow these steps:

1. Double-click on the cell you want to edit in either the "Final Names" or "New Names" table.
2. Make the necessary changes to the cell value.
3. Press Enter or click outside the cell to save the changes.

The edited value will be automatically saved to the database.

### Filtering Names

To filter the names in the "Final Names" table, follow these steps:

1. In the "Final Names" tab, locate the filter field at the top of the table.
2. Enter the desired search term in the filter field.
3. The table will automatically update to display only the names that match the filter criteria.
4. To clear the filter, click on the "x" button next to the filter field.

### Sorting Names

To sort the names in either the "Final Names" or "New Names" table, follow these steps:

1. Click on the column header of the column you want to sort.
2. The table will be sorted in ascending order based on the values in that column.
3. Click on the column header again to toggle between ascending and descending order.

### Saving Names

The application automatically saves any changes made to the names in the database. There is no need to manually save the data.

### Finalizing New Names

To finalize new names and move them to the "Final Names" table, follow these steps:

1. In the "New Names" tab, locate the "Finalize" column.
2. Click on the checkbox next to the name you want to finalize.
3. The name will be moved from the "New Names" table to the "Final Names" table.
4. To finalize all new names at once, click on the "Finalize" column header.

## Technical Documentation

### Prerequisites

- Python 3.x
- PyQt6

### Setting Up the Development Environment

1. Clone the repository:

```
git clone https://github.com/your-username/popular-names-app.git
cd popular-names-app
```

2. Create a virtual environment:

```
python -m venv venv
```

3. Activate the virtual environment:

- On Windows:

  ```
  venv\Scripts\activate
  ```

- On macOS and Linux:

  ```
  source venv/bin/activate
  ```

4. Install the dependencies:

```
pip install -r requirements.txt
```

### Running the Application in Development

To run the application in development mode, execute the following command:

```
python main.py
```

The application window will open, and you can start using the Popular Names of Acts in US Law application.

### Building an Executable for Production

To build an executable version of the application for production, you can use tools like PyInstaller or cx_Freeze. Here's an example using PyInstaller:

1. Install PyInstaller:

```
pip install pyinstaller
```

2. Run the following command to build the executable:

```
pyinstaller --onefile --windowed main.py
```

3. The executable will be generated in the `dist` directory.

Note: Make sure to include the necessary files (e.g., XML files, database file) in the same directory as the executable when distributing the application.

## Conclusion

The Popular Names of Acts in US Law application provides an intuitive interface for managing and interacting with the popular names data. It offers features such as importing new names, editing existing names, filtering and sorting the data, and finalizing new names. The application is built using Python and PyQt6, making it cross-platform and easy to deploy.

If you have any further questions or need assistance, please refer to the documentation or contact the application maintainer.