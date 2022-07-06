import re
import collections

REGX1 = " ?<td >([A-Z]+[a-z]+)</td> <td>([0-9,]+)</td>"


class Name:

    def __init__(self, *args):
        """ Constructor for Name class """
        # data structures
        self.myList = []
        boys_combined = collections.defaultdict(int)
        girls_combined = collections.defaultdict(int)

        try:
            count_global = 0  # total num of lines
            for file_name in args:

                # social security office data
                with open(file_name) as name_data:
                    # data structures
                    list_from_file = []  # all lines from one file
                    count_local = 0  # num of lines per file

                    compiled_regex = re.compile(REGX1 + REGX1)
                    try:
                        while True:
                            g1 = next(name_data)
                            # boolean
                            search_result = re.search(compiled_regex, g1)

                            if search_result:

                                tuple_names = (
                                    search_result.group(1),
                                    int(search_result.group(2).replace(",", "")),
                                    search_result.group(3),
                                    int(search_result.group(4).replace(",", "")),
                                )
                                list_from_file.append(tuple_names)

                                boys_combined[tuple_names[0]] += tuple_names[1]

                                girls_combined[tuple_names[2]] += tuple_names[3]

                                count_local += 1
                                count_global += 1
                                # print(count_local, tuple_names)  # DEBUG

                    except StopIteration:

                        print(
                            "Found",
                            count_local,
                            "data for each gender in file_name",
                            str(file_name),
                        )

                        count_local = 0

                # add file list to main list
                self.myList.append(list_from_file)

        except FileNotFoundError:

            print(
                "FileNotFoundError: file",
                file_name,
                "not found. Program terminated.\n",
            )

            raise SystemExit
        except AttributeError:
            print(
                "AttributeError: File",
                file_name,
                "does not contain proper data. Program terminated.\n",
            )

            raise SystemExit

        # data structures
        self.list_combined = list(
            zip(
                {
                    name: num_of_names
                    for name, num_of_names in sorted(
                        boys_combined.items(),
                        key=lambda item: item[1],
                        reverse=True,
                    )
                }.items(),
                {
                    name: num_of_names
                    for name, num_of_names in sorted(
                        girls_combined.items(),
                        key=lambda item: item[1],
                        reverse=True,
                    )
                }.items(),
            )
        )
        # print("list_combined=",self.list_combined) # DEBUG

        self.list_separate = list(zip(*self.myList))
		# print("myList=", self.myList)  # DEBUG

    def get_size(self):
        """Decorator function prints iterable count/items
        and prettifies output."""

        def wrapper(*args, **kwargs):
            print("\n" + 40 * "-")
            result = self(*args, **kwargs)

            print(len(list(result)))
            print()

            return result

        return wrapper

    @get_size
    def search_by_name(self, name, gender):
        """Search_by_name returns a generator,
        with n that match user input string and gender."""
        if gender == "M":
            col = 0
        elif gender == "F":
            col = 2
        decades = "(80s)", "(90s)", "(00s)"

        d1 = {
            names_stats[col]: ["--", "--"]
            for lists in self.myList
            for names_stats in lists
            if name.title() in names_stats[col]
        }

        for i, lists in enumerate(self.myList):
            for j, names_stats in enumerate(lists):
                try:
                    d1[names_stats[col]] += [decades[i] + str(j)]

                    if len(d1[names_stats[col]]) > len(self.myList):
                        d1[names_stats[col]].pop(0)

                except KeyError:
                    continue
        # print("type(d1)=", type(d1), "\nd1=", d1, "\n")  # DEBUG
        return d1


    def search_by_popularity(self, limit, is_by_decade):
        """Search_by_popularity returns a generator, containing user set limit
        of top popular names, either all time or sorted by decade."""
        # data structures
        if is_by_decade == False:

            return (
                (i + 1, elem)
                for i, elem in enumerate(
                    [(elem[0] + elem[1]) for elem in self.list_combined]
                )
                if i < limit
            )

        else:
            return (elem for i, elem in enumerate(self.list_separate) if i < limit)

# run app
n = Name("1980s.txt", "1990s.txt", "2000s.txt")
