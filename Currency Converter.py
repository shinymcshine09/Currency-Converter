from tkinter import *
import requests
import bs4

class currency_finder:
    """
    Class that gives the conversion rate of a list of currencies
    either a single conversion (1 dollar to sterling) or from a 
    given amount in a GUI.
    """
    
    def __init__(self):
        """Function that takes care of the GUI 
        aspects of this programme."""
        
        self.root = Tk()
        
        self.root.title("Currency Converter")
        self.root.geometry('250x230')
        
        Label(self.root, text="From", anchor='w').pack(fill='both')
        
        self.clicked1 = StringVar()
        self.clicked2 = StringVar()
        self.clicked1.set("Select a Currency")
        self.clicked2.set("Select a Currency")
        currrencies = [
        "USD - United States dollar",
         "EUR - Euro",
         "JPY - Japanese yen",
         "GBP - Sterling",
         "CHF - Swiss franc",
         "CAD - Canadian dollar",
         "AUD - Australian dollar",
         "NZD - New Zealand dollar",
         "ZAR - South African rand",
         "MXN - Mexican peso",
         "RUB - Russian rouble",
         "INR - Indian rupee",
         "BRL - Brazilian real",
         "SGD - Singapore dollar",
         "EGP - Egyptian pound",
         "FKP - Falkland Islands pound",
         "HKD - Hong Kong dollar"]

        self.drop1 = OptionMenu(self.root, self.clicked1, *currrencies)
        self.drop1.pack()
        
        Label(self.root, text="To", anchor='w').pack(fill='both')
        
        self.drop2 = OptionMenu(self.root, self.clicked2, *currrencies)
        self.drop2.pack()
        
        Label(self.root, text="Amount:", anchor='w').pack(fill='both')
        
        def temp_text(e):
            self.entry3.delete(0, "end")
            self.entry3.config(fg='black')
        
        self.entry3 = Entry(self.root, width=20, fg='grey')
        self.entry3.insert(0, "enter amount to convert")
        self.entry3.bind("<FocusIn>",temp_text)
        self.entry3.pack()
        Button(self.root, text="Convert", command=self.clicker).pack()
        
        Label(self.root, text="Conversion: ").pack()
        self.text = Text(self.root, height=1, width=15, fg='grey')
        self.text.insert(INSERT, "leave blank")
        self.text.pack()
        self.root.mainloop()
        
    def clicker(self):
        """
        Function that deals with the web scrapping and conversion
        of the chosen currency.
        """
        
        self.text.delete(1.0, "end-1c")
        self.text.config(fg='black')
        currency = self.clicked1.get()[:3]
        second_currency = self.clicked2.get()[:3]
        amount = self.entry3.get()
                
        url = "https://www.marketwatch.com/investing/currency/" + currency + second_currency + "?mod=search_symbol"
        
        if currency == "Sel" or second_currency == "Sel":
            return
        
        elif not amount.isnumeric() and not isfloat(amount):
            return
        
        elif currency == second_currency and (amount == "enter amount to convert" or amount == ""):    
            result = 1
            
        elif currency == second_currency and (amount != "" or amount != "enter amount to convert"):
            result = amount
        
        elif amount != "" and amount != "enter amount to convert":
            soup = bs4.BeautifulSoup(requests.get(url).content, "html.parser")
            currency_data = soup.find("div", class_="intraday__data").find("bg-quote")
            result = float(currency_data.text) * int(float(amount))
        
        else:
            soup = bs4.BeautifulSoup(requests.get(url).content, "html.parser")
            currency_data = soup.find("div", class_="intraday__data").find("bg-quote")
            result = currency_data.text
        
        self.text.insert("end-1c", round(float(result), 2))
    
def isfloat(number):
    """
    Function that returns if the given variable is convertable
    to a float or is a float.
    """
        
    try:
        float(number)
        return True
    except ValueError:
        return False
    
cf = currency_finder()