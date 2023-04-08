import os
import csv
import math
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

START_DATE = os.getenv('START_DATE')
DEPOSIT_AMOUNT = os.getenv('DEPOSIT_AMOUNT')
DEPOSIT_FREQUENCY_WEEKS = os.getenv('DEPOSIT_FREQUENCY_WEEKS')

MENU_OPTIONS = ['Check Balance (default)', 'Withdrawl']
CONFIRM_OPTIONS = ['Cancel (default)', 'Confirm']
WITHDRAWL_FILE_NAME = 'withdrawls.csv'

def printOptions(options):
    for index, option in enumerate(options):
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
    print('Current Balance: $%.2f' % balance)
    return balance

def withdrawlFromBalance():
    amount = input("Amount to withdrawl: ")

    # convert amount to 2 decimal places and float / validate
    try:
        amount = math.ceil(float(amount) * 100) / 100
        if amount < 0.01:
            raise Exception
    except Exception:
        print('The amount entered is not valid')
        return

    balance = checkBalance()
    print('Attempting to withdrawl: $%.2f' % amount)

    if balance < amount:
        print('Insufficient balance to make this withdrawl')
        return
    
    printOptions(CONFIRM_OPTIONS)
    confirm = getSelection()

    if confirm == 1:
        print('Transaction aborted')
        return

    
    # if .csv does not exist create one
    with open(WITHDRAWL_FILE_NAME, 'w+') as data:
        file = csv.reader(data)

        if balance < amount:
            return

    # check if withdrawl amount is valid / balance is enough
    # add withdrawl to .csv
    # display remaining balance
    return 'todo'

########
# MAIN #
########
if __name__ == "__main__":
    printOptions(MENU_OPTIONS)
    option = getSelection()

    if option == 1: checkBalance()
    else: withdrawlFromBalance()