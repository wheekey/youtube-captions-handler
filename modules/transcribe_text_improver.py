import re

import Levenshtein

from handle_functions import HandleFunctions
from text_helper import TextHelper
from typing import List


class Letter:
    def __init__(self, letter: str):
        self.letter = letter
        self.punctuations = ''

    def contains_white_space(self) -> bool:
        return ' ' in self.punctuations or '\n' in self.punctuations

    def add_punctuation(self, punctuation_char: str):
        self.punctuations += punctuation_char

    def get_formatted_char(self) -> str:
        return self.letter + self.punctuations


class LetterListManager:
    @staticmethod
    def create_letters_list(raw_line: str) -> List[Letter]:
        result = []
        for i, char in enumerate(raw_line):
            if i == 0:
                cap_letter = Letter(char)
                result.append(cap_letter)
            if re.match(r'[a-zA-Z]+', char) and i != 0:
                cap_letter = Letter(char)
                result.append(cap_letter)
            elif i != 0:
                cap_letter.add_punctuation(char)
        return result


class CaptionLine:
    def __init__(self, raw_line: str, line_number: int):
        self.raw_line = raw_line
        self.caption_letters = LetterListManager.create_letters_list(raw_line)
        self.line_number = line_number
        self.without_punctuation = TextHelper.leave_only_letters(self.raw_line)
        self.len_without_punctuation = len(self.without_punctuation)
        self.__start_pos_in_cap_text = 0
        self.__end_pos_in_cap_text = 0
        # Оставшийся текст, который нужно отформатировать
        self.left_unformatted_text = self.without_punctuation
        self.correct_unformatted_text = self.without_punctuation
        self.is_formatted = False
        self.formatted_text = ''
        self.checked = False
        self.checked_twice = False

    def has_left_unformatted_text(self) -> bool:
        return self.left_unformatted_text != ''

    @property
    def start_pos_in_cap_text(self):
        return self.__start_pos_in_cap_text

    @start_pos_in_cap_text.setter
    def start_pos_in_cap_text(self, start_pos_in_cap_text):
        self.__start_pos_in_cap_text = start_pos_in_cap_text

    @property
    def end_pos_in_cap_text(self):
        return self.__end_pos_in_cap_text

    @end_pos_in_cap_text.setter
    def end_pos_in_cap_text(self, end_pos_in_cap_text):
        self.__end_pos_in_cap_text = end_pos_in_cap_text

    def is_new_line(self) -> bool:
        return self.raw_line == '\n'


class PunctuationSentence:
    def __init__(self, original_sentence: str):
        self.original_sentence = original_sentence
        self.without_punctuation = TextHelper.leave_only_letters(self.original_sentence)
        self.len_without_punctuation = len(self.without_punctuation)
        self.unused_original_sentence = original_sentence
        self.letters = LetterListManager.create_letters_list(self.original_sentence)

    def letters_to_string(self, letters: List[Letter]) -> str:
        result = ''
        for letter in letters:
            result += letter.get_formatted_char()
        return result

    def get_part_of_sentence(self, letters_count: int) -> str:
        """
        Возвращает строку, которая включает в себя нужное количество символов
        Прежде чем делить текст, нам нужно сначала определить, конец ли это слова.
        Если нет, то отрезаем меньше.
        :param letters_count:
        :return:
        """
        last_index_with_space = 0

        for i, letter in enumerate(self.letters):
            if i < letters_count:
                if letter.contains_white_space():
                    last_index_with_space = i

        if last_index_with_space ==0:
            return ''

        result = self.letters_to_string(self.letters[:last_index_with_space + 1])
        self.letters = self.letters[last_index_with_space + 1:]

        return result.strip()


class CaptionLineListManager:
    def prepare_captions(self, captions: list) -> List[CaptionLine]:
        """
        :return: list
        """
        result = []
        for i in range(len(captions)):
            result.append(CaptionLine(captions[i], i))
        return result

    def captions_to_string(self, captions: List[CaptionLine]) -> str:
        result = ''
        for caption in captions:
            result = result + caption.left_unformatted_text
        return result

    def can_we_correct_captions(self, distance: int) -> bool:
        return distance <= 10

    def correct_caption_list(self, sentence: PunctuationSentence, captions: List[CaptionLine]) -> bool:
        """
        Корректировать можно только первый caption или только последний
        :param sentence:
        :param captions:
        :return:
        """
        captions_str = self.captions_to_string(captions)
        deleted_substr_at_start = ''
        deleted_substr_at_end = ''
        sentence_dist = 0

        for i in range(len(captions_str)):
            sentence_dist = Levenshtein.distance(captions_str, sentence.without_punctuation)
            wo_end_char_dist = Levenshtein.distance(captions_str[:-1], sentence.without_punctuation)
            wo_start_char_dist = Levenshtein.distance(captions_str[1:], sentence.without_punctuation)
            if sentence_dist >= wo_end_char_dist:
                deleted_substr_at_end = captions_str[-1:] + deleted_substr_at_end
                captions_str = captions_str[:-1]
            if sentence_dist > wo_start_char_dist:
                deleted_substr_at_start += captions_str[:1]
                captions_str = captions_str[1:]

        if not self.can_we_correct_captions(sentence_dist):
            return False

        self.correct_captions_at(captions, deleted_substr_at_start)
        self.correct_captions_at(captions, deleted_substr_at_end, False)

        return True

    def correct_captions_at(self, captions: List[CaptionLine], substr_to_del: str, is_at_start=True) -> bool:
        """
        Метод, который подрежет результирующий текст слева или справа
        :param captions:
        :param substr_to_del:
        :return:
        """
        if substr_to_del == '':
            return False

        to_cut_text = substr_to_del
        for caption in captions:
            to_cut_text = self.remove_reduntant_text_part(caption, to_cut_text, is_at_start)
        return True

    def is_similar_strings(self, str1: str, str2: str, at_start_to_cut=True) -> bool:
        len_to_cut = TextHelper.define_smallest_len_to_cut(str1, str2)
        if at_start_to_cut:
            if len(str1) == len_to_cut:
                if str2.startswith(str1):
                    return True
                else:
                    return False
            else:
                if str1.startswith(str2):
                    return True
                else:
                    return False
        else:
            if len(str1) == len_to_cut:
                if str2.endswith(str1):
                    return True
                else:
                    return False
            else:
                if str1.endswith(str2):
                    return True
                else:
                    return False

    def remove_reduntant_text_part(self, caption: CaptionLine, to_cut_text: str, at_start: bool) -> str:
        """
        Удаляем только ту часть, которая осталась лишней и неотформатированной.
        Возвращает подстроку, которую нужно еще удалить
        :return:
        """
        len_to_cut = TextHelper.define_smallest_len_to_cut(caption.left_unformatted_text, to_cut_text)
        if caption.left_unformatted_text == '':
            return to_cut_text

        if self.is_similar_strings(caption.left_unformatted_text, to_cut_text, at_start):
            if at_start:
                splitted_text_tuple = TextHelper.cut_text_from_start(caption.left_unformatted_text, len_to_cut)
            else:
                splitted_text_tuple = TextHelper.cut_text_from_end(caption.left_unformatted_text, len_to_cut)
        else:
            return to_cut_text

        caption.left_unformatted_text = splitted_text_tuple[1]
        caption.correct_unformatted_text = splitted_text_tuple[0]

        # Корректируем оставшуюся длину для удаления.
        return TextHelper.cut_text_from_start(to_cut_text, len_to_cut)[0]


class TranscribeTextImprover:
    def __init__(self, captions: list, script_raw_sentences: list, output_filename: str):
        self.output_filename = output_filename
        self.script_raw_sentences = script_raw_sentences
        self.captions = captions

    def start(self):
        cm = CaptionLineListManager()
        script_sentences = self.prepare_punctuation_file_sentences()
        captions_prepared = cm.prepare_captions(self.captions)
        # Берем script строку без пунктуации:
        for script_sentence in script_sentences:
            caption_list = self.find_caption_list_which_best_suit_for_sentence(script_sentence, captions_prepared)
            # Корректи7руем совпавшие captions
            if cm.correct_caption_list(script_sentence, caption_list):
                self.prepare_formatted_text_for_captions(script_sentence, caption_list)
        self.save_result(captions_prepared)

    def save_result(self, captions: List[CaptionLine]):
        for caption in captions:
            if caption.raw_line == '\n':
                HandleFunctions.save_str_to_file(self.output_filename, '\n')
            elif caption.formatted_text.strip() == '':
                HandleFunctions.save_str_to_file( self.output_filename, 'RAW ' + caption.formatted_text + '\n')
            else:
                HandleFunctions.save_str_to_file(self.output_filename, caption.formatted_text + '\n')


    def prepare_formatted_text_for_captions(self, script_sentence: PunctuationSentence,
                                            captions: List[CaptionLine]):
        """
        Метод, который уже вставит пропорционально текст в объекты CaptionLine
        :arg
        """
        for caption in captions:
            part_of_text = script_sentence.get_part_of_sentence(len(caption.correct_unformatted_text))

            # TODO Подправим концовку
            caption.formatted_text += part_of_text + " "
            if caption.left_unformatted_text == '':
                caption.left_unformatted_text = ''
                caption.is_formatted = True

    def define_percent_of_sentence(self, script_sentence: PunctuationSentence, caption: CaptionLine) -> int:
        return int(float(len(caption.correct_unformatted_text)) / float(script_sentence.len_without_punctuation) * 100)

    def find_caption_list_which_best_suit_for_sentence(self, punctuation_file_sentence: PunctuationSentence,
                                                       captions_prepared: List[CaptionLine]) -> List[CaptionLine]:
        """
        Метод, который вернет список CaptionLine, который
        содержит необходимые строки для форматирования.
        """
        result = []
        result_string_len = 0
        for caption_prepared in captions_prepared:

            if  not caption_prepared.checked_twice and caption_prepared.left_unformatted_text != '' and not caption_prepared.is_formatted and TextHelper.has_similar_substring(
                    caption_prepared.left_unformatted_text, punctuation_file_sentence.without_punctuation):
                # Собираем длину строки
                result_string_len += len(caption_prepared.left_unformatted_text)

                if caption_prepared.checked:
                    caption_prepared.checked_twice = True
                caption_prepared.checked = True

                result.append(caption_prepared)
                if result_string_len > punctuation_file_sentence.len_without_punctuation:
                    break

        return result

    def prepare_punctuation_file_sentences(self) -> List[PunctuationSentence]:
        """
        Формируем словарь соответствия PunctuationSentence оригинальное, предложение без пунктуации и пробелов.
        :return: list
        """
        result = []
        for script_raw_sentence in self.script_raw_sentences:
            result.append(PunctuationSentence(script_raw_sentence))

        return result
