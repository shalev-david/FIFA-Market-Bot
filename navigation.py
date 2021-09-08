from driver import By
from time import sleep
from pickle import dump

def login(d, c):
    # Go to the website
    d.driver.get("https://www.ea.com/fifa/ultimate-team/web-app/")
    # Load cookies if needed
    if(not c.new):
        for cookie in c.cookies:
            d.driver.add_cookie(cookie)

    d.wait_for_elem(30, '#Login > div > div > button.btn-standard.call-to-action', by=By.CSS_SELECTOR)
    sleep(3)
    d.click('#Login > div > div > button.btn-standard.call-to-action', by=By.CSS_SELECTOR)

    # Wait for the new page to load
    d.wait_for_elem(30, 'email', by=By.ID)
    # Insert the account details
    d.send_keys('email', c.email, by=By.ID)
    d.send_keys('password', c.password, by=By.ID)
    sleep(0.3)
    d.click('btnLogin', by=By.ID)
    # If it is a new account added to the system wait for confirmation and save the cookies
    if(c.new):
        input("Waiting for comfirmation...\nPress Enter when ready")
        f = open(f'Customers/{c.name}/cookies.pkl', 'wb')
        dump(d.driver.get_cookies(), f)
        f.close()
        d.new = False
    # Logged in
    # Wait for the new page to load
    sleep(7)
    d.WAIT()
    sleep(2)
    d.WAIT()
    print("\nLogged in\n")
    
def navigate_to_search(d):
    navigate_to_transfers(d)
    d.click('ut-tile-transfer-market')
    d.WAIT()
        
def navigate_to_transfers(d):
    d.WAIT(0.1)
    d.click('icon-transfer')
    d.WAIT()

def navigate_to_transfer_list(d):
    navigate_to_transfers(d)
    d.click('ut-tile-transfer-list')
    d.wait_for_elems(3, 'itemList')
    d.WAIT(2)

def navigate_to_transfer_targets(d):
    navigate_to_transfers(d)
    d.click('ut-tile-transfer-targets')
    d.wait_for_elems(3, 'itemList')
    d.WAIT(2)

def start_search(d):
    # Start search
    d.click('call-to-action')
    # Wait for it to load 
    d.wait_for_elems(3, 'listFUTItem')
    d.WAIT()