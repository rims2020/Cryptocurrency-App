import sqlite3
import requests
import json
import tkinter
from tkinter import messagebox, Menu
db=sqlite3.connect('cryptocurrency.sqlite')

cursor=db.cursor()
window=tkinter.Tk()
window.iconbitmap('download.ico')
window.title("CryptoCurrency")
window.configure(bg='gray42')

# cursor.execute("CREATE TABLE IF NOT EXISTS coins(id INTEGER PRIMARY KEY, symbol TEXT, amount INTEGER, price REAL )")
# cursor.execute("INSERT INTO COINS VALUES(1, 'BTC', 2, 3200)")
# cursor.execute("INSERT INTO COINS VALUES(2, 'ETH', 10, 40.05)")
# cursor.execute("INSERT INTO COINS VALUES(3, 'USDT', 75, 25)")
# cursor.execute("INSERT INTO COINS VALUES(4, 'XRP', 100, 10000)")
def main_header():

    label8 = tkinter.Label(window, text="PortID", fg='white', bg='MediumPurple4',font=("Times",18 , 'bold'), relief="groove", padx="1", pady="1", borderwidth=1)
    label8.config(height=2, width=0)
    label8.grid(row=0, column=0, sticky='nsew')

    label1 = tkinter.Label(window, text="Coin Name", fg='white', bg='MediumPurple4',font=("Times",18 , 'bold'), relief="groove", padx="5", pady="5", borderwidth=2)
    label1.config(height=2, width=0)
    label1.grid(row=0, column=1, sticky='nsew')

    label2 = tkinter.Label(window, text="Price", fg='white', bg='MediumPurple4',font=("Times",18 , 'bold'), relief="groove", padx="5", pady="5", borderwidth=2)
    label2.config(height=2, width=0)
    label2.grid(row=0, column=2, sticky='nsew')

    label3 = tkinter.Label(window, text="Coin Owned", fg='white', bg='MediumPurple4',font=("Times",18 , 'bold'), relief="groove", padx="5", pady="5", borderwidth=2)
    label3.config(height=2, width=0)
    label3.grid(row=0, column=3, sticky='nsew')

    label4 = tkinter.Label(window, text="Total Amount Paid", fg='white', bg='MediumPurple4',font=("Times",18 , 'bold'), relief="groove", padx="5", pady="5", borderwidth=2)
    label4.config(height=2, width=0)
    label4.grid(row=0, column=4, sticky='nsew')

    label5 = tkinter.Label(window, text="Current Value", fg='white', bg='MediumPurple4',font=("Times",18 , 'bold'), relief="groove", padx="5", pady="5", borderwidth=2)
    label5.config(height=2, width=0)
    label5.grid(row=0, column=5, sticky='nsew')

    label6 = tkinter.Label(window, text="P/L/coin", fg='white', bg='MediumPurple4',font=("Times",18 , 'bold'), relief="groove", padx="5", pady="5", borderwidth=2)
    label6.config(height=2, width=0)
    label6.grid(row=0, column=6, sticky='nsew')

    label7 = tkinter.Label(window, text="Total\nP/L/coin", fg='white', bg='MediumPurple4',font=("Times",18 , 'bold'), relief="groove", padx="5", pady="5", borderwidth=2)
    label7.config(height=2, width=2)
    label7.grid(row=0, column=7, sticky='nsew')


def navigation():
    def clear_all():
        cursor.execute("DELETE from coins")
        #db.commit()
        messagebox.showinfo("Notification", "Portfolio Cleared!")
        reset()
    def close_app():
        messagebox.showinfo("Notification", "The APP will close!")
        window.destroy()


    menu = Menu(window)
    item=Menu(menu)
    item.add_command(label="Clear Portfolio", command=clear_all)
    item.add_command(label='Close App', command=close_app)
    menu.add_cascade(label='Help', menu=item)
    window.configure(menu=menu)


def reset():

    for frame in window.winfo_children():
        frame.destroy()
    main_header()
    main_prog()


def main_prog():
    api_request=requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=30&convert=USD&CMC_PRO_API_KEY=50f1f6a8-bd1f-4dee-a267-6b3741c68c49")
    api=json.loads(api_request.content)

    cursor.execute("SELECT * FROM COINS")
    coins=cursor.fetchall()

    def colour(amount):
        if amount<=0:
            return "orange red"
        if amount>0:
            return "lawn green"
    def add():

        cursor.execute("INSERT INTO coins(symbol, amount, price) VALUES(?,?,?)",(Entry1.get(), Entry3.get(), Entry2.get()))
        db.commit()
        messagebox.showinfo("ADD","The entry is added")
        reset()
    def delete():
        cursor.execute("DELETE FROM coins WHERE id=?",(Entry4.get(),))
        db.commit()
        messagebox.showinfo("DELETE","The entry is deleted")
        reset()
    def update():
        cursor.execute("UPDATE coins SET symbol=?, amount=?, price=? WHERE id=?",(Entry6.get(), Entry8.get(), Entry7.get(), Entry5.get()))
        db.commit()
        messagebox.showinfo("UPDATE","The entry is UPDATED")
        reset()
    total=0
    row_no=1
    total_pl=0
    current=0
    totalpaid=0
    for i in range(0,5):

       for coin in coins:

          if api["data"][i]["symbol"]==coin[1]:

            total_paid= coin[2]*coin[3]
            current_value=coin[2]*api["data"][i]["quote"]["USD"]["price"]
            current=current+current_value

            pl_percoin=api["data"][i]["quote"]["USD"]["price"]-coin[3]
            total+=pl_percoin
            total_pl+=total
            totalpaid+=total_paid
            label9 = tkinter.Label(window, text=coin[0], fg='white', bg='gray42',font=("Times",16 ), relief="sunken", padx="3", pady="3", borderwidth=2)
            label9.grid(row=row_no, column=0, sticky='nsew')

            label10 = tkinter.Label(window, text=api["data"][i]["name"], fg='white', bg='gray42', font=("Times",16 ), relief="sunken", padx="3", pady="3", borderwidth=2)
            label10.grid(row=row_no, column=1, sticky='nsew')

            label11 = tkinter.Label(window, text="{0:.2f}".format(api["data"][i]["quote"]["USD"]["price"]), fg='white', bg='gray42', font=("Times",16 ), relief="sunken", padx="3", pady="3", borderwidth=2)
            label11.grid(row=row_no, column=2, sticky='nsew')

            label2 = tkinter.Label(window, text="{0:.2f}".format(coin[2]), fg='white', bg='gray42', font=("Times",16 ), relief="sunken", padx="3", pady="3", borderwidth=2)
            label2.grid(row=row_no, column=3, sticky='nsew')

            label3 = tkinter.Label(window, text="{0:.2f}".format(total_paid), fg='white', bg='gray42', font=("Times",16 ), relief="sunken", padx="3", pady="3", borderwidth=2)
            label3.grid(row=row_no, column=4, sticky='nsew')

            label4 = tkinter.Label(window, text="{0:.2f}".format(current_value), fg='white', bg='gray42', font=("Times",16 ), relief="sunken", padx="3", pady="3", borderwidth=2)
            label4.grid(row=row_no, column=5, sticky='nsew')

            label5 = tkinter.Label(window, text="{0:.2f}".format(pl_percoin), fg=colour(float("{0:.2f}".format(pl_percoin))), bg='gray42', font=("Times",16 ), relief="sunken", padx="3", pady="3", borderwidth=2)
            label5.grid(row=row_no, column=6, sticky='nsew')

            label16 = tkinter.Label(window, text="{0:.2f}".format(total), fg=colour(float("{0:.2f}".format(total))), bg='gray42', font=("Times",16 ), relief="sunken", padx="3", pady="3", borderwidth=2)
            label16.grid(row=row_no, column=7, sticky='nsew')

            #label8 = tkinter.Label(window, text="{0:.2f}".format(total), fg='white', bg='gray42', font=("Times",16 ), relief="sunken", padx="5", pady="5", borderwidth=2)
            #label8.grid(row=row_no, column=6, sticky='nsew')

            row_no+=1
    api=" "

    label17 = tkinter.Label(window, text="{0:.2f}".format(total_pl), fg=colour(float("{0:.2f}".format(total_pl))), bg='gray42', font=("Times",16 ), relief="sunken", padx="3", pady="3", borderwidth=2)

    label17.grid(row=row_no+1, column=7, sticky='nsew')
    label18 = tkinter.Label(window, text="{0:.2f}".format(current), fg='white', bg='gray42', font=("Times",16 ), relief="sunken", padx="3", pady="3", borderwidth=2)
    label18.grid(row=row_no+1, column=5, sticky='nsew')
    label9 = tkinter.Label(window, text="{0:.2f}".format(totalpaid), fg='white', bg='gray42', font=("Times",16 ), relief="sunken", padx="3", pady="3", borderwidth=2)
    label9.grid(row=row_no+1, column=4, sticky='nsew')
    Button2 = tkinter.Button(window, text="ADD COIN", fg='white', bg='MediumPurple4',command=add, font=("Times",18 ), relief="groove", padx="6", pady="8", borderwidth=2)
    Button2.grid(row=7, column=6, sticky='nsew')
    Entry1 = tkinter.Entry(window, fg='gray91', bg='gray42', font=("Times",16 ), relief="sunken")
    Entry1.insert(0,'Enter coin symbol ')
    Entry1.grid(row=7, column=1, sticky='nsew')
    Entry2 = tkinter.Entry(window, fg='gray91', bg='gray42', font=("Times",16 ), relief="sunken")
    Entry2.insert(0,'Enter coin price ')
    Entry2.grid(row=7, column=2, sticky='nsew')
    Entry3 = tkinter.Entry(window, fg='gray91', bg='gray42', font=("Times",16 ), relief="sunken")
    Entry3.insert(0,'Enter coins owned ')
    Entry3.grid(row=7, column=3, sticky='nsew')
    Entry4 = tkinter.Entry(window, fg='gray91', bg='gray42', font=("Times",16 ), relief="sunken")
    Entry4.insert(0,'Enter Portfolio ID ')
    Entry4.grid(row=row_no+3, column=0, sticky='nsew')
    Entry5 = tkinter.Entry(window, fg='gray91', bg='gray42', font=("Times",16 ), relief="sunken")
    Entry5.insert(0,'Enter Portfolio ID ')
    Entry5.grid(row=row_no+4, column=0, sticky='nsew')
    Entry6 = tkinter.Entry(window, fg='gray91', bg='gray42', font=("Times",16 ), relief="sunken")
    Entry6.insert(0,'Enter coin symbol ')
    Entry6.grid(row=row_no+4, column=1, sticky='nsew')
    Entry7 = tkinter.Entry(window, fg='gray91', bg='gray42', font=("Times",16 ), relief="sunken")
    Entry7.insert(0,'Enter coin price ')
    Entry7.grid(row=row_no+4, column=2, sticky='nsew')
    Entry8 = tkinter.Entry(window, fg='gray91', bg='gray42', font=("Times",16 ), relief="sunken")
    Entry8.insert(0,'Enter coins owned ')
    Entry8.grid(row=row_no+4, column=3, sticky='nsew')
    Button1 = tkinter.Button(window, text="REFRESH", fg='white', bg='MediumPurple4', command=main_prog, font=("Times",18 ), relief="groove", padx="5", pady="5", borderwidth=2)
    Button1.grid(row=row_no+4, column=7, sticky='nsew')
    Button3 = tkinter.Button(window, text="DELETE", fg='white', bg='MediumPurple4', command=delete, font=("Times",18 ), relief="groove", padx="5", pady="5", borderwidth=2)
    Button3.grid(row=row_no+3, column=6, sticky='nsew')
    Button4 = tkinter.Button(window, text="UPDATE", fg='white', bg='MediumPurple4', command=update, font=("Times",18 ), relief="groove", padx="5", pady="5", borderwidth=2)
    Button4.grid(row=row_no+4, column=6, sticky='nsew')
navigation()
main_header()
main_prog()

window.mainloop()
