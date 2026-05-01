# 🔍 Piksel Otopsisi (Sürüm 1.0)

## 🎯 Proje Neden Yapıldı?
Günümüzde dijital fotoğrafların manipüle edilmesi (montaj, sahtecilik) saniyeler süren sıradan bir işleme dönüşmüştür.
İnsan gözünün yakalayamadığı bu pikseller arası oynamaları tespit etmek için sezgilere değil, matematiğe dayanan bir sisteme ihtiyaç vardır. 
Bu proje, "Hata Seviyesi Analizi" (ELA - Error Level Analysis) tekniğini yapay zekâ ile harmanlayarak, fotoğraflardaki sahtelikleri otonom olarak ifşa eden 
bir adli bilişim (digital forensics) motoru inşa etmek amacıyla geliştirilmiştir.

## 🛠️ Neler Kullandık? (Sistem Mimarisi)
Bu sistem, hazır bir kütüphane çağırmak yerine sıfırdan yazılmış bir veri boru hattı (pipeline) kullanır:

* **Görüntü İşleme (Özellik Çıkarımı):** Python, PIL ve NumPy kullanılarak fotoğrafların ELA haritaları çıkarıldı. Sistem, görsele doğrudan bakmak yerine bu ELA haritalarından Işık Şiddeti Ortalaması, Standart Sapma, Parlak Piksel Oranı ve 16 kanallı Renk Histogramı olmak üzere **23 farklı matematiksel özellik** hesaplar (`pandas` ile matrise dökülür).
* **Yapay Zekâ (Karar Mekanizması):** `scikit-learn` kullanılarak **Random Forest** (200 Karar Ağacı) algoritması eğitildi. Zorlu CASIA veri setiyle eğitilen bu motor, klasik makine öğrenmesi sınırları içerisinde **%83 doğruluk** oranına ulaşıp mühürlendi.
* **Vitrin (Kullanıcı Arayüzü):** Arka planda çalışan bu ağır matematiği kullanıcı dostu bir hale getirmek için `Streamlit` ile karanlık temalı, anlık analiz yapabilen bir web arayüzü inşa edildi.

## 🚀 Gelecekte Neler Olacak? (Sürüm 2.0 Vizyonu)
Mevcut istatistiksel yaklaşım (Sürüm 1.0), siyah asfalt üzerindeki beyaz bir araba veya keskin araç plakaları gibi yüksek kontrastlı orijinal görsellerde "yanlış pozitif" (false positive) sonuçlar verebilmektedir. Sayısal özet çıkarma mantığının tavanına ulaşılmıştır.

Sistemin bir sonraki aşamasında (Sürüm 2.0) radikal bir paradigma değişikliğine gidilecektir:
1. İstatistiksel özellik çıkarma (CSV) adımı tamamen terk edilecektir.
2. Klasik Makine Öğrenmesi yerine **Derin Öğrenme (Deep Learning)** mimarisine geçilecektir.
3. `PyTorch` veya `TensorFlow` kullanılarak bir **Evrişimli Sinir Ağı (CNN)** inşa edilecek; yapay zekâya matematiksel özetler değil, 
manipülasyonun yapısal dokusunu öğrenmesi için ELA fotoğraflarının bizzat kendisi verilecektir.
4. Hedef, sisteme şekil ve doku vizyonu kazandırarak %95+ doğruluk oranına ulaşmaktır.