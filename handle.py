import os

from handle_functions import HandleFunctions as hF, HandleFunctions
from modules.to_google_translate_captions_preparator import ToGoogleTranslateCaptionsPreparator
from modules.to_russian_transcriber import ToRussianTranscriber
from modules.transcribe_text_improver import TranscribeTextImprover
from file_manager import FileManager


if __name__ == "__main__":
    print(
        "Enter operation ("
        "1 - remove timelines, "
        "2 - concat translate with timelines, "
        "3 - prepare timelines string length):"
        "4 - improve english translate"
        "5 - prepare captions for russian")
 #   operation = int(input())
    operation = 2

    if operation == 1:
        input_file = 'files/captions.sbv'
        output_file = 'files/captions_without_timelines.sbv'
        hF.remove_timelines(input_file, output_file)

    if operation == 2:
        input_file = os.getcwd() + '/files/captions.sbv'
        output_file = os.getcwd() + '/files/result.sbv'
        # print("Enter translated subs file...")
        subs_file = os.getcwd() + '/files/captions_rus_result.sbv'
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

    if operation == 5:
        input_file = os.getcwd() + '/files/captions_without_timelines.sbv'
        output_file = os.getcwd() + '/files/captions_for_google_translate.sbv'

        preparator = ToGoogleTranslateCaptionsPreparator(input_file, output_file)
        preparator.start()

    if operation == 6:
        eng_file = os.getcwd() + '/files/captions_for_google_translate.sbv'
        rus_file = os.getcwd() + '/files/captions_russian_raw.sbv'
        captions_file = os.getcwd() + '/files/captions_without_timelines.sbv'
        output_file = os.getcwd() + '/files/captions_rus_result.sbv'

        transcriber = ToRussianTranscriber(captions_file, rus_file, eng_file, output_file)
        transcriber.start()