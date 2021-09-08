from Data_Collection import check_price
qualities = {"GOLD" : 3}
rarities = {"COMMON" : 1, "RARE":2}
class settings:
    
    def __init__(self, d, c):
        self.quality = None
        self.rarity = None
        # number of players to buy in a search
        self.ptb = 10
        # PS
        if(c.platform == 1):
            self.PS()
        self.card = f'{list(qualities.keys())[list(qualities.values()).index(self.quality)]}-{list(rarities.keys())[list(rarities.values()).index(self.rarity)]}'
        prices = check_price(d, self)

        self.buy_price , self.min_bid_price, self.sell_price = prices
        c.sett = self

    def PS(self):
        self.quality = qualities["GOLD"]
        self.rarity = rarities["RARE"]

