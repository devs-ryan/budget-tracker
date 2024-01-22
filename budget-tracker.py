import os
import csv
import math
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

START_DATE = os.getenv('START_DATE')
DEPOSIT_AMOUNT = os.getenv('DEPOSIT_AMOUNT')
DEPOSIT_FREQUENCY_WEEKS = os.getenv('DEPOSIT_FREQUENCY_WEEKS')

MENU_OPTIONS = ['Check Balance (default)', 'Withdrawl', 'Next Deposit Date']
CONFIRM_OPTIONS = ['Cancel (default)', 'Confirm']
WITHDRAWL_FILE_NAME = 'withdrawls.csv'

def printOptions(options):
    for index, option in enumerate(options):
        print(f"[{index + 1}] - {option}")

def getSelection(max):
    print('=========')
    option = input("Choice: ")
    print('=========')
    if option.isdigit() and int(option) <= max:
        return int(option)
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

    weeks = (d2 - d1).days / 7
    depositWeeks = math.floor(weeks) / int(DEPOSIT_FREQUENCY_WEEKS)

    return depositWeeks * int(DEPOSIT_AMOUNT)

def getNextDepositDate():
    startDate = list(map(int, START_DATE.split('-')))
    d1 = datetime(startDate[0], startDate[1], startDate[2])
    d2 = datetime.now()

    daysUntilNextDeposit = 7 - ((d2 - d1).days % 7)
    nextDepositDate = (d2 + timedelta(daysUntilNextDeposit)).strftime('%m/%d/%Y')

    checkBalance()
    print('Deposit Date:', nextDepositDate)
    print('Deposit Amount: $%.2f' % (int(DEPOSIT_AMOUNT) / 2))
    print('Days until next deposit: %d' % daysUntilNextDeposit)

def checkBalance(display = True):
    withdrawlTotal = getWithdrawlTotal()
    totalDeposited = getTotalDeposited()
    balance = totalDeposited - withdrawlTotal
    if display:
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
        print('Allow a negative balance?')
        printOptions(CONFIRM_OPTIONS)
        confirm = getSelection(2)
    else:
        printOptions(CONFIRM_OPTIONS)
        confirm = getSelection(2)

    if confirm == 1:
        print('Transaction aborted')
        return
    
    comment = input("Enter a comment (optional): ")

    # if .csv does not exist create one
    with open(WITHDRAWL_FILE_NAME, 'a+') as data:
        fileWriter = csv.writer(data)
        fileWriter.writerow([datetime.today().date(), amount, comment])

    print('Withdrawl successful, remaining balance: $%.2f' % (balance - amount))

########
# MAIN #
########
if __name__ == "__main__":
    printOptions(MENU_OPTIONS)
    option = getSelection(3)

    if option == 2: withdrawlFromBalance()
    elif option == 3: getNextDepositDate()
    else: checkBalance()
