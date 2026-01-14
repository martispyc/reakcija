import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import analysis

KRASA_FONS = "#FFFFFF"
KRASA_PRIEKSPUSE = "#000000"
FONTS_L = ("Helvetica", 42)
FONTS_M = ("Helvetica", 24)
FONTS_S = ("Helvetica", 12)

class MinimalaPoga(tk.Button):
    def __init__(self, vecaks, teksts, komanda):
        super().__init__(vecaks, text=teksts, command=komanda, font=FONTS_M, bg=KRASA_FONS, fg=KRASA_PRIEKSPUSE,relief="flat", borderwidth=0, activebackground=KRASA_FONS, activeforeground="#666666",cursor="hand2")
        self.pack(pady=25, ipadx=10)

class IzvelnesEkrans(tk.Frame):
    def __init__(self, vecaks, kontrolieris):
        super().__init__(vecaks, bg=KRASA_FONS)
        self.kontrolieris = kontrolieris
        
        konteiners = tk.Frame(self, bg=KRASA_FONS)
        konteiners.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(konteiners, text="reakcija.", font=FONTS_L, bg=KRASA_FONS, fg=KRASA_PRIEKSPUSE).pack(pady=(0, 80))
        
        MinimalaPoga(konteiners, "sākt", lambda: kontrolieris.radit_ekranu("SpelesEkrans"))
        MinimalaPoga(konteiners, "dati", lambda: kontrolieris.radit_ekranu("StatistikasEkrans"))
        MinimalaPoga(konteiners, "iziet", kontrolieris.quit)

class SpelesEkrans(tk.Frame):
    def __init__(self, vecaks, kontrolieris):
        super().__init__(vecaks, bg=KRASA_FONS)
        self.kontrolieris = kontrolieris
        
        self.audekls = tk.Canvas(self, bg=KRASA_FONS, highlightthickness=0)
        self.audekls.pack(fill="both", expand=True)
        self.audekls.bind("<Button-1>", self.uz_klikska)
        
        self.teksts = self.audekls.create_text(
            400, 300, text="klikšķini lai sāktu", font=FONTS_M, fill=KRASA_PRIEKSPUSE
        )
        
        self.aktivs = False
        self.gaida_ievadi = False
        
        self.atpakal = tk.Label(self, text="← atpakaļ", font=FONTS_S, bg=KRASA_FONS, fg=KRASA_PRIEKSPUSE, cursor="hand2")
        self.atpakal.bind("<Button-1>", lambda e: self.iziet_spele())
        self.atpakal.place(x=40, y=40)

    def tkraise(self, virs_si=None):
        super().tkraise(virs_si)
        self.audekls.delete("all")
        self.teksts = self.audekls.create_text(
            self.winfo_width()/2, self.winfo_height()/2, 
            text="klikšķini lai sāktu", font=FONTS_M, fill=KRASA_PRIEKSPUSE
        )
        self.aktivs = False
        self.gaida_ievadi = False
        self.audekls.config(bg=KRASA_FONS)

    def uz_klikska(self, notikums):
        if not self.aktivs:
            self.aktivs = True
            self.audekls.itemconfig(self.teksts, text="gaidi...")
            
            import random
            kavesanas = random.randint(1000, 3000)
            self.after(kavesanas, self.radit_signalu)
            
        elif self.gaida_ievadi:
            ilgums = self.kontrolieris.speles_dzinejs.beigt_raundu()
            self.kontrolieris.db.registret_speli(ilgums, 0)
            
            self.gaida_ievadi = False
            self.aktivs = False
            self.audekls.config(bg=KRASA_FONS)
            self.audekls.itemconfig(self.teksts, text=f"{ilgums}ms\nklikšķini vēlreiz", fill=KRASA_PRIEKSPUSE)

    def radit_signalu(self):
        if not self.aktivs: return
        self.kontrolieris.speles_dzinejs.sakt_raundu()
        self.audekls.config(bg=KRASA_PRIEKSPUSE)
        self.audekls.itemconfig(self.teksts, text="", fill=KRASA_FONS)
        self.gaida_ievadi = True

    def iziet_spele(self):
        self.aktivs = False
        self.kontrolieris.radit_ekranu("IzvelnesEkrans")

class StatistikasEkrans(tk.Frame):
    def __init__(self, vecaks, kontrolieris):
        super().__init__(vecaks, bg=KRASA_FONS)
        self.kontrolieris = kontrolieris
        
        galvene = tk.Frame(self, bg=KRASA_FONS)
        galvene.pack(fill="x", pady=40, padx=40)
        
        atpakal = tk.Label(galvene, text="← atpakaļ", font=FONTS_S, bg=KRASA_FONS, fg=KRASA_PRIEKSPUSE, cursor="hand2")
        atpakal.bind("<Button-1>", lambda e: kontrolieris.radit_ekranu("IzvelnesEkrans"))
        atpakal.pack(side="left")
        
        kontroles = tk.Frame(galvene, bg=KRASA_FONS)
        kontroles.pack(side="right")
        
        tk.Label(kontroles, text="intensitāte:", font=FONTS_S, bg=KRASA_FONS, fg=KRASA_PRIEKSPUSE).pack(side="left", padx=10)
        
        self.intensitate_var = tk.IntVar(value=30)
        
        stils = ttk.Style()
        stils.theme_use('default')
        stils.configure("TCombobox", fieldbackground=KRASA_FONS, background=KRASA_FONS, borderwidth=0, arrowsize=15)
        
        self.izvele = ttk.Combobox(kontroles, textvariable=self.intensitate_var, values=[10, 30, 60], width=5, font=FONTS_S, state="readonly")
        self.izvele.pack(side="left")
        self.izvele.bind("<<ComboboxSelected>>", lambda e: self.atjaunot_grafikus())

        self.figura = Figure(figsize=(8, 5), dpi=100, facecolor=KRASA_FONS)
        self.ass1 = self.figura.add_subplot(211)
        self.ass2 = self.figura.add_subplot(212)
        
        self.audekls = FigureCanvasTkAgg(self.figura, self)
        self.audekls.get_tk_widget().pack(side="top", fill="both", expand=True, padx=40, pady=10)

    def tkraise(self, virs_si=None):
        super().tkraise(virs_si)
        self.atjaunot_grafikus()

    def atjaunot_grafikus(self):
        df = self.kontrolieris.db.iegut_datus()
        analysis.zimot_vesturi(self.ass1, df)
        analysis.simulet_izaugsmi(self.ass2, df, self.intensitate_var.get())
        self.audekls.draw()
