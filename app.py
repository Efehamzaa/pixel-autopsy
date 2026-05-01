import streamlit as st
from PIL import Image
import joblib
import pandas as pd
import os
from src.ozellik_cikarici import ozellik_cikar

# 1. Sayfa Ayarları (En üstte olmak zorundadır)
st.set_page_config(
    page_title="Piksel Otopsisi",
    page_icon="🔍", 
    layout="centered"
)

# 2. CSS ile Profesyonel Arka Plan ve Cam Efekti Enjeksiyonu
# Unsplash'ten karanlık, teknolojik bir hacker/matris arka planı çekiyoruz
arka_plan_css = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://images.unsplash.com/photo-1525547719571-a2d4ac8945e2?q=80&w=1920");
    background-size: cover;
    background-position: top center;
    background-attachment: fixed;
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}
/* İçeriklerin okunabilmesi için siyah, yarı saydam bir panel */
.block-container {
    background-color: rgba(14, 17, 23, 0.85);
    padding: 3rem;
    border-radius: 15px;
    box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.5);
}
</style>
"""
st.markdown(arka_plan_css, unsafe_allow_html=True)

# 3. Başlıklar ve Açıklamalar
st.title("🔍 Piksel Otopsisi")
st.subheader("Dijital Fotoğraf Adli Analiz Motoru")
st.write("Yapay zekâ destekli ELA (Hata Seviyesi Analizi) ile fotoğraflardaki montajı ve manipülasyonu tespit edin.")

# Başlık ve açıklamaların hemen altına eklenecek:

with st.expander("ℹ️ Sistem Sınırları ve Gelecek Yol Haritası (Kullanmadan Önce Okuyunuz)"):
    st.warning("Geliştirici Notu: Mevcut motor (Sürüm 1.0), test ortamlarında %83 doğruluk oranına ulaşmış bir Random Forest modelidir.")
    
    st.markdown("""
    **🔍 Mevcut Kör Noktalar (Neden Yanılabilir?)**
    Şu anki algoritmamız, fotoğrafın genel ışık ve kontrast istatistiklerini hesaplar. Bu nedenle;
    * Beyaz arabalar gibi **yüksek kontrastlı objeler**,
    * Plakalar veya tabelalar gibi **keskin metinler**,
    * Doğal güneş parlamaları,
    
    sistem tarafından yanlışlıkla "montaj/sahtelik" olarak algılanabilir. 
    
    **🚀 Gelecek Vizyonu (Sürüm 2.0)**
    Uygulamanın bir sonraki aşamasında, klasik istatistiksel modeller yerine **Evrişimli Sinir Ağları (CNN - Derin Öğrenme)** entegre edilecektir. Bu sayede yapay zekâ, piksellerin sadece parlaklığına değil, nesnelerin fiziksel dokusuna da doğrudan bakarak %95+ doğruluk oranına ulaşacaktır.
    """)

st.markdown("---")

# 4. Dosya Yükleme Arayüzü
st.subheader("Adım 1: Şüpheli Fotoğrafı Yükleyin")
yuklenen_dosya = st.file_uploader("Bir fotoğraf seçin (Sadece JPG veya PNG)", type=["jpg", "jpeg", "png"])

if yuklenen_dosya is not None:
    resim = Image.open(yuklenen_dosya)
    st.image(resim, caption="İncelenecek Fotoğraf", use_column_width=True)
    st.info("Fotoğraf yüklendi. Analiz için 'Analiz Et' butonuna tıklayın.")

    st.markdown("---")
    
    # 5. Analiz Motoru Tetikleyicisi
    if st.button("🚀 Fotoğrafı Analiz Et"):
        with st.spinner("Yapay zekâ pikselleri inceliyor, lütfen bekleyin..."):
            
            # 5.1. Fotoğrafı geçici olarak kaydet
            temp_path = "temp_resim.png"
            with open(temp_path, "wb") as f:
                f.write(yuklenen_dosya.getbuffer())
                
            # 5.2. Faz 1: Özellik Çıkarımı
            is_ort, std, maks, p95, med, parlak_oran, kont, hist = ozellik_cikar(temp_path)
            
            # 5.3. DataFrame Formatına Getir
            satir = {
                "isik_siddeti_ortalamasi": [is_ort], 
                "standart_sapma": [std],
                "maksimum_deger": [maks],
                "parlaklik_95": [p95],
                "medyan": [med],
                "parlak_piksel_orani": [parlak_oran],
                "kontrast": [kont]
            }
            for i in range(16):
                satir[f"hist_{i}"] = [hist[i]]
                
            test_verisi = pd.DataFrame(satir)
            
            # 5.4. Faz 2: Yapay Zekâ Tahmini
            try:
                model = joblib.load("data/model.pkl")
                tahmin = model.predict(test_verisi)
                
                # 5.5. Sonucu Ekrana Bas
                st.subheader("📊 Analiz Sonucu")
                if tahmin[0] == 1:
                    st.error("🚨 DİKKAT: Yapay Zekâ bu fotoğrafta MONTAJ (Sahtelik) tespit etti!")
                else:
                    st.success("✅ GÜVENLİ: Bu fotoğrafın pikselleri orijinal görünüyor.")
            except FileNotFoundError:
                st.error("HATA: 'data/model.pkl' dosyası bulunamadı! Modeli eğittiğinden emin ol.")
                
            # Temizlik
            if os.path.exists(temp_path):
                os.remove(temp_path)