import threading
import tkinter as tk
from dealer_5 import dealer_5_func
from tkinter import messagebox as mb
def command():
    dealer_5_func()
    mb.showinfo("success", "Сесію було успішно створено")
    win.quit()


def mdealer():
    global dealer
    global var
    var = 1
    dealer = tk.Toplevel()
    dealer.resizable(width=False, height=False)
    dealer.configure(width=400, height=350, bg="#26242f")
    pls = tk.Label(dealer, text="Вітаємо в програмі Дилер!\nВведіть параметри сесії:", justify=tk.CENTER,
                   font="Helvetica 12 bold", bg="darkgray")
    pls.place(relx=0.25, rely=0.04)

    lAmount = tk.Label(dealer, text="Кількість учасників: ", font="Helvetica 12")
    lAmount.place(relheight=0.10, relwidth=0.48, relx=0.05, rely=0.25)
    eAmount = tk.Entry(dealer, font="Helvetica 14", justify=tk.CENTER)
    eAmount.place(relwidth=0.43, relheight=0.1, relx=0.53, rely=0.25)
    eAmount.focus()

    lThreshold = tk.Label(dealer, text="Порогова кількість: ", font="Helvetica 12")
    lThreshold.place(relheight=0.10, relwidth=0.48, relx=0.05, rely=0.39)
    eThreshold = tk.Entry(dealer, font="Helvetica 14", justify=tk.CENTER)
    eThreshold.place(relwidth=0.43, relheight=0.1, relx=0.53, rely=0.39)
    eThreshold.focus()

    lTime = tk.Label(dealer, text="Час голосування: ", font="Helvetica 12")
    lTime.place(relheight=0.10, relwidth=0.48, relx=0.05, rely=0.53)
    eTime = tk.Entry(dealer, font="Helvetica 14", justify=tk.CENTER)
    eTime.place(relwidth=0.43, relheight=0.1, relx=0.53, rely=0.53)
    eTime.focus()

    lSafety = tk.Label(dealer, text="Параметр безпеки: ", font="Helvetica 12")
    lSafety.place(relheight=0.10, relwidth=0.48, relx=0.05, rely=0.67)

    b1024 = tk.Radiobutton(dealer, text="Середній", font="Helvetica 12", variable=var, value=1024)
    b1024.place(relheight=0.10, relwidth=0.215, relx=0.53, rely=0.67)

    b2048 = tk.Radiobutton(dealer, text="Високий", font="Helvetica 12", variable=var, value=2048)
    b2048.place(relheight=0.10, relwidth=0.215, relx=0.745, rely=0.67)

    log = tk.Button(dealer, text="Генерувати ключі", font="Helvetica 14 bold", command=command, justify=tk.CENTER)
    log.place(relx=0.3, rely=0.85)

global win
win = tk.Tk()
win.title("Дилер")
win.withdraw()
dealer = None
mdealer()
callback_done = threading.Event()
win.mainloop()