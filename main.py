import tkinter as tk
from screens import IzvelnesEkrans, SpelesEkrans, StatistikasEkrans
from db_handler import DatubazesApstradatajs
from game_engine import SpelesDzinejs


class ReakcijasLietotne(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Reakcijas Treniņš")
        self.geometry("800x600")
        self.resizable(False, False)
        
        self.db = DatubazesApstradatajs()
        self.speles_dzinejs = SpelesDzinejs()
        
        self.konteiners = tk.Frame(self)
        self.konteiners.pack(side="top", fill="both", expand=True)
        self.konteiners.grid_rowconfigure(0, weight=1)
        self.konteiners.grid_columnconfigure(0, weight=1)
        
        self.ekrani = {}
        
        for F in (IzvelnesEkrans, SpelesEkrans, StatistikasEkrans):
            ekrana_nosaukums = F.__name__
            ekrans = F(vecaks=self.konteiners, kontrolieris=self)
            self.ekrani[ekrana_nosaukums] = ekrans
            ekrans.grid(row=0, column=0, sticky="nsew")
        
        self.radit_ekranu("IzvelnesEkrans")

    def radit_ekranu(self, ekrana_nosaukums):
        ekrans = self.ekrani[ekrana_nosaukums]
        ekrans.tkraise()

if __name__ == "__main__":
    lietotne = ReakcijasLietotne()
    lietotne.mainloop()
