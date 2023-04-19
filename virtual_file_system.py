# virtual_file_system.py

import os


class VirtualFile:
    def __init__(self, content, page_size):
        self.pages = [content[i:i+page_size] for i in range(0, len(content), page_size)]


class VirtualFileSystem:
    def __init__(self, page_size=2000):
        self.virtual_files = {}
        self.page_size = page_size

    def dump_all(self, dump_directory="dump"):
        if not os.path.exists(dump_directory):
            os.makedirs(dump_directory)

        for file_name in self.virtual_files:
            file_path = os.path.join(dump_directory, file_name)
            with open(file_path, 'w') as f:
                for page in self.virtual_files[file_name].pages:
                    f.write(page)
        return f"All virtual files saved to '{dump_directory}' directory."


    def create_file(self, file_name, content):
        if file_name in self.virtual_files:
            return f"Error: File '{file_name}' already exists."
        self.virtual_files[file_name] = VirtualFile(content, self.page_size)
        return f"File '{file_name}' created."

    def read_file(self, file_name, page, include_surrounding=False, surrounding_chars=100):
        if file_name not in self.virtual_files:
            return f"Error: No such file: '{file_name}'"
        if page >= len(self.virtual_files[file_name].pages):
            return f"Error: Invalid page: {page}"
        
        content = self.virtual_files[file_name].pages[page]

        if include_surrounding:
            prev_page = self.virtual_files[file_name].pages[page - 1] if page > 0 else ""
            next_page = self.virtual_files[file_name].pages[page + 1] if page < len(self.virtual_files[file_name].pages) - 1 else ""

            prev_content = prev_page[-surrounding_chars:] if prev_page else ""
            next_content = next_page[:surrounding_chars] if next_page else ""

            content = f"{prev_content}{content}{next_content}"

        return content

    def update_file(self, file_name, page, new_content):
        if file_name not in self.virtual_files:
            return f"Error: No such file: '{file_name}'"
        if page >= len(self.virtual_files[file_name].pages):
            return f"Error: Invalid page: {page}"
        self.virtual_files[file_name].pages[page] = new_content
        self.reorganize_pages(file_name)
        return f"File '{file_name}' updated at page {page}."

    def save_to_disk(self, file_name, file_path=None):
        if file_name not in self.virtual_files:
            return f"Error: No such file: '{file_name}'"
        if not file_path:
            file_path = file_name
        with open(file_path, 'w') as f:
            for page in self.virtual_files[file_name].pages:
                f.write(page)
        return f"File '{file_name}' saved to disk at '{file_path}'."

    def list_files(self):
        return "Files: " + ", ".join(self.virtual_files.keys())

    def delete_file(self, file_name):
        if file_name not in self.virtual_files:
            return f"Error: No such file: '{file_name}'"
        del self.virtual_files[file_name]
        return f"File '{file_name}' deleted."

    def append_to_file(self, file_name, content):
        if file_name not in self.virtual_files:
            return f"Error: No such file: '{file_name}'"
        self.virtual_files[file_name].pages.extend(
            [content[i:i+self.page_size] for i in range(0, len(content), self.page_size)]
        )
        return f"Content appended to file '{file_name}'."

    def rename_file(self, old_name, new_name):
        if old_name not in self.virtual_files:
            return f"Error: No such file: '{old_name}'"
        if new_name in self.virtual_files:
            return f"Error: File already exists: '{new_name}'"
        self.virtual_files[new_name] = self.virtual_files.pop(old_name)
        return f"File '{old_name}' renamed to '{new_name}'."

    def get_file_info(self, file_name):
        if file_name not in self.virtual_files:
            return f"Error: No such file: '{file_name}'"
        file = self.virtual_files[file_name]
        return f"File '{file_name}' has {len(file.pages)} pages and a total size of {sum(len(page) for page in file.pages)} characters."

    def reorganize_pages(self, file_name):
        if file_name not in self.virtual_files:
            return f"Error: No such file: '{file_name}'"
        file = self.virtual_files[file_name]
        content = "".join(file.pages)
        file.pages = [content[i:i+self.page_size] for i in range(0, len(content), self.page_size)]
        return f"Pages reorganized for file '{file_name}'."
    
    def get_documentation(self):
        documentation = """
Virtual File System (VFS) Commands:

1. CREATE_FILE <file_name> <content>
   - Creates a new file with the given name and content.

2. READ_FILE <file_name> <page> [INCLUDE_SURROUNDING] [SURROUNDING_CHARS <num_chars>]
   - Reads the specified page of the file. Optionally, include surrounding content from adjacent pages with the specified number of characters.

3. UPDATE_FILE <file_name> <page> <new_content>
   - Updates the specified page of the file with the new content.

4. SAVE_TO_DISK <file_name> [file_path]
   - Saves the file to disk at the specified file path. If no file path is provided, it will use the file name as the file path.

5. LIST_FILES
   - Lists all the files in the VFS.

6. DELETE_FILE <file_name>
   - Deletes the specified file from the VFS.

7. APPEND_TO_FILE <file_name> <content>
   - Appends the given content to the specified file.

8. RENAME_FILE <old_name> <new_name>
   - Renames the specified file to the new name.

9. GET_FILE_INFO <file_name>
   - Retrieves information about the specified file, such as the number of pages and total size.

10. REORGANIZE_PAGES <file_name>
    - Reorganizes the pages of the specified file.

11. DUMP_ALL [dump_directory]
    - Dumps all virtual files to the specified directory. If no directory is provided, it will use the default "dump" directory.

To execute a command, type the command followed by its arguments. For example:
CREATE_FILE example.txt This is an example file.
"""
        return documentation

    def execute_command(self, command):
        command_parts = command.split()
        if not command_parts:
            return "Error: Empty command."

        command_name = command_parts[0].upper()
        args = command_parts[1:]

        if command_name == "CREATE_FILE":
            if len(args) < 2:
                return "Error: CREATE_FILE requires at least 2 arguments."
            return self.create_file(args[0], " ".join(args[1:]))

        elif command_name == "READ_FILE":
            if len(args) < 2:
                return "Error: READ_FILE requires at least 2 arguments."
            include_surrounding = "INCLUDE_SURROUNDING" in args
            if include_surrounding:
                args.remove("INCLUDE_SURROUNDING")
            surrounding_chars_index = next((i for i, x in enumerate(args) if x == "SURROUNDING_CHARS"), None)
            if surrounding_chars_index is not None and surrounding_chars_index + 1 < len(args):
                surrounding_chars = int(args[surrounding_chars_index + 1])
                args = args[:surrounding_chars_index] + args[surrounding_chars_index + 2:]
            else:
                surrounding_chars = 100
            return self.read_file(args[0], int(args[1]), include_surrounding, surrounding_chars)

        elif command_name == "UPDATE_FILE":
            if len(args) < 3:
                return "Error: UPDATE_FILE requires at least 3 arguments."
            return self.update_file(args[0], int(args[1]), " ".join(args[2:]))

        elif command_name == "SAVE_TO_DISK":
            if len(args) < 1:
                return "Error: SAVE_TO_DISK requires at least 1 argument."
            return self.save_to_disk(args[0], args[1] if len(args) > 1 else None)

        elif command_name == "LIST_FILES":
            return self.list_files()

        elif command_name == "DELETE_FILE":
            if len(args) < 1:
                return "Error: DELETE_FILE requires at least 1 argument."
            return self.delete_file(args[0])

        elif command_name == "APPEND_TO_FILE":
            if len(args) < 2:
                return "Error: APPEND_TO_FILE requires at least 2 arguments."
            return self.append_to_file(args[0], " ".join(args[1:]))

        elif command_name == "RENAME_FILE":
            if len(args) < 2:
                return "Error: RENAME_FILE requires at least 2 arguments."
            return self.rename_file(args[0], args[1])

        elif command_name == "GET_FILE_INFO":
            if len(args) < 1:
                return "Error: GET_FILE_INFO requires at least 1 argument."
            return self.get_file_info(args[0])

        elif command_name == "REORGANIZE_PAGES":
            if len(args) < 1:
                return "Error: REORGANIZE_PAGES requires at least 1 argument."
            return self.reorganize_pages(args[0])

        elif command_name == "DUMP_ALL":
            return self.dump_all(args[0] if args else None)

        else:
            return f"Error: Unknown command '{command_name}'."


def show_functionality():
    vfs = VirtualFileSystem()

    # Create a file
    print(vfs.create_file("test.txt", "This is a test file with more than 2000 characters..." * 100))
    # Read the first page with surrounding content
    print(vfs.read_file("test.txt", 0, include_surrounding=True, surrounding_chars=100))

    # Update the first page
    print(vfs.update_file("test.txt", 0, "This is an updated test file with more than 2000 characters..." * 100))

    # Save the file to disk
    print(vfs.save_to_disk("test.txt", "output.txt"))

    # List files
    print(vfs.list_files())

    # Append content to the file
    print(vfs.append_to_file("test.txt", "This is appended content."))

    # Rename the file
    print(vfs.rename_file("test.txt", "renamed_test.txt"))

    # Get file information
    print(vfs.get_file_info("renamed_test.txt"))

    # Delete the file
    print(vfs.delete_file("renamed_test.txt"))

if __name__ == "__main__":
    show_functionality()