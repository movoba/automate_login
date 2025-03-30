import tkinter as tk
from tkinter import BOTH, Label, Button, X, BOTTOM, LEFT, Entry, messagebox
from encrypt import save_zugangsdaten, load_zugangsdaten
from ilovegfn import WebNav
from datetime import datetime
import csv
import schedule
import time


class LoginFrame:
    def __init__(self, root):
        self.root = root
        self.root.resizable(False, False)
        self.root.title("Automatische Zeiterfassung")
        self.root.geometry("400x250")
        self.ersterFrame()
        self.buttonFrame()
        self.buttonFrame2()
        self.zweiterFrame()
        self.loginLabels()
        self.dritterFrame()

    def ersterFrame(self):
        self.frm = tk.Frame(self.root, bg="white")
        self.frm.pack(fill=BOTH, expand=True)

        label = Label(
            self.frm,
            text="Willkommen bei deiner automatischen Zeiterfassung",
            bg="white",
        )

        label.pack(pady=10)

    def buttonFrame(self):
        # eigener Frame für die Buttons
        self.button_frm = tk.Frame(self.root, bg="white")

        self.button_frm.pack(side=BOTTOM, fill=X)

        # ---platzhalter damit nicht nach links rutscht----
        links_placeholder = tk.Frame(self.button_frm)

        links_placeholder.pack(side=LEFT, expand=True)

        button_beenden = Button(self.button_frm, text="Beenden", command=self.root.quit)

        button_beenden.pack(pady=5, padx=10, side=LEFT)

        self.button_weiter = Button(
            self.button_frm, text="Weiter", command=self.zeige_frame2
        )
        self.root.bind("<Return>", lambda event: self.button_weiter.invoke())
        self.button_weiter.pack(pady=5, padx=10, side=LEFT)

        # ---placeholder damit nichts nach rechts rutscht----
        right_placeholder = tk.Frame(self.button_frm)
        right_placeholder.pack(side=LEFT, expand=True)

    def zweiterFrame(self):
        self.frm_two = tk.Frame(self.root, bg="white")
        self.frm_two.pack_forget()

        label_two = Label(
            self.frm_two, text="Bitte gib deine Logindaten ein:", bg="white"
        )

        label_two.pack(pady=5)

    def buttonFrame2(self):
        self.button_frm_two = tk.Frame(self.root, bg="white")

        self.button_frm_two.pack_forget()

        # ---platzhalter damit nicht nach links rutscht----
        links_placeholder2 = tk.Frame(self.button_frm_two)

        links_placeholder2.pack(side=LEFT, expand=True)

        self.button_beenden_two = Button(
            self.button_frm_two, text="Beenden", command=self.root.quit
        )
        self.button_beenden_two.pack(pady=5, padx=10, side=LEFT)

        self.button_back = Button(
            self.button_frm_two, text="Zurück", command=self.zeige_frame1
        )

        self.button_back.pack(pady=5, padx=10, side=LEFT)

        button_weiter_two = Button(
            self.button_frm_two, text="Weiter", command=self.abschließen_button
        )
        self.root.bind("<Return>", lambda event: self.button_ende.invoke())
        button_weiter_two.pack(pady=5, padx=10, side=LEFT)

        # ---placeholder damit nichts nach rechts rutscht----
        right_placeholder2 = tk.Frame(self.button_frm_two)

        right_placeholder2.pack(side=LEFT, expand=True)

    def loginLabels(self):
        # credentials
        username_label = Label(self.frm_two, text="Benutzername", bg="white")
        username_label.pack(pady=10)
        self.username = Entry(self.frm_two, bg="white", width=30)
        # username.insert(0, "Benutzer")
        self.username.pack()
        passwort_label = Label(self.frm_two, text="Passwort", bg="white")
        passwort_label.pack(pady=5)
        self.passwort = Entry(self.frm_two, bg="white", show="*", width=30)
        # passwort.insert(0, "Passwort")
        self.passwort.pack()

    def dritterFrame(self):
        self.frm_three = tk.Frame(self.root, bg="white")
        self.frm_three.pack_forget()

        label_three = Label(
            self.frm_three, text="Das hat doch wunderbar geklappt", bg="white"
        )
        label_three.pack()
        self.button_ende = Button(self.frm_three, text="Ende", command=self.beende_und_startroutine)
        self.button_ende.pack(side=BOTTOM, padx=10)

    #mit einem thread muss gui erst beendet werden
    def beende_und_startroutine(self):
        self.root.quit()
        self.webNav_start()
        
    def zeige_frame2(self):
        self.frm.pack_forget()
        self.button_frm.pack_forget()
        self.button_frm_two.pack(side=BOTTOM, fill=X)
        self.frm_two.pack(fill=BOTH, expand=True)

    def zeige_frame1(self):
        self.frm_two.pack_forget()
        self.button_frm.pack(side=BOTTOM, fill=X)
        self.button_frm_two.pack_forget()
        self.frm.pack(fill=BOTH, expand=True)

    def zugangdaten(self):
        name = self.username.get()
        passw = self.passwort.get()

        daten = {"username": name, "passwort": passw}
        save_zugangsdaten(daten)

    def abschließen_button(self):
        # strip gegen leerzeichen
        if not self.username.get().strip() or not self.passwort.get().strip():
            messagebox.showerror("Fehler", "Bitte alle Felder ausfüllen!")
        else:
            self.zugangdaten()
            self.frm_two.pack_forget()
            self.button_frm_two.pack_forget()
            self.frm_three.pack(fill=BOTH, expand=True)

    def webNav_start(self):
        heute = datetime.now().date()
        daten = []
        with open("daten.csv", encoding="utf-8") as csvdatei:
            datum = csv.reader(csvdatei)
            for row in datum:
                datumObj = datetime.strptime(row[0], "%Y-%m-%d").date()
                daten.append(datumObj)
        

        if heute in daten:
            webnav = WebNav(load_zugangsdaten())
            schedule.every().day.at("08:21").do(webnav.automate_login)
            schedule.every().day.at("16:31").do(webnav.automate_logout)

            while True:
                schedule.run_pending()
                #logging.info("Warte auf naechste geplante Aufgabe...")
                time.sleep(1)
