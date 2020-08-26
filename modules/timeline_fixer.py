import re

import Levenshtein

from file_manager import FileManager
from handle_functions import HandleFunctions
from subtitle import Subtitle
from text_helper import TextHelper
from typing import List





class TimelinesFixer:
    def __init__(self, input_filename: str, output_filename: str):
        self.input_filename = input_filename
        self.output_filename = output_filename


    def fix(self):
        caption_rows = FileManager.get_file_rows(self.input_filename)

        for i, caption_row in enumerate(caption_rows):
            if Subtitle.is_timeline(caption_row):

                if i + 3 < len(caption_rows):
                    timeline_splitted = caption_row.split(',')
                    timeline_splitted_next = caption_rows[i + 3].split(',')
                    HandleFunctions.save_str_to_file(self.output_filename, timeline_splitted[0] + ',' + timeline_splitted_next[0] + '\n')
                else:
                    HandleFunctions.save_str_to_file(self.output_filename, caption_row)
            else:
                HandleFunctions.save_str_to_file(self.output_filename, caption_row)

