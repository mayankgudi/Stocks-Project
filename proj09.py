###########################################################
#  Computer Project #9
#
#  Algorithm
#    open_file function
#    all the other functions
#    main function
#       asks for menu input
#       asks for more input depending on choice
#       displays prints depending on choice
#       if user inputs 6, exits code
#
###########################################################


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
    '''This function opens the file that is inputted'''
    while True:
    # starts while loop for reprompts
        price = input("\nEnter the price's filename: ")
        # prompts for prices file
        try:
            price = open(price)
            # attempts to open the file

            break
        except:
            print("\nFile not found. Please try again.")
            # if file doesn't open, error prompt is printed and input prompt is reprompted
            continue

    while True:
        # starts while loop for reprompts
        security = input("\nEnter the security's filename: ")
        # prompts for security file
        try:
            security = open(security)
            # attempts to open the file
            break
        except:
            print("\nFile not found. Please try again.")
            # if file doesn't open, error prompt is printed and input prompt is reprompted
            continue

    return price, security
    # returns the two opened files


def read_file(securities_fp):
    '''This function reads the security file pointer and returns the names set and the structure for the master dictionary'''
    names = set()
    thedict = {}
    empty = []
    # initilize sets, lists, and dictionaries. Whether used or not I like to keep them here

    data = securities_fp.readlines()
    # reads file line by line
    for line in data[1:]:
    # starts for loop for each line, skipping the first header line
        pp = []
        # initialize the list here because it gets reset every loop

        line = line.split(",")
        # splits at the commas

        if len(line) == 10:
        # this if statement is for the companies that have a comma in the name.
        # this is necesary because the comma created a problem when using the split method above.
            word1 = line[1] + ',' + line[2]
            # combines the names that are split by a comma
            word = line[6] + ',' + line[7]
            # combines the city and state which were split by a comma

            pp.append(word1)
            pp.append(line[4])
            pp.append(line[5])
            pp.append(word)
            pp.append(line[8])
            # appends all values to a list
        else:
        # the else is for companies that dont have a comma in their name
            word = line[5] + ',' + line[6]
            # combines the city and state which were split by a comma
            pp.append(line[1])
            pp.append(line[3])
            pp.append(line[4])
            pp.append(word)
            pp.append(line[7])
            # appends all values to a list

        for num, value in enumerate(pp[3]):
        # this for loop gets rid of the quotations around the words
            if value == '"':
                pp[3] = pp[3].replace('"', "")
                pp[0] = pp[0].replace('"', "")
                pp[1] = pp[1].replace('"', "")
                pp[2] = pp[2].replace('"', "")

        pp.append([])
        # appends the empty list at the end of the list for future use

        thedict[line[0]] = pp
        # adds to the final dictionary

        thedict = {key.replace('"', ''): val for key, val in thedict.items()}
        # the line above gets rid of the quotations around the key strings

        names.add(pp[0])
        # adds names to the names set
    names = list(names)
    # converts to a list for easier use
    for i, name in enumerate(list(names)):
    # this for loop gets rid of the quotations
        names[i] = names[i].replace('"', "")
        # gets rid of quotations around the names in the set
        names[i] = names[i].replace(",reports", "")
        # gets rid of the ",reports" at the end of some names
    names = set(names)
    # converts back to a set to be returned

    return names, thedict


def add_prices(master_dictionary, prices_file_pointer):
    '''This function creates the final master dictionary'''
    test = []
    # initializes the list
    data = prices_file_pointer.readlines()
    # reads file line by line
    for line in data[1:]:
    # starts for loop and skips the header line
        line = line.split(",")
        # splits by comma
        for key in master_dictionary:
        # starts for loop to test for keys
            if line[1] == key:
                test.append(line[0])
                test.append(float(line[2]))
                test.append(float(line[3]))
                test.append(float(line[4]))
                test.append(float(line[5]))
                # if the key matches, then the data is appended to that empty list at the end of the big list

                list1 = master_dictionary[key]
                list1[5].append(test)
                # adds to the empty list in the list
                test = []
                # resets list for the next loop


def get_max_price_of_company(master_dictionary, company_symbol):
    '''This function finds the max price of the country based on the given company symbol'''

    try:
        value = master_dictionary[company_symbol]
        # tests to see if the symbol given is valid

        the_tuple = []
        # initializes list
        thelist = value[5]
        # assigns the fifth index of value, which is a list, to a variable

        maximum = 0
        max_date = 0
        # initialize variables
        for boo in thelist:
            if boo[4] > maximum:
            # if the new value is greater than the previous max, it replaces the max as the new max value, this is to find the highest value for that company
                maximum = boo[4]
                # new max value
                max_date = boo[0]
                # the date of the max value
            if boo[4] == maximum:
            # if the new max value is the same and previous, it finds which is the greater date
                if boo[0] > max_date:
                    max_date = boo[0]
                    maximum = boo[4]
            else:
                continue
        the_tuple.append(maximum)
        the_tuple.append(max_date)
        # appends to new lists
        the_tuple = tuple(the_tuple)
        # converts to tuple for return

        return the_tuple

    except:
        return None, None
        # if the code is invalid, the function returns None, None as the tuple


def find_max_company_price(master_dictionary):
    '''Finds the max price out of all the companies'''
    test = []
    test_name = []
    # initializes lists
    for key in master_dictionary:
        bum = get_max_price_of_company(master_dictionary, key)
        # calls another function to use in this for loop
        test_name.append(key)
        test.append(bum)
        # appends to new lists to keep track

    maxitest = max(test)
    # finds max of the value
    ind = test.index(maxitest)
    # finds index of that max value
    name = test_name[ind]
    # uses the index found in the other list to find the corresponding name
    num = maxitest[0]

    final = (name, num)
    # adds the name and number of the max to a tuple and returns

    return final


def get_avg_price_of_company(master_dictionary, company_symbol):
    '''This function gets the average price of the company given'''
    zero = 0
    count = 0
    doink = []
    # initialize variables
    try:
        test = master_dictionary[company_symbol]
        # tests to see if company symbol is valid
        for key in master_dictionary:
            # starts for loop for each key in the dictionary
            if key == company_symbol:
                # if the key equals the company symbol, then it takee the value of the key
                value = master_dictionary[key]
                pop = value[5]
                # pop is given the value of the fifth index in the list
                if pop == []:
                    # if pop is empty though, the function returns zero
                    return zero
                else:
                    for a in pop:
                    # if pop is not empty, the for loop runs and find the price and adds to a list
                        num = a[4]
                        doink.append(num)
                        count += 1
            else:
                continue
        final = sum(doink)
        # sum of list is found
        final = final / count
        # average of list is found and returned after rounding
        final = round(final, 2)
    except:
        # if company symbol doesn't work, returns zero
        return zero

    return final


def display_list(dislist):  # "{:^35s}"
    '''This string is purely to display the first and second options of the main function'''

    change = []
    # initilize list
    dislist = list(dislist)
    # converts to a list to sort
    dislist.sort()
    length = len(dislist)
    # finds length

    for x in (dislist):

        change.append(x)
        # adds value to list

        if len(change) == 3:
        # once the length of the list hits 3, it prints the first 3 names
            print("{:^35s}{:^35s}{:^35s}".format(change[0], change[1], change[2]))
            change = []
            # resets list for next 3 values

    if length % 3 == 0:
        pass
    if length % 3 == 1:
    # once the end comes and 1 value is left, that value is then printed
        print("{:^35s}\n".format(dislist[-1]))
    else:
        print("\n")


def main():
    '''The main function. It controls everything above'''
    print(WELCOME)

    price_open, security_open = open_file()
    name_set, code_dict = read_file(security_open)
    add_prices(code_dict, price_open)
    # initializes the variables needed in the future

    while True:
    # starts while loop to properly reprompt the menu
        print(MENU)
        menu = input("\nOption: ")
        # prints and asks for input
        if (menu == "1"):
        # if option 1 is selected this if statement runs
            print("\n{:^105s}".format("Companies in the New York Stock Market from 2010 to 2016"))
            # prints header for the list of companies
            display_list(name_set)
            # uses display_list function to display the companies in the proper format
            continue
            # continue is used to reprompt the menu option
        if (menu == "2"):
        # if option 2 is selected this if statement runs
            print("\ncompanies' symbols:")
            code_list = []
            for code in code_dict:
                code_list.append(code)
            # gathers all the company codes into a list
            display_list(code_list)
            # uses display_list function to display the company codes in the proper format
            continue
            # continue is used to reprompt the menu option
        if (menu == "3"):
        # if option 3 is selected this if statement runs
            while True:
            # starts while loop to properly reprompt the input for company symbol
                comp_symbol = input("\nEnter company symbol for max price: ")
                # asks for input
                result = get_max_price_of_company(code_dict, comp_symbol)
                # runs given input in the get_max_price_of_company function along with the master dictionary
                result = list(result)
                num = result[0]
                date = result[1]
                # gathers the values needed from the result of the function
                if num == None or date == None:
                # if the results are None, then the error message is prompted
                    print("\nError: not a company symbol. Please try again.")
                    continue
                    # continue is used to reprompt the company symbol input
                if num == 0 or num == 0.00:
                # if the results were 0, meaning the company had no stock price ever, message is prompted and code breaks from the while loop
                    print("\nThere were no prices.")
                    break
                else:
                # if the company has a max stock price, the data is inputted into the format of this print statement below
                    print("\nThe maximum stock price was ${:.2f} on the date {:s}/\n".format(float(num), str(date)))
                    break
                    # the code breaks and continues with the menu options
            continue
            # continue is used to reprompt the menu option
        if (menu == "4"):
        # if option 4 is selected this if statement runs
            result = find_max_company_price(code_dict)
            # uses find_max_company_price function and prints results in formatted print statement
            print("\nThe company with the highest stock price is {:s} with a value of ${:.2f}\n".format(result[0], result[1]))
            continue
            # continue is used to reprompt the menu option
        if (menu == "5"):
        # if option 5 is selected this if statement runs
            while True:
            # while loop to properly reprompt the company symbol input
                option = input("\nEnter company symbol for average price: ")
                result = get_avg_price_of_company(code_dict, option)
                # runs through get_avg_price_of_company function with the input and the master dictionary
                if result == 0:
                # if the result is zero, the error message is prompted
                    print("\nError: not a company symbol. Please try again.")
                    continue
                    # continue is used here to reprompt the company symbol input
                else:
                # if all goes well, then the code breaks from the while loop
                    break
            # print statement with the result of the while loop in the proper format
            print("\nThe average stock price was ${:.2f}.\n".format(result))
            continue
            # continue is used to reprompt the menu option
        if (menu == "6"):
        # if option 6 is selected the code will exit
            exit()
        else:
        # if an invalid option is inputted, this error message will print and menu option will reprompt
            print("\nInvalid option. Please try again.")
            continue


if __name__ == "__main__":
    main()