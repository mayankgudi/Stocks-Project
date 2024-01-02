import csv
import math

MENU = '''\nSelect an option from below:
            (1) Display all companies in the New York Stock Exchange
            (2) Display companies' symbols
            (3) Find max price of a company
            (4) Find the company with the maximum stock price
            (5) Find the average price of a company's stock
            (6) quit
    '''
WELCOME = "Welcome to the New York Stock Exchange.\n"


def open_file():
    '''Docstring'''
    while True:
        price = input("\nEnter the price's filename: ")
        try:
            price = open(price)

            break
        except:
            print("\nFile not found. Please try again.")
            continue

    while True:
        security = input("\nEnter the security's filename: ")
        try:
            security = open(security)

            break
        except:
            print("\nFile not found. Please try again.")
            continue

    return price, security


def read_file(securities_fp):
    '''Docstring'''
    names = set()
    thedict = {}
    empty = []

    data = securities_fp.readlines()
    for line in data[1:]:
        pp = []

        line = line.split(",")

        if len(line) == 10:
            word1 = line[1] + ',' + line[2]
            word = line[6] + ',' + line[7]

            pp.append(word1)
            pp.append(line[4])
            pp.append(line[5])
            pp.append(word)
            pp.append(line[8])
        else:
            word = line[5] + ',' + line[6]
            pp.append(line[1])
            pp.append(line[3])
            pp.append(line[4])
            pp.append(word)
            pp.append(line[7])

        for num, value in enumerate(pp[3]):

            if value == '"':
                pp[3] = pp[3].replace('"', "")
                pp[0] = pp[0].replace('"', "")
                pp[1] = pp[1].replace('"', "")
                pp[2] = pp[2].replace('"', "")

        pp.append([])

        thedict[line[0]] = pp

        thedict = {key.replace('"', ''): val for key, val in thedict.items()}

        names.add(pp[0])
    names = list(names)
    for i, name in enumerate(list(names)):
        names[i] = names[i].replace('"', "")
        names[i] = names[i].replace(",reports", "")
    names = set(names)

    return names, thedict


def add_prices(master_dictionary, prices_file_pointer):
    '''Docstring'''
    test = []
    data = prices_file_pointer.readlines()
    for line in data[1:]:
        line = line.split(",")
        for key in master_dictionary:
            if line[1] == key:
                test.append(line[0])
                test.append(float(line[2]))
                test.append(float(line[3]))
                test.append(float(line[4]))
                test.append(float(line[5]))

                list1 = master_dictionary[key]
                list1[5].append(test)
                test = []


def get_max_price_of_company(master_dictionary, company_symbol):
    '''Docstring'''

    try:
        value = master_dictionary[company_symbol]

        the_tuple = []
        thelist = value[5]

        maximum = 0
        max_date = 0
        for boo in thelist:
            if boo[4] > maximum:
                maximum = boo[4]
                max_date = boo[0]
            if boo[4] == maximum:
                if boo[0] > max_date:
                    max_date = boo[0]
                    maximum = boo[4]
            else:
                continue
        the_tuple.append(maximum)
        the_tuple.append(max_date)
        the_tuple = tuple(the_tuple)

        return the_tuple

    except:
        return None, None


def find_max_company_price(master_dictionary):
    '''Docstring'''
    test = []
    test_name = []
    for key in master_dictionary:
        bum = get_max_price_of_company(master_dictionary, key)
        test_name.append(key)
        test.append(bum)

    maxitest = max(test)
    ind = test.index(maxitest)
    name = test_name[ind]
    num = maxitest[0]

    final = (name, num)

    return final


def get_avg_price_of_company(master_dictionary, company_symbol):
    '''Docstring'''
    zero = 0
    count = 0
    doink = []
    try:
        test = master_dictionary[company_symbol]
        for key in master_dictionary:
            if key == company_symbol:
                value = master_dictionary[key]
                pop = value[5]
                if pop == []:
                    return zero
                else:
                    for a in pop:
                        num = a[4]
                        doink.append(num)
                        count += 1
            else:
                continue
        final = sum(doink)
        final = final / count
        final = round(final, 2)
    except:
        return zero

    return final


def display_list(dislist):  # "{:^35s}"
    '''Docstring'''

    change = []
    dislist = list(dislist)
    dislist.sort()
    length = len(dislist)

    for x in (dislist):

        change.append(x)

        if len(change) == 3:
            print("{:^35s}{:^35s}{:^35s}".format(change[0], change[1], change[2]))
            change = []

    if length % 3 == 0:
        pass
    if length % 3 == 1:
        print("{:^35s}\n".format(dislist[-1]))
    else:
        print("\n")


def main():
    print(WELCOME)

    price_open, security_open = open_file()
    name_set, code_dict = read_file(security_open)

    add_prices(code_dict, price_open)

    while True:
        print(MENU)
        menu = input("\nOption: ")
        if (menu == "1"):
            print("\n{:^105s}".format("Companies in the New York Stock Market from 2010 to 2016"))
            display_list(name_set)
            continue
        if (menu == "2"):
            print("\ncompanies' symbols:")
            code_list = []
            for code in code_dict:
                code_list.append(code)

            display_list(code_list)
            continue
        if (menu == "3"):
            while True:
                comp_symbol = input("\nEnter company symbol for max price: ")
                result = get_max_price_of_company(code_dict, comp_symbol)
                result = list(result)
                num = result[0]
                date = result[1]
                if num == None or date == None:
                    print("\nError: not a company symbol. Please try again.")
                    continue
                if num == 0 or num == 0.00:
                    print("\nThere were no prices.")
                    break
                else:
                    print("\nThe maximum stock price was ${:.2f} on the date {:s}/\n".format(float(num), str(date)))
                    break
            continue
        if (menu == "4"):
            result = find_max_company_price(code_dict)
            print("\nThe company with the highest stock price is {:s} with a value of ${:.2f}\n".format(result[0], result[1]))
            continue
        if (menu == "5"):
            while True:
                option = input("\nEnter company symbol for average price: ")
                result = get_avg_price_of_company(code_dict, option)
                if result == 0:
                    print("\nError: not a company symbol. Please try again.")
                    continue
                else:
                    break
            print("\nThe average stock price was ${:.2f}.\n".format(result))
            continue
        if (menu == "6"):
            exit()
        else:
            print("\nInvalid option. Please try again.")
            continue


if __name__ == "__main__":
    main()
