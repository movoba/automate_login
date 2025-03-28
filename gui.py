import tkinter as tk
from tkinter import BOTH, Label, Button, X, BOTTOM, LEFT, Entry
from encrypt import save_zugangsdaten

root = tk.Tk()
root.resizable(False, False)
root.title("Automatische Zeiterfassung")
root.geometry("400x250")


def zeige_frame2():
    frm.pack_forget()
    button_frm.pack_forget()
    button_frm_two.pack(side=BOTTOM, fill=X)
    frm_two.pack(fill=BOTH, expand=True)
    
def zeige_frame1():
    frm_two.pack_forget()
    button_frm.pack(side=BOTTOM, fill=X)
    button_frm_two.pack_forget()
    frm.pack(fill=BOTH, expand=True)   

def zugangdaten(username: str, passwort: str):
    name = username.get()
    passw = passwort.get()
    
    daten = {
        "username": name,
        "passwort": passw
    }
    save_zugangsdaten(daten)


def beenden_button_click():
    #vielleicht später noch wichtig für speichern oder so
    root.quit()

frm = tk.Frame(root, bg="white")
frm.pack(fill=BOTH, expand=True)

label= Label(frm, text="Willkommen bei deiner automatischen Zeiterfassung", bg="white")
label.pack(pady=10)

# eigener Frame für die Buttons
button_frm = tk.Frame(root, bg="white")
button_frm.pack(side=BOTTOM, fill=X)
#---platzhalter damit nicht nach links rutscht----
links_placeholder = tk.Frame(button_frm)
links_placeholder.pack(side=LEFT, expand=True)

button_beenden = Button(button_frm, text="Beenden", command = root.quit)
button_beenden.pack(pady=5, padx=10, side=LEFT)

button_weiter = Button(button_frm, text="Weiter", command=zeige_frame2)
button_weiter.pack(pady=5, padx=10, side=LEFT)
#---placeholder damit nichts nach rechts rutscht----
right_placeholder = tk.Frame(button_frm)
right_placeholder.pack(side=LEFT, expand=True)
#-------------------------------------------------
#-------------------------------------------------
frm_two= tk.Frame(root, bg="white")
frm_two.pack_forget()

label_two = Label(frm_two, text="Bitte gib deine Logindaten ein:", bg="white")
label_two.pack(pady=5)

button_frm_two = tk.Frame(root, bg="white")
button_frm_two.pack_forget()

#credentials
username_label = Label(frm_two, text="Benutzername", bg="white")
username_label.pack(pady=10)
username = Entry(frm_two ,bg="white")
#username.insert(0, "Benutzer")
username.pack()
passwort_label = Label(frm_two, text="Passwort", bg="white")
passwort_label.pack(pady=5)
passwort = Entry(frm_two, bg="white", show="*")
#passwort.insert(0, "Passwort")
passwort.pack()

#---platzhalter damit nicht nach links rutscht----
links_placeholder2 = tk.Frame(button_frm_two)
links_placeholder2.pack(side=LEFT, expand=True)

button_beenden_two = Button(button_frm_two, text="Beenden", command= root.quit)
button_beenden_two.pack(pady=5, padx=10, side=LEFT)

button_back = Button(button_frm_two, text="Zurück", command= zeige_frame1)
button_back.pack(pady=5, padx=10,side=LEFT)

button_weiter_two = Button(button_frm_two, text="Weiter")
button_weiter_two.pack(pady=5,padx=10, side=LEFT)
#---placeholder damit nichts nach rechts rutscht----
right_placeholder2 = tk.Frame(button_frm_two)
right_placeholder2.pack(side=LEFT, expand=True)


root.mainloop()

