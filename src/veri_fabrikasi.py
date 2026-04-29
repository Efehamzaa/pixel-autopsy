import os
from ela_engine import ela_farkini_bul, ela_haritasini_kaydet

def uretim_bandi(girdi_klasoru , cikti_klasoru , maksimum_foto=1000):
    islenen_foto=0
    for dosya_adi in os.listdir(girdi_klasoru):
        if islenen_foto>=maksimum_foto:
            break
        if not dosya_adi.lower().endswith(('.jpg', '.jpeg')):
            continue
        girdi_yolu = os.path.join(girdi_klasoru , dosya_adi)
        cikti_yolu = os.path.join(cikti_klasoru , dosya_adi)
        fark_matrisi = ela_farkini_bul(girdi_yolu, kalite_orani=90)
        ela_haritasini_kaydet(fark_matrisi, cikti_yolu, carpan=15)
        islenen_foto+=1
        print(f"{islenen_foto}. dosya islendi: {dosya_adi}")

if __name__ == "__main__":
    print("Uretim bandi basliyor... Orijinal fotograflar isleniyor...")
    #gerçek fotoğrafları alıp processed/authentic klasörüne kaydediyoruz
    uretim_bandi("data/raw/authentic", "data/processed/authentic",1000)
    print("\n")
    print("Uretim bandi devam ediyor... Oynanmis fotograflar isleniyor...")
    #değiştirilmiş fotoğrafları alıp processed/tampered klasörüne kaydediyoruz
    uretim_bandi("data/raw/tampered", "data/processed/tampered",1000)

    print("\nUretim bandi tamamlandi! Islenen fotograflar kaydedildi.")


