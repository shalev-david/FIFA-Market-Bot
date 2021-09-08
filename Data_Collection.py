from navigation import start_search, navigate_to_search
import pandas as pd
from datetime import date, datetime
import calendar
from csv import writer
from time import sleep

start_price = {"GOLD-COMMON":1000, "GOLD-RARE":2300}


def scrap_market(d, c, quality, rarity, start_price):
    '''
    Scrap the market and try to find the price for an item
    For example - try to find the current best price to buy Gold Rare Card
    Then save the day and the time with the price
    At the end I'll print the results on a graph and make my decisions
    '''
    # Start in transfer market search
    set_settings(d, quality, rarity, start_price)
    
    '''
    Algorythm
    ---------
    Search the market for the specific card
    Start with Buy now price of [start_price]
    go down from there and check the time that left for each player
    If the time that left is about > 56 Minutes - 
    - this is the current price for this card
    else lower the price and repeat
    '''
    
    try:
        while True:
            with open('Data/data.csv', 'a') as f:
                writer(f).writerow(search_price(d, c))
                f.close()
                sleep(300)
    except KeyboardInterrupt:
        return
    
def set_settings(d, quality, rarity, start_price):
    # First reset previous settings
    d.click('btn-standard', i=8)
    d.WAIT()
    # Set the quality
    d.click('ut-search-filter-control--row', i=0)
    d.wait_for_elems(3, "with-icon")
    d.click('with-icon', i=quality)
    
    # Set the Rarity
    d.click('ut-search-filter-control--row', i=1)
    d.wait_for_elems(3, 'with-icon') 
    d.click('with-icon', i=rarity)
    d.WAIT(0.5)

    # Set start price
    d.send_keys('numericInput', start_price, i=3)
    d.WAIT(0.5)

def search_price(d, platform):
    while(True):
        start_search(d)
        d.wait_for_elems(3, 'time')
        d.WAIT()
        try:
            time = d.text('time', i=0).split(' ')[0]
            try: 
                time = int(time)
                if(time > 56):
                    # our price
                    # go back and save the price
                    navigate_to_search(d)
                    price = int(d.driver.find_elements_by_class_name('numericInput')[3].get_attribute("value").replace(',', ''))
                    return [
                                date.today().strftime('%d/%m/%y'),
                                calendar.day_name[date.today().weekday()],
                                datetime.now().strftime('%H:%M'),
                                platform,
                                price
                            ]
            except:
                # Definitely not our price
                pass
            # decrease the price
            navigate_to_search(d)
            d.click('decrement-value', i=3)
            d.WAIT()
        except:
            # can't find any items
            # increase the price
            navigate_to_search(d)
            d.click('increment-value', i=3)
            d.WAIT()
            pass

def check_price(d, sett):
    navigate_to_search(d)
    '''
    Check the current price for a specific card
    '''
    set_settings(d, sett.quality, sett.rarity, start_price[sett.card])
    sell_price = search_price(d, 0)[4]
    '''
    now check for the best price to buy
    '''
    while(True):
        # Decrease the value
        d.click('decrement-value', i=3)
        d.WAIT(0.3)
        # Check the price
        min_bid_price = int(d.driver.find_elements_by_class_name('numericInput')[3].get_attribute("value").replace(',', ''))
        if(sell_price*0.95 - min_bid_price >= 0):
            # we found our limit
            # the next price can meet our standarts
            # Decrease the value
            d.click('decrement-value', i=3)
            d.WAIT(0.3)
            buy_price = int(d.driver.find_elements_by_class_name('numericInput')[3].get_attribute("value").replace(',', ''))
            return [buy_price, min_bid_price, sell_price]

    




