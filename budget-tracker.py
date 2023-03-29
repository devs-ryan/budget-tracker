import os
import csv
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

START_DATE = os.getenv('START_DATE')
DEPOSIT_AMOUNT = os.getenv('DEPOSIT_AMOUNT')
DEPOSIT_FREQUENCY_WEEKS = os.getenv('DEPOSIT_FREQUENCY_WEEKS')

MENU_OPTIONS = ['Check Balance (default)', 'Withdrawl']
WITHDRAWL_FILE_NAME = 'withdrawls.csv'

def printMenuOptions():
    for index, option in enumerate(MENU_OPTIONS):
        print(f"[{index + 1}] - {option}")

def getSelection():
    option = input("Choice: ")
    if option == '2':
        return 2
    return 1

def getWithdrawlTotal():
    if not os.path.isfile(WITHDRAWL_FILE_NAME):
        return 0

    total = 0
    with open(WITHDRAWL_FILE_NAME, 'r') as data:
        for line in csv.reader(data):
                total += float(line[1])

    return total

def getTotalDeposited():
    startDate = list(map(int, START_DATE.split('-')))
    d1 = datetime(startDate[0], startDate[1], startDate[2])
    d2 = datetime.now()

    monday1 = (d1 - timedelta(days=d1.weekday()))
    monday2 = (d2 - timedelta(days=d2.weekday()))

    weeks = (monday2 - monday1).days / 7
    depositWeeks = weeks / int(DEPOSIT_FREQUENCY_WEEKS)

    return depositWeeks * int(DEPOSIT_AMOUNT)


def checkBalance():
    withdrawlTotal = getWithdrawlTotal()
    totalDeposited = getTotalDeposited()
    balance = totalDeposited - withdrawlTotal
    print('Current Balance: $' + "%.2f" % balance)
    return balance

def withdrawlFromBalance():
    amount = input("Amount to withdrawl: ")
    # if .csv does not exist create one
    # check if withdrawl amount is valid / balance is enough
    # add withdrawl to .csv
    # display remaining balance
    return 'todo'

########
# MAIN #
########
if __name__ == "__main__":
    printMenuOptions()
    option = getSelection()

    if option == 1: checkBalance()
    else: withdrawlFromBalance()