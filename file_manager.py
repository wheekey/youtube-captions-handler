


class FileManager:


    @staticmethod
    def get_file_rows(input_file: str) -> list:
        res = []

        with open(input_file) as fp:
            for line in fp:
                res.append(line)
        return res