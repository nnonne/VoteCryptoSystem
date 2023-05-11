import time
from threshold_crypto_library import *
from firebase_admin import firestore, credentials
import threading
import uuid
import tkinter as tk
from tkinter import messagebox as mb
from client_key_params import client_key_params_func


def prepare_crypto():
    def prepare_values_str_to_int(values):
        p = int(values[u'p'])
        q = int(values[u'q'])
        g = int(values[u'g'])
        n = values[u'n']
        t = values[u't']
        pub_key = int(values[u'pub_key'])
        share = [values[u'share'][0], int(values[u'share'][1])]
        return p, q, g, n, t, pub_key, share

    def regenerate_crypto_params_objects(p, q, g, n, t, pub_key, share):
        key_params = KeyParameters(p, q, g)
        thresh_params = ThresholdParameters(t, n)
        pub_key = PublicKey(pub_key, key_params)
        share = KeyShare(share[0], share[1], key_params)
        return key_params, thresh_params, pub_key, share

    with open('key_parameters.json') as file:
        key_parameters = json.load(file)

    p, q, g, n, t, pub_key, share = prepare_values_str_to_int(key_parameters)
    key_params, thresh_params, pub_key, share = regenerate_crypto_params_objects(p, q, g, n, t, pub_key, share)
    return key_params, thresh_params, pub_key, share


def clear_collection(db):

    data = db.collection(u'messages_id')
    for d in data.stream():
        d.reference.delete()
    data = db.collection(u'parts')
    for d in data.stream():
        d.reference.delete()

def adm():
    global isAdmin
    isAdmin = True

def mLogin():
    global login, isAdmin
    login = tk.Toplevel()
    login.title("Учасник")
    login.resizable(width=False, height=False)
    login.configure(width=400, height=250)

    pls = tk.Label(login, text="Вітаємо у Vote Crypto chat!\nВведіть ваше ім'я:", justify=tk.CENTER,
                   font="Helvetica 14 bold")
    pls.place(relheight=0.2, relx=0.15, rely=0.1)

    lName = tk.Label(login, text="Ім'я: ", font="Helvetica 12 bold")
    lName.place(relheight=0.15, relx=0.1, rely=0.35)
    eName = tk.Entry(login, font="Helvetica 14")
    eName.place(relwidth=0.4, relheight=0.1, relx=0.5, rely=0.35)
    eName.focus()

    lCode = tk.Label(login, text="Код запрошення: ", font="Helvetica 12 bold")
    lCode.place(relheight=0.15, relx=0.1, rely=0.48)
    eCode = tk.Entry(login, font="Helvetica 14")
    eCode.place(relwidth=0.4, relheight=0.1, relx=0.5, rely=0.48)
    eCode.focus()

    bAdmin = tk.Checkbutton(login, text="", variable=isAdmin, onvalue=True, command=lambda: adm())
    bAdmin.place(relx=0.45, rely=0.65)
    lAdmin = tk.Label(login, text="Я адміністратор ", font="Helvetica 12 bold")
    lAdmin.place(relheight=0.15, relx=0.1, rely=0.625)
    log = tk.Button(login, text="Login", font="Helvetica 14 bold", command=lambda: logIn(eName.get()))
    log.place(relx=0.4, rely=0.80)

def logIn(name):
    # Ця функція наразівідкриває лише функцію layout, яка є головним вікном. Після того як буде зроблено програма для адміна,
    # вона буде віівдкривати два цих вікна, які працюють незалежно один від одного.
    global user_name
    login.destroy()
    user_name = name
    layout(name)
    #admin("Pasha")

def finish():
    sendButton('Сесію було завершено адміністратором')

def layout(name):

    global textCons
    global entryMsg

    win.deiconify()
    win.title("Учасник")
    win.resizable(width=False, height=False)
    if isAdmin:
        win.configure(width=470, height=600, bg="#17202A")
        labelHead = tk.Label(win, bg="#17202A", fg="#EAECEE", text=name, font="Helvetica 13 bold", pady=5)
        labelHead.place(relwidth=1)

        line = tk.Label(win, width=450, bg="#ABB2B9")
        line.place(relwidth=1, rely=0.07, relheight=0.012)

        textCons = tk.Text(win, width=20, height=2, bg="#17202A", fg="#EAECEE", font="Helvetica 14", padx=5, pady=5)
        textCons.place(relheight=0.745, relwidth=1, rely=0.08)

        labelBottom = tk.Label(win, bg="#ABB2B9", height=100)
        labelBottom.place(relwidth=1, rely=0.825)
        entryMsg = tk.Entry(labelBottom, bg="#2C3E50", fg="#EAECEE", font="Helvetica 13")

        entryMsg.place(relwidth=0.74, relheight=0.03, rely=0.002, relx=0.011)
        entryMsg.focus()

        buttonMsg = tk.Button(labelBottom, text="Надіслати", font="Helvetica 10 bold", width=20, bg="#ABB2B9",
                              command=lambda: sendButton(entryMsg.get()))
        buttonMsg.place(relx=0.77, rely=0.002, relheight=0.03, relwidth=0.22)
        textCons.config(cursor="arrow")

        btnFinishSession = tk.Button(labelBottom, text="Завершити сесію", font="Helvetica 10 bold", width=20,
                                     bg="red", command=lambda: sendButton('Сесію було завершено адміністратором'))
        btnFinishSession.place(relx=0.0, rely=0.035, relheight=0.03, relwidth=1)
    else:
        win.configure(width=470, height=550, bg="#17202A")
        labelHead = tk.Label(win, bg="#17202A", fg="#EAECEE", text=name, font="Helvetica 13 bold", pady=5)
        labelHead.place(relwidth=1)

        line = tk.Label(win, width=450, bg="#ABB2B9")
        line.place(relwidth=1, rely=0.07, relheight=0.012)

        textCons = tk.Text(win, width=20, height=2, bg="#17202A", fg="#EAECEE", font="Helvetica 14", padx=5, pady=5)
        textCons.place(relheight=0.745, relwidth=1, rely=0.08)

        labelBottom = tk.Label(win, bg="#ABB2B9", height=80)
        labelBottom.place(relwidth=1, rely=0.825)

        entryMsg = tk.Entry(labelBottom, bg="#2C3E50", fg="#EAECEE", font="Helvetica 13")

        entryMsg.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        entryMsg.focus()

        buttonMsg = tk.Button(labelBottom, text="Надіслати", font="Helvetica 10 bold", width=20, bg="#ABB2B9",
                              command=lambda: sendButton(entryMsg.get()))
        buttonMsg.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)
        textCons.config(cursor="arrow")


    scrollbar = tk.Scrollbar(textCons)

    scrollbar.place(relheight=1, relx=0.974)
    scrollbar.config(command=textCons.yview)
    textCons.config(state=tk.DISABLED)


def sendButton(message):

    global doc_ref
    global user_name
    global entryMsg
    entryMsg.delete(0, tk.END)

    try:
        if message != "":

            # Each raw message is encrypted by public key
            encrypted = ThresholdCrypto.encrypt_message(message, pub_key)
            encrypted_message = encrypted.enc
            v = str(encrypted.v)
            c = str(encrypted.c)

            doc_ref = db.collection(u'messages_id').document(str(uuid.uuid4()))

            data = db.collection(u'parts')
            for d in data.stream():
                d.reference.delete()

            doc_ref.set({u'user': user_name, u'message': encrypted_message, u'v': v, u'c': c, u'topic': message})

    except:
        pass


def on_snapshot(collection_snapshot, changes, read_time):

    for doc in collection_snapshot:
        if doc.id not in messages_id:

            if True:
                t1 = time.perf_counter()
                messages_id.add(doc.id)
                doc = doc.to_dict()
                topic = doc[u'topic']
                if topic == 'Сесію було завершено адміністратором':
                    # Тут треба зробитивспливаюче повідомлення в якому сказано що адміністратор завершив сесію. Після цього через пару секунд закрити вікно (як кнопка червоного хрестика)
                    mb.showinfo("сесію завершено", "Сесію було завершено адміністратором")
                    time.sleep(3)
                    win.quit()
                    break
                user = doc[u'user']
                want_to_read = wantToRead(topic, user)
                t2 = time.perf_counter()

                encrypted_message = EncryptedMessage(int(doc[u'v']), int(doc[u'c']), doc[u'message'])

                if want_to_read and float(t2-t1) < 6:

                    partial_decryption = ThresholdCrypto.compute_partial_decryption(encrypted_message, share)
                    x = partial_decryption.x
                    v_y = str(partial_decryption.v_y)

                    doc_ref = db.collection(u'parts').document(str(uuid.uuid4()))
                    doc_ref.set({u'user': user_name, u'x': x, u'v_y': v_y})

                time.sleep(5)

                partial_decryptions = []
                read_ref2 = db.collection(u'parts')

                for part in read_ref2.stream():
                    part = part.to_dict()
                    part_decryption = PartialDecryption(part[u'x'], int(part[u'v_y']))
                    partial_decryptions.append(part_decryption)

                try:
                    decrypted_message = ThresholdCrypto.decrypt_message(partial_decryptions, encrypted_message,
                                                                        thresh_params, key_params)
                    showMessage(f'Голосування на тему "{decrypted_message}" було прийнято.')
                except:
                    showMessage(f'Голосування на тему: "{topic}" було відхилено.')

    callback_done.set()


def wantToRead(topic, name):
    return mb.askyesno(title="Нове голосування", message=f'Чи голосуєте ви за "{topic}", запропонований {name}?')


def showMessage(message):

    global textCons
    to_show = message
    textCons.config(state=tk.NORMAL)
    textCons.insert(tk.END, to_show + "\n\n")
    textCons.config(state=tk.DISABLED)
    textCons.see(tk.END)


# ===================== start chat =========================

client_key_params_func()
cred = credentials.Certificate(r'thresholdcryptochat-firebase-adminsdk-efq0t-9f4616190a (2).json')
db = firestore.client()
clear_collection(db)

key_params, thresh_params, pub_key, share = prepare_crypto()

win = tk.Tk()
win.withdraw()
login = None
user_name = None
isAdmin = None
mLogin()

messages_id = set()

callback_done = threading.Event()
read_ref = db.collection(u'messages_id')

query_watch = read_ref.on_snapshot(on_snapshot)

win.mainloop()