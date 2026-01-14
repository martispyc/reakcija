import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def zimot_vesturi(ass, df):
    ass.clear()
    ass.set_facecolor("white")
    
    if df.empty:
        ass.text(0.5, 0.5, "nav datu", ha='center', va='center', color="black", fontname="Helvetica")
        ass.axis('off')
        return

    nesenie_dati = df.tail(10).reset_index(drop=True)
    
    ass.plot(nesenie_dati.index + 1, nesenie_dati['reakcijas_laiks_ms'], marker='o', markersize=4, linestyle='-', color='black', linewidth=1.5)
    
    ass.set_title("vēsture (10 spēles)", fontsize=10, fontname="Helvetica", pad=10)
    
    ass.spines['top'].set_visible(False)
    ass.spines['right'].set_visible(False)
    ass.spines['left'].set_visible(False)
    ass.spines['bottom'].set_color('black')
    ass.spines['bottom'].set_linewidth(0.5)
    
    ass.tick_params(axis='x', colors='black', labelsize=8)
    ass.tick_params(axis='y', colors='black', labelsize=8, length=0)
    ass.grid(False)
    
    if len(nesenie_dati) > 0:
        ass.set_xticks(range(1, len(nesenie_dati) + 1))

def simulet_izaugsmi(ass, df, intensitate_minutes):
    ass.clear()
    ass.set_facecolor("white")
    
    if df.empty or len(df) < 2:
        ass.text(0.5, 0.5, "nepieciešams vairāk datu", ha='center', va='center', color="black", fontname="Helvetica")
        ass.axis('off')
        return

    intensitates_karte = {10: 0.995, 30: 0.99, 60: 0.985}
    krituma_koeficients = intensitates_karte.get(intensitate_minutes, 0.995)
    
    pasreizejais_vid = df.tail(5)['reakcijas_laiks_ms'].mean()
    dienas = np.arange(1, 21)
    prognozetie_laiki = [pasreizejais_vid * (krituma_koeficients ** d) for d in dienas]
    
    ass.plot(dienas, prognozetie_laiki, linestyle='--', color='black', linewidth=1, label='prognoze')
    ass.axhline(y=pasreizejais_vid, color='gray', linestyle=':', linewidth=1, label='vidējais')
    
    ass.set_title(f"prognoze ({intensitate_minutes} min)", fontsize=10, fontname="Helvetica", pad=10)
    
    ass.spines['top'].set_visible(False)
    ass.spines['right'].set_visible(False)
    ass.spines['left'].set_visible(False)
    ass.spines['bottom'].set_color('black')
    ass.spines['bottom'].set_linewidth(0.5)
    
    ass.tick_params(axis='both', colors='black', labelsize=8, length=0)
    ass.legend(frameon=False, fontsize=8)
    ass.grid(False)
