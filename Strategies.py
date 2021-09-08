from driver import By
from random import random
from navigation import *
from Data_Collection import check_price
from settings import settings



def PS(d, c):
    '''
    Strategy on PS consoles
    ----------------------- 
    bid on gold common players about 1300-1800 and sell for 2200 with start bid of 1900 

    ''' 

    # Start this when already in transfer tab
    # Set the settings for the search
    while (True):
        PS_set_settings(d, c.sett)
        for i in range(5):
            start_search(d)
            bid_search(d, c.sett.buy_price, c.sett.ptb)

            # After bidding go back and sell
            navigate_to_transfers(d)
            # Sleep for a minute
            d.WAIT()

            # Go to the Transfer Targets tab and fight for the items
            navigate_to_transfer_targets(d)
            fight_for_bids(d, c.sett.buy_price)
            sell_from_transfer_targets(d, c)

            # Go back to the Transfer List and try to see if we sold something
            navigate_to_transfer_list(d)
            clear_sold(d, c)
            navigate_to_search(d)

            print(f"Money Earned So Far: {c.money_earned}\n")
        sleep(180)
        d.caution = False
        settings(d, c)


def XBOX_set_settings(d):
    # Start this when already in transfer tab

    # Set quality to Gold
    d.click('ut-search-filter-control--row', i=0)
    d.wait_for_elems(3, "with-icon")
    d.click('with-icon', i=3)
    d.WAIT(0.5)

    # Set Rarity to common
    d.click('ut-search-filter-control--row', i=1)
    d.wait_for_elems(3, 'with-icon')
    d.click('with-icon', i=1)
    d.WAIT(0.5)


    # Set bid max price to 350
    d.send_keys('numericInput', 350, i=1)
    d.WAIT(0.5)

def PS_set_settings(d, sett):
    # Start this when already in Transfer Market Search tab
    # First reset previous settings
    d.click('btn-standard', i=8)
    d.WAIT()
    # Set quality
    d.click('ut-search-filter-control--row', i=0)
    d.wait_for_elems(3, "with-icon")
    d.click('with-icon', i=sett.quality)
    d.WAIT(0.5)

    # Set Rarity to Rare
    d.click('ut-search-filter-control--row', i=1)
    d.wait_for_elems(3, 'with-icon') 
    d.click('with-icon', i=sett.rarity)
    d.WAIT(0.5)

    # Set bid min price to 1300
    #d.send_keys('numericInput', 1300, i=0)
    #d.WAIT(0.5)

    # Set bid max price
    d.send_keys('numericInput', sett.buy_price, i=1)
    d.WAIT(0.5)

def bid_search(d, max_bid, count):
    '''
    there are 60 elements with the class 'auctionValue'
    every |elem%3 = 1| is the current bid price
    it can be either '---' or a number
    we will buy every element that answer the terms
    '''
    j=1
    
    while(j>0):
        i = 1
        while(i <  60 and count!=0):
            price = d.text('auctionValue', i=i).split('\n')[1].replace(',', '')
            if(price == '---' or int(price)<max_bid):
                # Perfect match - lets buy it
                d.click('listFUTItem', i=int(i/3))
                d.WAIT(0.1)
                d.click('bidButton')
                d.WAIT(0.1)
                # try to see of we ran into a trouble
                try:
                    #Notification negative
                    # If there isn't an error it means that we might be in trouble
                    text = d.text('negative')
                    if(d.caution):
                        if(text == 'Too many actions have been taken, and use of this feature has been temporarily disabled.'):
                        # we have temporary ban - get into lockdown for a few minutes
                            lockdown(300)
                    else: 
                        # Else turn on the flag and return
                        if(text == 'Too many actions have been taken, and use of this feature has been temporarily disabled.'):
                            d.caution = True
                    return
                except:
                    count-=1
                sleep(random() + random() + 0.25)

            i+=3
        d.click('next')
        d.WAIT()
        j-=1   

def sell_from_transfer_targets(d, c):
    #start when inside the Transfer Targets tab
    try:
        while(True):
            # Try to see if we've succeeded and bought some items
            bought = d.driver.find_elements_by_class_name('itemList')[2]
            # If we did go and sell every player
            bought.find_elements_by_class_name('won')[0].click()
            d.WAIT(0.2)
            d.click('accordian')
            d.WAIT(0.1)
            d.wait_for_elem(3, 'subContent')
            # Save how much players in which price was bought
            name = d.text('main-view')
            if(name == ''): name = d.text('main-view')
            price = int(d.text('subContent').replace(',', ''))
            if(name in c.bought): c.bought[name].append(price)
            else: c.bought[name] = [price]

            # Sell the items
            d.click('numericInput', i=0)
            d.WAIT(0.1)
            d.send_keys('numericInput', c.sett.min_bid_price, i=0)
            d.click('numericInput', i=1)
            d.WAIT(0.1)
            d.send_keys('numericInput', c.sett.sell_price, i=1)
            d.WAIT(0.1)
            d.click('call-to-action', i=4)

            d.WAIT()
    except:
        pass
    # Clear the Expired Items
    try:
        d.click('call-to-action', i=3)
    except:
        pass

def clear_sold(d, c):
    #start from inside the Transfer List tab
    #try to see if we sold something
    try:
        count = 0
        while(True):
            # Try to see if we've succeeded and sold some items
            sold = d.driver.find_elements_by_class_name('itemList')[0]
            # If we did go and add the profit
            sold.find_elements_by_class_name('won')[count].click()
            d.WAIT()
            name = d.text('main-view', i=count)
            if(name == ''): name = d.text('main-view', i=count)
            if(name in c.bought):
                price = int(d.text('subContent', i=1).replace(',', ''))
                bought = c.bought[name].pop(-1)
                c.money_earned += (price*0.95) - bought
                if(not c.bought[name]):
                    c.bought.pop(name, None)
            count+=1
    except:
        # Write to file
        # Change the money earned
        with open(f'Customers/{c.name}/settings.set', 'r') as file:
            # read a list of lines into data
            data = file.readlines()
            file.close()
        data[4] = str(int(c.money_earned)) + '\n'

        with open(f'Customers/{c.name}/settings.set', 'w') as file:
            file.writelines( data )
            file.close()
    
        #clear the sold list
        try:
            d.click('call-to-action')
        except:
            pass
        return

def lockdown(time, d, c):
    print("In Lockdown\n")
    sleep(time)

def fight_for_bids(d, max_bid):
    #start when inside the Transfer Targets tab
    try:
        i=0
        while(True):
            # first check if there are items with bids and that we are not trying for nothing
            bids = d.driver.find_elements_by_class_name('itemList')[0]

            # if an error is thrown here that means that there are no players left in the active bids list
            bids.find_elements_by_class_name('listFUTItem')[0]

            try:
                # check if we got outbid by someone and add another bid if it is < max_bid
                outbid = bids.find_elements_by_class_name('outbid')[i]
                outbid.click()
                d.WAIT(0.5)
                # check the price
                price = int(d.text('subContent', i=1).replace(',', ''))
                if(price < max_bid):
                    # bid again
                    d.click('call-to-action', i=4)
                    #check if we are in cooldown
                    try:
                        text = d.text('negative')
                        if(d.caution):
                            if(text == 'Too many actions have been taken, and use of this feature has been temporarily disabled.'):
                            # we have temporary ban - get into lockdown for a few minutes
                                lockdown(300)
                        else: 
                            # Else turn on the flag and return
                            if(text == 'Too many actions have been taken, and use of this feature has been temporarily disabled.'):
                                d.caution = True
                    except:
                        pass
                    i=0
                else:
                    # unwatch item
                    # first check if the item is already processing - if so skip to the next one
                    if(d.text('subContent', i=0) == 'Processing...'):
                        i+=1
                        continue
                    #else unwatch the player
                    d.click('watch')
                    i=0
                d.WAIT(1.5)
            except:
                pass

    except:
        return
