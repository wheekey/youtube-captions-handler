import re
from typing import List
import math
from file_manager import FileManager
from handle_functions import HandleFunctions
from text_helper import TextHelper


class EnglishSentence():
    def __init__(self, raw_sentence: str):
        self.raw_sentence = raw_sentence.strip()
        self.handled_percent = 0

    def is_handled(self) -> bool:
        return self.handled_percent >= 90

    def add_percent(self, percent: int):
        self.handled_percent = self.handled_percent + percent

    def get_full_len(self) -> int:
        return len(self.raw_sentence)

class RussianSentence():
    def __init__(self, raw_sentence: str):
        self.raw_sentence = raw_sentence.strip()
        self.original_sentence = self.raw_sentence

    def get_part_of_string_by_percent(self, percent: int) -> str:
        if percent >= 90:
            percent = 100

        cut_chars_from_start_cnt = math.floor(len(self.original_sentence) * percent / 100)

        # Бывает, что текст обрезается на половине слова, поэтому нужно его увеличить.
        for i, char in enumerate(self.raw_sentence):
            if i >= cut_chars_from_start_cnt:
                if not TextHelper.is_letter(char) or re.match(r'[.?!,]', char) is not None:
                    cut_chars_from_start_cnt = i
                    break

        result = self.raw_sentence[:cut_chars_from_start_cnt]
        self.raw_sentence = self.raw_sentence[cut_chars_from_start_cnt:]

        if re.match(r'[.?!]', self.raw_sentence) is not None:
            result += self.raw_sentence
            self.raw_sentence = ''
        return result

class CaptionLine():
    def __init__(self, caption_raw: str):
        self.caption_raw = caption_raw.strip()
        self.analyze_caption_line()
        self.formatted_text = ''


    def get_full_len(self) -> int:
        return len(self.caption_raw)

    def analyze_caption_line(self):
        #Сколько предложений
        self.substrings = re.split('[.?!]', self.caption_raw)
        while ("" in self.substrings):
            self.substrings.remove("")
        self.substrings_cnt = len(self.substrings)

    def add_formatted_text(self, text: str):
        if self.formatted_text == '':
            self.formatted_text += text
        else:
            self.formatted_text += ' ' + text

class ToRussianTranscriber():
    def __init__(self, captions_filename: str,  russian_sentences_filename: str, english_sentences_filename: str, output_filename: str):
        self.russian_sentences_filename = russian_sentences_filename
        self.english_sentences_filename = english_sentences_filename
        self.output_filename = output_filename
        self.captions_filename = captions_filename
        self.english_sentences = self.prepare_english_sentences()
        self.russian_sentences = self.prepare_russian_sentences()

    def prepare_english_sentences(self):
        rows = FileManager.get_file_rows(self.english_sentences_filename)
        res = []
        for row in rows:
            res.append(EnglishSentence(row))

        return res

    def prepare_russian_sentences(self):
        rows = FileManager.get_file_rows(self.russian_sentences_filename)
        res = []
        for row in rows:
            res.append(RussianSentence(row))

        return res

    def get_first_not_empty_russian_sentence(self) -> RussianSentence:
        for sent in self.russian_sentences:
            if sent.raw_sentence != '':
                return sent

    def get_first_not_handled_english_sentence(self) -> EnglishSentence:
        for sent in self.english_sentences:
            if not sent.is_handled():
                return sent

    def start(self):
        captions_raw = FileManager.get_file_rows(self.captions_filename)
        result = []

        # Для каждой строки caption определяем номер предложения и  количество символов
        for caption_raw in captions_raw:
            caption_line = CaptionLine(caption_raw)

            if TextHelper.is_new_line(caption_raw):
                result.append(caption_line)
                continue

            if caption_line.substrings_cnt == 1:
                eng_sentence = self.get_first_not_handled_english_sentence()
                percent = int(caption_line.get_full_len() / eng_sentence.get_full_len() * 100)
                eng_sentence.add_percent(percent)
                sentence_part = self.get_first_not_empty_russian_sentence().get_part_of_string_by_percent(percent)
                caption_line.add_formatted_text(sentence_part)

            if caption_line.substrings_cnt > 1:
                for i in range(caption_line.substrings_cnt):
                    eng_sentence = self.get_first_not_handled_english_sentence()
                    len_cap_line = len(caption_line.substrings[i])

                    percent = int(len_cap_line / eng_sentence.get_full_len() * 100)
                    eng_sentence.add_percent(percent)
                    sentence_part = self.get_first_not_empty_russian_sentence().get_part_of_string_by_percent(percent)
                    caption_line.add_formatted_text(sentence_part)

            result.append(caption_line)
        
        self.save_list_to_file(result)

    def save_list_to_file(self, lst: List[CaptionLine]):
        for i, caption in enumerate(lst):
            if caption.formatted_text == '':
                HandleFunctions.save_str_to_file(self.output_filename, '\n')
            else:
                if i + 1 == len(lst) or lst[i+1].formatted_text == '' :
                    HandleFunctions.save_str_to_file(self.output_filename, caption.formatted_text.strip() + '\n')
                else:
                    HandleFunctions.save_str_to_file(self.output_filename, caption.formatted_text.strip() + ' ')
