import re
import Levenshtein

class TextHelper:

    @staticmethod
    def is_new_line(str: str) -> bool:
        return str == "\n"

    @staticmethod
    def leave_only_letters(str: str) -> str:
        return re.sub(r"[^a-zA-Z]", '', str).lower()

    @staticmethod
    def strings_has_similar_lengths(str1: str, str2: str) -> bool:
        """
        Строки имеют одинаковую длину,
        если разница в длине не превышает 15 символов.
        """
        return abs(len(str1) - len(str2)) <= 15

    @staticmethod
    def is_similar_strings(str1, str2) -> bool:
        return Levenshtein.distance(str1, str2) < 5

    @staticmethod
    def has_similar_substring(str1: str, str2: str) -> bool:
        """
        Сначала берем самую длинную строку из двух
        Потом начинаем удалть по одному символу с двух сторон, если подстроки примерно одинаковые,
        то подстрока существует
        :param substr:
        :param text:
        :return:
        """
        deleted_substr_at_start = ''
        deleted_substr_at_end = ''

        len_to_cut = abs(len(str1) - len(str2))

        if len(str1) > len(str2):
            text_to_cut = str1
            text_to_compare = str2
        else:
            text_to_cut = str2
            text_to_compare = str1

        for i in range(len_to_cut):
            sentence_dist = Levenshtein.distance(text_to_cut, text_to_compare)
            wo_end_char_dist = Levenshtein.distance(text_to_cut[:-1], text_to_compare)
            wo_start_char_dist = Levenshtein.distance(text_to_cut[1:], text_to_compare)
            if sentence_dist >= wo_end_char_dist:
                deleted_substr_at_end = text_to_cut[-1:] + deleted_substr_at_end
                text_to_cut = text_to_cut[:-1]
            if sentence_dist >= wo_start_char_dist:
                deleted_substr_at_start += text_to_cut[:1]
                text_to_cut = text_to_cut[1:]

        res = Levenshtein.distance(text_to_cut, text_to_compare)
        return res < 7

    @staticmethod
    def cut_text_from_start(text: str, to_remove_letters_cnt: int) -> tuple:
        """
        Возвращает set: обрезанную строку и отрезанную часть
        :arg
        """
        result = text[to_remove_letters_cnt:]
        return result, text[:len(result) * -1]

    @staticmethod
    def cut_text_from_end(text: str, to_remove_letters_cnt: int) -> tuple:
        result = text[:(to_remove_letters_cnt * -1)]

        if result == '':
            return text, ''
        else:
            return result, text[to_remove_letters_cnt * -1:]

    @staticmethod
    def define_smallest_len_to_cut( str1: str, str2: str) -> int:
        str1_len = len(str1)
        str2_len = len(str2)
        if str1_len < str2_len:
            return str1_len
        else:
            return str2_len
