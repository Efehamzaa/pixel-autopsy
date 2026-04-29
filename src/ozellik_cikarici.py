import os
import numpy as np
import pandas as pd
from PIL import Image

def ozellik_cikar(resim_yolu):
    # Resmi aç ve siyah-beyaz formata çevir
    resim = Image.open(resim_yolu).convert('L')
    resim_array = np.array(resim)
    
    isik_siddeti_ortalamasi = np.mean(resim_array)
    standart_sapma = np.std(resim_array)
    maksimum_deger = np.max(resim_array)
    parlaklik_95 = np.percentile(resim_array, 95)
    medyan = np.median(resim_array)
    parlak_piksel_orani = np.mean(resim_array > 25)
    kontrast = maksimum_deger - np.min(resim_array)
    
    hist_degerleri, _ = np.histogram(resim_array, bins=16, range=(0, 255))
    
    return (isik_siddeti_ortalamasi, standart_sapma, maksimum_deger, parlaklik_95, 
            medyan, parlak_piksel_orani, kontrast, hist_degerleri)

def veri_seti_olustur():
    veriler = []
    
    print("Gercek fotograflar isleniyor...")
    girdi_gercek = "data/processed/authentic"
    for dosya_adi in os.listdir(girdi_gercek):
        resim_yolu = os.path.join(girdi_gercek, dosya_adi)
        # Fonksiyondan tüm değerleri çek
        is_ort, std, maks, p95, med, parlak_oran, kont, hist = ozellik_cikar(resim_yolu)
        
        satir = {
            "dosya_adi": dosya_adi, 
            "etiket": 0, 
            "isik_siddeti_ortalamasi": is_ort, 
            "standart_sapma": std,
            "maksimum_deger": maks,
            "parlaklik_95": p95,
            "medyan": med,
            "parlak_piksel_orani": parlak_oran,
            "kontrast": kont
        }
        
        for i in range(16):
            satir[f"hist_{i}"] = hist[i]
            
        veriler.append(satir)

    print("Sahte fotograflar isleniyor...")
    girdi_degistirilmis = "data/processed/tampered"
    for dosya_adi in os.listdir(girdi_degistirilmis):
        resim_yolu = os.path.join(girdi_degistirilmis, dosya_adi)
        
        is_ort, std, maks, p95, med, parlak_oran, kont, hist = ozellik_cikar(resim_yolu)
        
        satir = {
            "dosya_adi": dosya_adi, 
            "etiket": 1, 
            "isik_siddeti_ortalamasi": is_ort, 
            "standart_sapma": std,
            "maksimum_deger": maks,
            "parlaklik_95": p95,
            "medyan": med,
            "parlak_piksel_orani": parlak_oran,
            "kontrast": kont
        }
        
        for i in range(16):
            satir[f"hist_{i}"] = hist[i]
            
        veriler.append(satir)

    # Listeyi Pandas Tablosuna Çevir ve Kaydet
    df = pd.DataFrame(veriler)
    df.to_csv("data/veri_seti.csv", index=False)
    print("Veri seti basariyla olusturuldu! Tam 23 kolonlu 'veri_seti.csv' kaydedildi.")

if __name__ == "__main__":
    print("Veri cikarim motoru baslatiliyor...")
    veri_seti_olustur()