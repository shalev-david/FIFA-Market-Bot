from anti_captcha import set_anticpatcha_settigns as setup_anticaptcha
from Customer import Customer
from driver import Driver
from navigation import *
from Strategies import *
from Data_Collection import scrap_market
from settings import settings

def main():
    
    #first set the anticaptcha extansion
    driver = Driver()
    setup_anticaptcha(driver)
    # then choose between an existing customer or a new one 
    state = int(input("1)Existing Customer\n2)New Customer\nChoose an option: "))
    customer = Customer()
    if(state == 1):
        customer.load_customer()
    else:
        customer.create_customer()
    
    login(driver, customer)
    navigate_to_search(driver)
    while(True):
        try:
            #scrap_market(driver, customer, 3, 2, 2500)
            settings(driver, customer)
            PS(driver, customer)
        except:
            driver.driver.refresh()
            driver.WAIT(60)
            navigate_to_search(driver)

    input()





if __name__ == "__main__":
    main()