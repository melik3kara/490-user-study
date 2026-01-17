# EyeLink Entegrasyon - Dosya Rehberi

## 📚 EyeLink ile İlgili Dosyalar

### Hızlı Başlangıç Dosyaları

| Dosya | Amaç | Başlangıçta | Kod |
|-------|------|------------|------|
| **EYELINK_QUICK_START.md** | 5 min hızlı başlangıç | ✅ BAŞLA BURADAN | ❌ |
| **EYELINK_SETUP_GUIDE_TR.py** | 10 adımlı Türkçe rehber | ✅ Çok İyi | ❌ |
| **EYELINK_DIAGRAMS.md** | Görsel akış şemaları | ✅ Görsellerden hoşlanırsan | ❌ |

### Teknik Dosyalar

| Dosya | Amaç | Başlangıçta | Kod |
|-------|------|------------|------|
| **EYELINK_GUIDE.md** | Teknik referans ve kod | ⚠️ Detaylı ama uzun | ✅ |
| **eyelink_utils.py** | Ana Manager sınıfı | ❌ Altyapı (simülasyon) | ✅ |
| **eyelink_utils_ACTIVE.py** | Açıklamalarla uygulamalar | ✅ Ne açmalı gösterilmiş | ✅ |

### Konfigürasyon

| Dosya | Bölüm | Amaç |
|-------|-------|--------|
| **config.py** | Satır 150-200 | EyeLink ayarları |
| **main_experiment.py** | Satır 240-300 | EyeLink entegrasyonu (otomatik) |

---

## 🚀 HIZLI BAŞLANGIC (3 ADIM)

### 1️⃣ Oku
```bash
cat EYELINK_QUICK_START.md
```

### 2️⃣ Kur
```bash
pip install EyeLinkCoreGraphicsPyAPI.whl
```

### 3️⃣ Ayarla ve Çalıştır
```bash
# config.py: EYELINK_ENABLED = True
# eyelink_utils.py: PYLINK_AVAILABLE = True
python main_experiment.py
```

---

## 📖 KAPSAMLI REHBER

Adım adım 10 aşama:
```bash
python EYELINK_SETUP_GUIDE_TR.py
```

---

## 🎨 GÖRSEL

Akış şemaları, diyagramlar, zaman çizelgeleri:
```bash
cat EYELINK_DIAGRAMS.md
```

---

## 🔧 TEKNIK REFERANS

Kod örnekleri ve API detayları:
```bash
cat EYELINK_GUIDE.md
```

---

## ✓ KONTROL LİSTESİ

```
□ EyeLink donanımı güç kaynağına bağlı
□ Ethernet kablosu bağlı
□ ping 100.1.1.1 çalışıyor
□ pylink kurulu (pip list | grep pylink)
□ config.py: EYELINK_ENABLED = True
□ eyelink_utils.py: PYLINK_AVAILABLE = True
□ eyelink_utils.py: Fonksiyonlar açık
```

---

## 🔗 HIZLI LINKLER

- **Başlangıç →** [EYELINK_QUICK_START.md](EYELINK_QUICK_START.md)
- **Detaylı →** [EYELINK_SETUP_GUIDE_TR.py](EYELINK_SETUP_GUIDE_TR.py)
- **Görsel →** [EYELINK_DIAGRAMS.md](EYELINK_DIAGRAMS.md)
- **Teknik →** [EYELINK_GUIDE.md](EYELINK_GUIDE.md)

---

## ❓ SORU SORMA REHBERI

| Soru | Cevap |
|------|--------|
| "EyeLink'i nasıl kurabilirim?" | EYELINK_QUICK_START.md § Adım 2 |
| "Bağlantı başarısız" | EYELINK_SETUP_GUIDE_TR.py § ADIM 3 |
| "Kalibrasyon başarısız" | EYELINK_SETUP_GUIDE_TR.py § ADIM 9 |
| "Verileri nasıl analiz ederim" | EYELINK_GUIDE.md § STEP 8 |
| "Akış nasıl çalışıyor" | EYELINK_DIAGRAMS.md |

---

## 🎯 ÖZET

**Başlama Aşaması:**
1. EYELINK_QUICK_START.md (5 dakika)
2. EYELINK_SETUP_GUIDE_TR.py (20 dakika)
3. Sorun çıkarsa → Troubleshooting bölümü

**Sonra:**
- EYELINK_DIAGRAMS.md (Akış anlamak için)
- EYELINK_GUIDE.md (Teknik detaylar)

---

## 💡 PRO TIPS

- pylink kurmadan önce test edin: `python demo_experiment.py`
- Ağ bağlantısını test edin: `ping 100.1.1.1`
- Kalibrasyon öncesi drift check yapın
- EDF dosyalarını backup alın
- Interest areas analiz öncesi tanımlayın

---

**Hazırsın! Başla →** 🚀
