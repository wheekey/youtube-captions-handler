from file_manager import FileManager
from handle_functions import HandleFunctions


class ToGoogleTranslateCaptionsPreparator:
    def __init__(self, input_filename: str, output_filename: str):
        self.output_filename = output_filename
        self.input_filename = input_filename

    def start(self):
        input_file_str = FileManager.get_file_as_str(self.input_filename)
        input_file_str = self.format_file(input_file_str)
        HandleFunctions.save_str_to_file(self.output_filename, input_file_str)

    def format_file(self, file_str: str) -> str:
        return file_str.replace('\n', ' ').replace('. ', '.\n').replace('!', '!\n').replace('?', '?\n').replace('  ', ' ')
