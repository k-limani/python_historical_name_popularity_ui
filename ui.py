"""
User interface for displaying / analyzing baby name popularity throughout the 80s, 90s, and 00s
"""

from name import Name

class UI:

    def __init__(self, *file_names):
        """ constructor for UI class """
        self.n1 = Name(*file_names)

    def user_search_by_name(self):
        """search partial or full names, results include all three
        decades and the ranking of the name"""

        usr_input = input("\nEnter gender (M/F): ")
        while True:
            gender = str(usr_input.title().strip())
            if gender not in ("M", "F"):
                usr_input = input("\nWrong entry. \nEnter gender (M/F): ")
                continue
            break
        usr_input = input("\nEnter a name or partial name: ")
        name = str(usr_input.title().strip())
        data_dic = self.n1.search_by_name(name, gender)
        # print("type(data_dic)=", type(data_dic)) # DEBUG
        if not bool(data_dic):  # if it's empty
            print(f'{"No names containing that word found.":36s}')
        else:
            print(f'{"Name":12s} {"Decades and Ranks":<s} ')

            for k in sorted(data_dic.keys()):
                print(
                    f"{k:<13s}{data_dic[k][0]:<12s}{data_dic[k][1]:<12s} {data_dic[k][2]:<12s}"
                )

    def user_search_by_popularity(self):
        """search popular names by decade or combined,
        set the number of names shown"""

        usr_input = input(
            "\n>>> Enter a decade (1980, 1990, or 2000), or press Enter for all three: "
        )

        usr_decade_choice = str(usr_input)
        limit, year_index = -1, -1
        is_by_decade = True
        YRS = ["1980", "1990", "2000"]
        while True:
            if usr_decade_choice in YRS:
                for i, elem in enumerate(YRS):
                    if usr_decade_choice == elem:
                        year_index = i
                print()
                break
            elif usr_decade_choice == "":
                print("All three decades chosen.")
                is_by_decade = False
                print()
                break
            else:

                usr_input = input(
                    "\nWrong entry. \n>>> Enter a decade (1980, 1990, or 2000),\
                    \nor press Enter for all three: "
                )

                usr_decade_choice = str(usr_input)
                continue
        while True:

            usr_input = input(
                ">>> Enter a limit for top names, or press Enter for all: "
            )

            if usr_input in ("", "0"):
                limit = 600
                break
            try:
                limit = int(usr_input)
                if limit < 1 or limit > 600:
                    raise ValueError
                break
            except ValueError:
                print("\nWrong entry.")
        data_gen = self.n1.search_by_popularity(limit, is_by_decade)
        print()
        if year_index != -1:
            print("Showing names for the " + YRS[year_index] + "s.")
        else:
            print("Showing combined names for all three decades.")
        print(f'{"Rank":<6s} {"Name (boy)":15s} {"Name (girl)":14s}')
        try:
            c = 0
            while True:
                top_names = next(data_gen)
                c += 1
                if year_index != -1:

                    print(
                        f"{c:<7d} {top_names[year_index][0]:15s} {top_names[year_index][2]:15s}"
                    )

                else:

                    print(f"{c:<7d}{top_names[1][0]:15s} {top_names[1][2]:15s}")

        except StopIteration:
            print(80 * "-")

    def run(self):
        """main menu of choices"""
        user_input = None

        self._menu = {
            "n": self.user_search_by_name,
            "p": self.user_search_by_popularity,
            "q": (lambda: print("Exited. Thank you.")),
        }

        while user_input != "q":

            print(
                "\nMENU OPTIONS:\nn. Search by name\np. Search by popularity\nq. Quit\n"
            )

            user_input = input(">> Choose an option: ")
            print("Your choice:", user_input)
            try:
                self._menu[str(user_input.strip()).lower()]()
            except AttributeError:
                print("No classes found. Try again.")
            except KeyError:
                print("Invalid choice. Try again.")


file_names = [(str(elem) + "s.txt") for elem in (1980, 1990, 2000)]
app = UI(*file_names)
app.run()
