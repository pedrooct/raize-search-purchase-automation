import json
import time
import os
import csv
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def dataCSV():
    if os.path.exists("cessoes.csv"):
        os.remove("cessoes.csv")
    else:
        print("The file does not exist, continuing...")


def readJson():
    print("Reading credentials for:")
    f = open("credentials.json")
    data = json.load(f)
    f.close()
    print(data["username"])
    return data["username"], data["password"]


def buyCessions(cessios, list, driver):
    print("yeah")


def printPurchasesPossible(balance):
    list = []
    f = open("cessoes.csv")
    data = csv.reader(f)
    next(data)
    balance = balance.replace(",", ".")
    balance = balance.replace(" €", "")
    id = 0
    for row in data:
        price = float(row[12])
        if row[5] == "regular" and price <= float(balance):
            id = id+1
            list.append(
                {"id": id, "name": row[1], "juros": row[9], "preco": row[12]})
            print("id" + str(id) + "Name: "
                  + row[1]+" - Juros:"+row[9]+"€ - Preço:"+row[12]+"€")
    f.close()
    return list


def getCSVlist(username, password):
    print("Reading data from raize, Please wait...")
    path = os.path.dirname(os.path.abspath(__file__))
    options = Options()
    options.headless = True
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", path)
    profile.set_preference(
        "browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
    driver = webdriver.Firefox(
        options=options, firefox_profile=profile, executable_path=path+"/geckodriver")
    driver.get("https://www.raize.pt/login")
    time.sleep(6)
    usernameElement = driver.find_element_by_name("username")
    passwordElement = driver.find_element_by_name("password")
    usernameElement.send_keys(username)
    passwordElement.send_keys(password)
    print("Entering credentials...")
    driver.find_element_by_xpath(
        '//*[@id="page"]/div/div/div/div/div/div/div/div/div[2]/form/button').click()
    time.sleep(6)
    print('Enter your code:')
    code = input()
    codeElement = driver.find_element_by_name("code")
    codeElement.send_keys(code)
    driver.find_element_by_xpath(
        '/html/body/div/div[1]/div/div/div/div/div/div/div/div/div[2]/form/button').click()
    time.sleep(6)
    print("Getting balance")
    money = driver.find_element_by_xpath(
        "/html/body/div/div[1]/div/div/div/div/div[4]/div[2]/div/div[2]/ul/li[1]/div/div[1]/span[3]").text
    driver.find_element_by_xpath(
        '/html/body/div/header/div/nav/div/ul/li[2]/a').click()
    time.sleep(6)
    driver.find_element_by_xpath(
        '/html/body/div/div[1]/div/div/div/div[1]/nav/ul/li[3]/a').click()
    time.sleep(6)
    print("Downloading cessions file")
    driver.find_element_by_xpath(
        '/html/body/div/div[1]/div/div/div/div[2]/div[2]/div/div[2]/a[1]').click()
    time.sleep(10)
    return money, driver


def main():
    dataCSV()
    username, password = readJson()
    balance, driver = getCSVlist(username, password)
    print("Balance:"+balance)
    printPurchasesPossible(balance)


if __name__ == "__main__":
    main()
