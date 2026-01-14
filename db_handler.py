import pandas as pd
import os
from datetime import datetime


class DatubazesApstradatajs:
    def __init__(self, faila_nosaukums='reakcijas_dati.csv'):
        self.faila_nosaukums = faila_nosaukums
        self.kolonnas = ['laika_zimogs', 'reakcijas_laiks_ms', 'merka_izmers']
        
        if not os.path.exists(self.faila_nosaukums):
            df = pd.DataFrame(columns=self.kolonnas)
            df.to_csv(self.faila_nosaukums, index=False)

    def registret_speli(self, reakcijas_laiks, merka_izmers):
        dati = {
            'laika_zimogs': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            'reakcijas_laiks_ms': [reakcijas_laiks],
            'merka_izmers': [merka_izmers]
        }
        jauna_rinda = pd.DataFrame(dati)
        
        try:
            jauna_rinda.to_csv(self.faila_nosaukums, mode='a', header=False, index=False)
        except Exception as k:
            print(f"Kļūda saglabājot datus: {k}")

    def iegut_datus(self):
        if os.path.exists(self.faila_nosaukums):
            try:
                return pd.read_csv(self.faila_nosaukums)
            except pd.errors.EmptyDataError:
                return pd.DataFrame(columns=self.kolonnas)
        else:
            return pd.DataFrame(columns=self.kolonnas)
