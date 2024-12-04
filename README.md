# OpenwCursor

OpenwCursor is a Python script that installs or uninstalls context menu entries for opening files or directories with the Cursor application.

## Prerequisites

- Windows operating system
- Python 3.x installed
- Cursor application installed

## Installation

1. Clone the repository or download the script.
2. Open a terminal and navigate to the directory containing the script.
3. Run the script with administrator privileges:

```sh
python openwcursor.py
```

## Usage

- Install Context Menu Entries
To install the context menu entries, simply run the script without any arguments:

```
python openwcursor.py
```

The script will search for the Cursor.exe application in common installation paths and add context menu entries for opening files and directories with Cursor.

- Uninstall Context Menu Entries
To uninstall the context menu entries, run the script with the --uninstall argument:

```
python openwcursor.py --uninstall
```

## Functions
`is_admin()`
Checks if the script is running with administrator privileges.

`run_as_admin()`
Restarts the script with administrator privileges if it is not already running as an administrator.

`find_cursor_path()`
Searches for the Cursor.exe application in common installation paths and the AppData directory.

`create_registry_key(key_path, value_name, value_data)`
Creates a registry key with the specified path, value name, and value data.

`remove_registry_key(key_path)`
Removes a registry key with the specified path.

`install_context_menu(cursor_path)`
Installs context menu entries for opening files and directories with Cursor.

`uninstall_context_menu()`
Uninstalls context menu entries for opening files and directories with Cursor.

`restart_explorer()`
Restarts the Windows Explorer process to apply changes to the context menu.

`main()`
Main function that handles argument parsing and calls the appropriate functions to install or uninstall context menu entries.

## License
This project is licensed under the MIT License.

