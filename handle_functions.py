from subtitle import Subtitle, SubtitleString, TimeLine
from file_manager import FileManager

class HandleFunctions:

    @staticmethod
    def save_str_to_file(filepath: str, s: str):
        with open(filepath, "a") as myfile:
            myfile.write(s)

    @staticmethod
    def remove_timelines(input_file: str, output_file: str):
        file_rows = FileManager.get_file_rows(input_file)
        for i, file_row in enumerate(file_rows):
            if not Subtitle.is_timeline(file_row):
                HandleFunctions.save_str_to_file(output_file, file_row)

    @staticmethod
    def get_timelines(input_file: str) -> list:
        res = []
        file_rows = FileManager.get_file_rows(input_file)

        for i, file_row in enumerate(file_rows):
            if Subtitle.is_timeline(file_row):
                res.append(file_row)
        return res

    @staticmethod
    def get_translated_lines(input_file: str):
        res = []
        file_rows = FileManager.get_file_rows(input_file)

        for i, file_row in enumerate(file_rows):
            if file_row != '\n':
                res.append(file_row)
        return res

    @staticmethod
    def concat_translate_with_timelines(input_file: str, output_file: str, subs_file: str):
        timelines = HandleFunctions.get_timelines(input_file)
        translated_lines = HandleFunctions.get_translated_lines(subs_file)
        for i, timeline in enumerate(timelines):
            HandleFunctions.save_str_to_file(output_file, timeline)
            HandleFunctions.save_str_to_file(output_file, translated_lines[i])
            HandleFunctions.save_str_to_file(output_file, '\n')

    @staticmethod
    def get_subtitles(file_rows: list) -> list:
        result = []
        timeline_raw = ''
        subtitle_raw = ''
        for i, file_row in enumerate(file_rows):
            if Subtitle.is_timeline(file_row):
                timeline_raw = file_row
            if Subtitle.is_subtitle_string(file_row):
                subtitle_raw = file_row
            if timeline_raw != '' and subtitle_raw != '':
                result.append(Subtitle(SubtitleString(subtitle_raw), TimeLine(timeline_raw)))
                timeline_raw = ''
                subtitle_raw = ''

        return result

    @staticmethod
    def prepare_timelines_string_length(input_file: str, output_file: str):
        result = []
        file_rows = FileManager.get_file_rows(input_file)
        subtitles = HandleFunctions.get_subtitles(file_rows)

        for i, subtitle in enumerate(subtitles):
            if i - 1 < len(subtitles) and subtitle.is_large_subtitle():
                splitted_subtitle_list = subtitle.split()
                result = result + splitted_subtitle_list
            else:
                result.append(subtitle)

        for i, subtitle in enumerate(result):
            HandleFunctions.save_str_to_file(output_file, subtitle.timeline.to_string().strip() + '\n')
            HandleFunctions.save_str_to_file(output_file, subtitle.subtitle_string.to_string().strip() + '\n')
            HandleFunctions.save_str_to_file(output_file, '\n')

