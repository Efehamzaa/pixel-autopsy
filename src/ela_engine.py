from PIL import Image
import numpy as np 
import os

def gorseli_matrise_cevir(dosya_yolu):
    # Gorseli aç ve RGB formatına çevir
    gorsel = Image.open(dosya_yolu).convert('RGB')
    # Gorseli numpy kullanarak matrise çevirme işlemi
    matris = np.array(gorsel)
    return matris

def ela_farkini_bul(dosya_yolu , kalite_orani = 90):
    # orijinal gorseli matrise cevir
    orijinal_matris = gorseli_matrise_cevir(dosya_yolu)
    # gorseli kalite oranina gore kaydet
    gorsel = Image.open(dosya_yolu).convert('RGB')
    gorsel.save("gecici_kopya.jpg", "JPEG", quality=kalite_orani)
    kopya_matris= gorseli_matrise_cevir("gecici_kopya.jpg")
    # iki matris arasindaki farki bul
    fark = np.abs(orijinal_matris.astype(np.int16) - kopya_matris.astype(np.int16))
    return fark

def ela_haritasini_kaydet(fark_matrisi , kayit_yolu , carpan=15):
    fark_matrisi = fark_matrisi * carpan
    parlak_matris = np.clip(fark_matrisi, 0, 255)

    fark_gorsel = Image.fromarray(parlak_matris.astype(np.uint8))
    fark_gorsel.save(kayit_yolu)

#test etme
if __name__ == "__main__":
    dosya_yolu = "data/raw/oynanmis2.jpg"  # Değiştirilecek gorsel dosya yolu
    fark_matrisi = ela_farkini_bul(dosya_yolu, kalite_orani=90)
    ela_haritasini_kaydet(fark_matrisi, "data/processed/ela_haritasi_oynanmis2.jpg", carpan=15)



