from sys import stdout
from time import sleep
from csv import reader, DictReader
from pathlib import Path
from color import Color


class Settings:
    def __init__(self):
        self.writing_time = 0
        self.turn_pause = 0
        self.language = "czech"
        self.color_names = []
        self.max_prefix_of_word_length = 3

    def slow_print(self, string, newline=False, no_record=False):
        if not no_record:
            if newline:
                string += "\n"
            for c in string:
                stdout.write(c)
                stdout.flush()
                if self.writing_time > 0:
                    sleep(self.writing_time)
            print("")
            if self.writing_time > 0:
                sleep(0.1)

    def translation(self, item_name, lang=None):
        if lang is None:
            lang = self.language

        # open translations csv file
        csv_file = open(Path(__file__).parent.parent / "data/translations.csv", "r")
        trans = DictReader(csv_file, delimiter=";")

        # search for the item in the file
        for line in trans:
            if line["item"] == item_name:
                translation = line[lang]
                break
        else:
            translation = "*translation_error - item \"{}\" not found*".format(item_name)

        csv_file.close()

        return str(translation)

    def translate_slow_print(self, translating, formatting=(), newline=False, no_record=False):
        self.slow_print(self.translation(translating).format(*formatting), newline, no_record)

    def finding_color_names(self):
        colors = []

        # open colors translations csv file
        csv_file = open(Path(__file__).parent.parent / "data/colors.csv", "r")
        trans = DictReader(csv_file, delimiter=";")

        # finding color names
        for line in trans:
            colors.append(Color(name=line["color"]))

        csv_file.close()

        self.color_names = self.removing_duplicate_colors(colors)

    @staticmethod
    def removing_duplicate_colors(colors):
        new_colors = []

        for color in colors:
            for color_name in new_colors:
                if color.name == color_name.name:
                    break
            else:
                new_colors.append(color)

        return new_colors

    def max_color_name_length(self):
        max_name_length = 0

        for color in self.color_names:
            if len(color.translation) > max_name_length:
                max_name_length = len(color.translation)

        return max_name_length

    def translating_colors(self):
        # looking for color names
        if not self.color_names:
            self.finding_color_names()

        # translating color names
        for color in self.color_names:
            # open translations csv file
            csv_file = open(Path(__file__).parent.parent / "data/colors.csv", "r")
            trans = DictReader(csv_file, delimiter=";")

            # search for the item in the file
            for line in trans:
                if line["color"] == color.name:
                    color.translation = line[self.language]
                    break

            csv_file.close()

        # changing prefixes and suffixes
        separated_colors = []

        for characters_number in range(1, self.max_color_name_length() + 1):
            colors_being_separated = []
            # going from the shortest names to the longest
            for color in self.color_names:
                if len(color.translation) == characters_number:
                    colors_being_separated.append(color)

            for trans_col in colors_being_separated:
                # setting maximum length of colors prefix
                if len(trans_col.translation) > self.max_prefix_of_word_length >= 1:
                    max_prefix_length = self.max_prefix_of_word_length
                else:
                    max_prefix_length = len(trans_col.translation)

                for prefix_string_length in range(1, max_prefix_length + 1):  # len(trans_col.translation)
                    for col in separated_colors:
                        if col.prefix == trans_col.translation[:prefix_string_length]:
                            break
                    else:
                        separated_colors.append(trans_col)
                        trans_col.prefix = trans_col.translation[:prefix_string_length]
                        trans_col.suffix = trans_col.translation[prefix_string_length:]
                        break
                else:
                    color_number = 1
                    while True:
                        for col in separated_colors:
                            if col.prefix == str(color_number):
                                color_number += 1
                                break
                        else:
                            separated_colors.append(trans_col)
                            trans_col.prefix = str(color_number)
                            trans_col.suffix = " " + trans_col.translation
                            break

    def base_options(self, message, formatting=(), translate=True, newline=False, no_record=False):
        # displaying text
        if not translate:
            self.slow_print(message.format(*formatting), newline, no_record)
        else:
            self.translate_slow_print(message, formatting, newline, no_record)

        # getting commands from data/commands.csv
        csv_file = open(Path(__file__).parent.parent / "data/commands.csv", "r")
        trans = reader(csv_file, delimiter=";")

        leaving, language_change, print_time_change, pause_change = [], [], [], []

        # search for the item in the file
        for line in trans:
            if len(line) > 1:
                if line[0] == "quit":
                    leaving = line[1:]
                elif line[0] == "language":
                    language_change = line[1:]
                elif line[0] == "time":
                    print_time_change = line[1:]
                elif line[0] == "pause":
                    pause_change = line[1:]

        csv_file.close()

        # waiting for players input
        option = input()

        # leaving the game
        if option == "quit" or option == "exit" or option in leaving and option != "":
            quit()

        # changing language
        elif option == "language" or option in language_change and option != "":
            csv_file = open(Path(__file__).parent.parent / "data/translations.csv", "r")
            trans_list = reader(csv_file, delimiter=";")

            lang_options, lang_english_names, lang_names = [], [], []

            for line in trans_list:
                if line[0] == "item" and len(line) > 1:
                    lang_english_names = line[1:]
                elif line[0] == "lang_name" and len(line) > 1:
                    lang_names = line[1:]

            for num in range(0, len(lang_english_names)):
                lang_options.append([lang_english_names[num], lang_names[num], str(num + 1)])

            # string formatting
            language_option = self.translation("please_choose_language")
            for lang in lang_options:
                language_option += "\n  [{}] {}".format(lang[2], lang[1])

            # player choosing language
            while len(lang_english_names) > 0:
                self.slow_print(language_option)
                player_option = input()
                for lang_opt in lang_options:
                    if player_option == lang_opt[2]:
                        self.language = lang_opt[0]
                        option = "skip"
                        break
                else:
                    self.slow_print(self.translation("input_error"))

                if option == "skip":
                    break
            else:
                settings.slow_print("error - not enough languages")

            self.translating_colors()

            csv_file.close()

        # changing character printing speed
        elif option == "time" or option in print_time_change and option != "":
            option = "skip"
            while True:
                self.translate_slow_print("how_fast_print")

                player_option = input()

                if player_option is self.translation("how_fast_print_1"):
                    self.writing_time = 0
                    break
                elif player_option is self.translation("how_fast_print_2"):
                    self.writing_time = 0.005
                    break
                elif player_option is self.translation("how_fast_print_3"):
                    self.writing_time = 0.015
                    break
                else:
                    settings.translate_slow_print("input_error")

        # changing pauses lengths between turns
        elif option == "pause" or option in pause_change and option != "":
            option = "skip"
            while True:
                self.translate_slow_print("how_long_pause")
                player_option = input()
                try:
                    int(player_option)
                except ValueError:
                    settings.translate_slow_print("input_error")
                else:
                    if int(player_option) < 0:
                        settings.translate_slow_print("input_error")
                    else:
                        self.turn_pause = int(player_option)
                        break

        return option


settings = Settings()
