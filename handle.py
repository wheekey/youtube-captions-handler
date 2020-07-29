import os

from handle_functions import HandleFunctions as hF
from modules.transcribe_text_improver import TranscribeTextImprover
from file_manager import FileManager


if __name__ == "__main__":
    print(
        "Enter operation ("
        "1 - remove timelines, "
        "2 - concat translate with timelines, "
        "3 - prepare timelines string length):"
        "4 - improve english translate")
    operation = int(input())

    if operation == 1:
        input_file = 'files/captions.sbv'
        output_file = 'files/captions_without_timelines.sbv'
        hF.remove_timelines(input_file, output_file)

    if operation == 2:
        input_file = 'files/captions.sbv'
        output_file = 'files/captions_concatted_eng.sbv'
        # print("Enter translated subs file...")
        subs_file = 'files/captions_without_timelines.sbv'
        hF.concat_translate_with_timelines(input_file, output_file, subs_file)

    if operation == 3:
        input_file = 'files/captions_concatted_rus.sbv'
        output_file = 'files/result.sbv'
        hF.prepare_timelines_string_length(input_file, output_file)

    if operation == 4:
        input_file = 'files/captions_without_timelines.sbv'
        punctuation_file = 'files/punctuation.txt'
        output_file = os.getcwd() + '/files/captions_without_timelines_improved.sbv'

        transcribe_text_improver = TranscribeTextImprover(FileManager.get_file_rows(input_file), FileManager.get_file_rows(punctuation_file), output_file)
        transcribe_text_improver.start()
