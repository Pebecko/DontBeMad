import sys
import time


class Settings:
    def __init__(self):
        self.writing_time = 0
        self.turn_pause = 0

    def slow_print(self, string):
        for c in string:
            sys.stdout.write(c)
            sys.stdout.flush()
            if self.writing_time > 0:
                time.sleep(self.writing_time)
        print("")
        if self.writing_time > 0:
            time.sleep(0.1)

    def base_options(self, message=""):
        self.slow_print(message)
        option = input()

        if option == "quit" or option == "leave" or option == "exit" or option == "vypnout" or option == "odejít":
            quit()

        elif option == "time" or option == "čas":
            option = "skip"
            while True:
                self.slow_print("Jak rychle chcete aby se text vypisoval:\n"
                                "    [i]nstantně\n"
                                "    [r]ychle\n"
                                "    [p]omalu\n")
                player_option = input()
                if player_option is "i":
                    self.writing_time = 0
                    break
                elif player_option is "r":
                    self.writing_time = 0.005
                    break
                elif player_option is "p":
                    self.writing_time = 0.015
                    break
                else:
                    self.slow_print("Zadaný vstup nesouhlasí s možnostmi.\n")

        elif option == "pause" or option == "pauza":
            option = "skip"
            while True:
                self.slow_print("Jak dlouhou pauzu mezi tahy chcete?\n [celé číslo větší nebo rovno 0]")
                player_option = input()
                try:
                    int(player_option)
                except ValueError:
                    print("Zadaný vstup nesouhlasí s možnostmi.\n")
                else:
                    if int(player_option) < 0:
                        print("Zadaný vstup nesouhlasí s možnostmi.\n")
                    else:
                        self.turn_pause = int(player_option)
                        break

        return option


settings = Settings()
