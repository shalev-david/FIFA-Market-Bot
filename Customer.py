from os import listdir, mkdir
from pickle import load

class Customer:

    def __init__(self):
        # Name, Email & Password
        self.name = None
        self.email = None
        self.password = None
        # the cookies used for logging in
        self.cookies = None
        # Money earned so far
        self.money_earned = None
        # Money Goal
        self.goal = None
        # If new Customer - default false
        self.new = False
        # items bought
        self.bought = {}
        # settings
        self.sett = None
        '''
        Platforms
        ---------
        1 - PS
        2 - XBOX
        3 - PC
        '''
        self.platform = None

    '''
    Load an existing customer from the list
    '''
    def load_customer(self):
        # list every customer
        dir = listdir("Customers/")
        count = 1
        for d in dir:
            print(f"{count}) {d}")
            count+=1
        # pick user
        p = int(input("Pick a Customer: ")) -1
        dir = dir[p]
        
        #load the settings to the system
        f = open(f"Customers/{dir}/settings.set", 'r')
        settings = f.readlines()
        f.close()
        '''
        Structer of Settings
        0 | Email
        1 | Password
        2 | Platform
        3 | Goal
        4 | Money Earned
        '''
        #save the values in the object
        self.name = dir
        self.email = settings[0].strip('\n')
        self.password = settings[1].strip('\n')
        self.platform = int(settings[2])
        self.goal = int(settings[3])
        self.money_earned = int(settings[4])
        print(f"Money Earned before the bot: {str(self.money_earned)}")
        f = open(f"Customers/{dir}/cookies.pkl", "rb")
        self.cookies = load(f)
        f.close()
          
    '''
    Create a new Customer
    '''
    def create_customer(self):
        #Get the settings from the Customer
        self.name = input("Enter The Customer's Name: ")
        self.email = input("Enter The Customer's Email: ")
        self.password = input("Enter The Customer's Password: ")
        self.platform = input("Choose The Platform:\n    1)PS\n    2)XBOX\n    3)PC\nOption: ")
        self.goal = input("Enter Money Goal: ")
        self.money_earned = 0
        self.new = True
        
        #create the settings file
        settings = [f'{self.email}\n', f'{self.password}\n', f'{self.platform}\n', f'{self.goal}\n', "0\n"]
        mkdir(f"Customers/{self.name}")
        f = open(f"Customers/{self.name}/settings.set", 'w')
        f.writelines(settings)
        f.close()



