import re


class SubtitleBeautifier:

    @staticmethod
    def remove_newlines(s: str):
    
        return s.replace('\n', ' ')

class TimeStamp:
    def __init__(self, timestamp='', ms=None):
        if timestamp != '':
            timestamp_list = [int(n) for n in re.split(':|\.', timestamp)]
            self.hours = timestamp_list[0]
            self.minutes = timestamp_list[1]
            self.seconds = timestamp_list[2]
            self.milliseconds = timestamp_list[3]
        if ms is not None:
            self.hours = int((ms // (1000 * 60 * 60)))
            self.minutes = int((ms / (1000 * 60)) % 60)
            self.seconds = int((ms / 1000) % 60)
            self.milliseconds = int(ms % 1000)

    def convert_to_milliseconds(self) -> int:
        """0:00:00.030"""
        return self.hours * 60 * 60 * 1000 + self.minutes * 60 * 1000 + self.seconds * 1000 + self.milliseconds

    def to_string(self) -> str:
        return str(self.hours) + ":" + str(self.minutes).zfill(2) + ":" + str(self.seconds).zfill(2) + "." + str(self.milliseconds).zfill(3)

class TimeLine:
    def __init__(self, timeline='', time_from=None, time_to=None):
        if timeline != '':
            timeline_beautified = re.sub(r'[^0-9.:,]', '', timeline)
            timeline_list = timeline_beautified.split(",")
            self.time_from = TimeStamp(timestamp = timeline_list[0])
            self.time_to = TimeStamp(timestamp = timeline_list[1])
        if time_from is not None and time_to is not None:
            self.time_from = TimeStamp(ms = time_from)
            self.time_to = TimeStamp(ms = time_to)

    def get_difference_in_start_time_between_timelines(self) -> int:
        """
        Return difference in milliseconds between time_to and next time_from.
        """
        return self.time_to.convert_to_milliseconds() - self.time_from.convert_to_milliseconds()

    def split(self, parts_cnt: int, time_len: int) -> list:
        result = []

        time_len_part_size = time_len // parts_cnt
        time_from_ms = self.time_from.convert_to_milliseconds()

        for i in range(parts_cnt):
            time_from = (time_from_ms + (i * time_len_part_size))
            time_to = (time_from_ms + ((i+1) * time_len_part_size))
            result.append(TimeLine(time_from=time_from, time_to=time_to))

        return result

    def to_string(self) -> str:
        return self.time_from.to_string() + "," + self.time_to.to_string()

    @staticmethod
    def is_timeline(s: str) -> bool:
        regexp = re.compile(r'\.[0-9]{3}')
        if regexp.search(s):
            return True

        return False

class SubtitleString:
    subtitle_max_length = 40

    def __init__(self, string_raw: str):
        self.subtitle = SubtitleBeautifier.remove_newlines(string_raw)

    def get_length(self):
        return len(self.subtitle)

    def to_string(self):
        return self.subtitle

    def split_subtitle(self) -> list:
        result = []

        words = self.subtitle.split(" ")
        subtitle_tmp = ''

        for i, word in enumerate(words):
            if len(subtitle_tmp + ' ' + word) > self.subtitle_max_length:
                result.append(SubtitleString(subtitle_tmp))
                subtitle_tmp = word
            else:
                subtitle_tmp = subtitle_tmp + ' ' + word

        if subtitle_tmp != '':
            result.append(SubtitleString(subtitle_tmp))

        return result

    @staticmethod
    def is_subtitle_string(s: str) -> bool:
        regexp = re.compile(r'[^\d]{2,}')
        if regexp.search(s):
            return True

        return False


    def is_large_subtitle(self) -> bool:
        return len(self.subtitle) > self.subtitle_max_length


class Subtitle:
    def __init__(self, subtitle_string: SubtitleString, timeline: TimeLine):
        self.timeline = timeline
        self.subtitle_string = subtitle_string

    def get_subtitle_string_length(self) -> int:
        return self.subtitle_string.get_length()

    def split(self) -> list:
        """
        Делим большие субтитры и формируем таймлайны
        """

        result = []
        splitted_subtitle = self.subtitle_string.split_subtitle()
        time_diff = self.timeline.get_difference_in_start_time_between_timelines()

        splitted_timeline = self.timeline.split(len(splitted_subtitle), time_diff)

        for i, subtitle_part in enumerate(splitted_subtitle):
            result.append(Subtitle(subtitle_part, splitted_timeline[i]))

        return result

    @staticmethod
    def is_subtitle_string(s: str) -> bool:
        return SubtitleString.is_subtitle_string(s)

    @staticmethod
    def is_timeline(s: str) -> bool:
        return TimeLine.is_timeline(s)

    def is_large_subtitle(self) -> bool:
        return self.subtitle_string.is_large_subtitle()
