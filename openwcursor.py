import os
import sys
import winreg
import ctypes
from pathlib import Path
import subprocess
import argparse

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(['"' + sys.argv[0] + '"'] + sys.argv[1:]), None, 1)

def find_cursor_path():
    # Common installation paths
    possible_paths = [
        os.path.join(os.getenv('LOCALAPPDATA'), 'Programs', 'cursor', 'Cursor.exe'),
        os.path.join(os.getenv('LOCALAPPDATA'), 'Programs', 'Cursor', 'Cursor.exe'),
        os.path.join(os.getenv('PROGRAMFILES'), 'cursor', 'Cursor.exe'),
        os.path.join(os.getenv('PROGRAMFILES'), 'Cursor', 'Cursor.exe'),
        os.path.join(os.getenv('PROGRAMFILES(X86)'), 'cursor', 'Cursor.exe'),
        os.path.join(os.getenv('PROGRAMFILES(X86)'), 'Cursor', 'Cursor.exe'),
    ]
    
    # Check each possible path
    for path in possible_paths:
        if os.path.isfile(path):
            return path
            
    # If not found in common paths, try to find it in AppData recursively
    appdata_path = os.getenv('LOCALAPPDATA')
    for root, dirs, files in os.walk(appdata_path):
        if 'Cursor.exe' in files:
            return os.path.join(root, 'Cursor.exe')
            
    return None

def create_registry_key(key_path, value_name, value_data):
    try:
        # Split the key path into root and sub_key
        root_key = winreg.HKEY_CLASSES_ROOT
        
        # Create or open the key
        key = winreg.CreateKeyEx(root_key, key_path, 0, winreg.KEY_WRITE)
        
        # Set the value
        winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, value_data)
        
        # Close the key
        winreg.CloseKey(key)
        return True
    except Exception as e:
        print(f"Error creating registry key {key_path}: {str(e)}")
        return False

def remove_registry_key(key_path):
    try:
        winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, key_path)
    except:
        pass

def install_context_menu(cursor_path):
    # First remove any existing entries
    keys_to_remove = [
        r'Directory\Background\shell\Open with Cursor\command',
        r'Directory\Background\shell\Open with Cursor',
        r'Directory\shell\Open with Cursor\command',
        r'Directory\shell\Open with Cursor',
        r'*\shell\Open with Cursor\command',
        r'*\shell\Open with Cursor'
    ]
    
    for key in keys_to_remove:
        remove_registry_key(key)

    # Add new registry entries
    registry_entries = [
        # Background (right-click in folder)
        {
            'key_path': r'Directory\Background\shell\Open with Cursor',
            'entries': [
                ('', 'Open with Cursor'),
                ('Icon', cursor_path)
            ]
        },
        {
            'key_path': r'Directory\Background\shell\Open with Cursor\command',
            'entries': [
                ('', f'"{cursor_path}" "."')
            ]
        },
        # Folder
        {
            'key_path': r'Directory\shell\Open with Cursor',
            'entries': [
                ('', 'Open with Cursor'),
                ('Icon', cursor_path)
            ]
        },
        {
            'key_path': r'Directory\shell\Open with Cursor\command',
            'entries': [
                ('', f'"{cursor_path}" "%1"')
            ]
        },
        # Files
        {
            'key_path': r'*\shell\Open with Cursor',
            'entries': [
                ('', 'Open with Cursor'),
                ('Icon', cursor_path)
            ]
        },
        {
            'key_path': r'*\shell\Open with Cursor\command',
            'entries': [
                ('', f'"{cursor_path}" "%1"')
            ]
        }
    ]

    success = True
    for entry in registry_entries:
        for value_name, value_data in entry['entries']:
            if not create_registry_key(entry['key_path'], value_name, value_data):
                success = False

    return success

def uninstall_context_menu():
    keys_to_remove = [
        r'Directory\Background\shell\Open with Cursor\command',
        r'Directory\Background\shell\Open with Cursor',
        r'Directory\shell\Open with Cursor\command',
        r'Directory\shell\Open with Cursor',
        r'*\shell\Open with Cursor\command',
        r'*\shell\Open with Cursor'
    ]
    
    print("Removing context menu entries...")
    for key in keys_to_remove:
        remove_registry_key(key)
    
    print("Restarting Explorer...")
    restart_explorer()
    print("Successfully removed context menu entries!")

def restart_explorer():
    try:
        subprocess.run(['taskkill', '/f', '/im', 'explorer.exe'], check=True)
        subprocess.Popen('explorer.exe')
    except:
        print("Failed to restart Explorer automatically. Please restart it manually.")

def main():
    if not is_admin():
        run_as_admin()
        return

    parser = argparse.ArgumentParser(description='Install/Uninstall Cursor context menu')
    parser.add_argument('--uninstall', action='store_true', help='Uninstall context menu entries')
    args = parser.parse_args()

    if args.uninstall:
        uninstall_context_menu()
        return

    print("Looking for Cursor installation...")
    cursor_path = find_cursor_path()
    
    if not cursor_path:
        print("Error: Could not find Cursor.exe")
        print("Please enter the path to Cursor.exe manually:")
        cursor_path = input().strip('"')
        if not os.path.isfile(cursor_path):
            print("Invalid path. Exiting...")
            return

    print(f"Found Cursor at: {cursor_path}")
    print("Installing context menu entries...")
    
    if install_context_menu(cursor_path):
        print("Successfully installed context menu entries!")
        print("Restarting Explorer...")
        restart_explorer()
        print("Done! You should now see 'Open with Cursor' in your context menu.")
    else:
        print("Failed to install context menu entries.")

if __name__ == '__main__':
    main()