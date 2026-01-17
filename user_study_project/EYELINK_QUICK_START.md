# EyeLink Eye Tracker Entegrasyonu - Hızlı Özet

## 🎯 Kısa Cevap: Eye Tracker Verilerini Almak

Eye tracker cihazından veri almanız için 5 ana adım var:

### 1️⃣ **Donanım Hazırlığı**
```
EyeLink Host PC (tracker cihazı)
         ↓ (Ethernet kablosu)
    Experiment PC (sizin bilgisayarınız)
    
- IP: 100.1.1.1 (EyeLink)
- IP: 100.1.1.2+ (Sizin PC)
```

### 2️⃣ **Yazılım Kurulumu**
```bash
# SR Research'ten pylink indir
pip install EyeLinkCoreGraphicsPyAPI.whl

# Test et
python -c "import pylink; print('OK')"
```

### 3️⃣ **config.py'ı Ayarla**
```python
EYELINK_ENABLED = True
EYELINK_IP = "100.1.1.1"
EYELINK_SAMPLE_RATE = 1000  # Hz
```

### 4️⃣ **eyelink_utils.py'ı Aç**
Satır 22'de bu kodu açın:
```python
# Kapalı (❌)
# try:
#     import pylink

# Açık (✓)
try:
    import pylink
```

### 5️⃣ **Tüm "UNCOMMENT WHEN PYLINK INSTALLED" Bölümlerini Aç**

---

## 📊 Veri Akışı

```
main_experiment.py
    ↓
eyelink_utils.py  ← Manager sınıfı
    ↓
pylink (EyeLink SDK)
    ↓
EyeLink Host PC
    ↓
EDF dosyası (eyelink_data/)
```

---

## 🔄 Deney Sırasında Otomatik Olanlar

```python
# Trial başında
eyelink.start_recording(trial_id=1)
eyelink.send_message("TRIAL_START")

# Video sırasında
eyelink.send_message("VIDEO_ONSET")
eyelink.send_message("VIDEO_OFFSET")

# Cevap sırasında
eyelink.send_message("RESPONSE")

# Trial sonunda
eyelink.stop_recording()

# Deney sonunda
eyelink.disconnect()  # EDF dosyasını transfer et
```

---

## 📈 EDF Veri Dosyaları

**Nereye kaydediliyor:**
```
eyelink_data/
  └── el150900.edf (participant_001_session1)
  └── el151030.edf (participant_002_session1)
```

**İçinde ne var:**
- 👁️ Gaze (x, y) koordinatları
- 👁️ Pupil size (çift boyutu)
- 📍 Fixations (sabit noktalar)
- ✏️ Saccades (göz hareketleri)
- 🔔 Events (Mesajlar, trial başı/sonu)
- ⏱️ Timestamps (Zaman damgaları)

**Analiz araçları:**
- EyeLink Data Viewer (GUI - SR Research)
- Python: `pandas`, `eyelinkcore`
- MATLAB: Özel araçlar

---

## ⚠️ Sık Sorunlar ve Çözümler

| Sorun | Çözüm |
|-------|--------|
| `ModuleNotFoundError: pylink` | `pip install EyeLinkCoreGraphicsPyAPI.whl` |
| Failed to connect (100.1.1.1) | Ethernet kablosunu, IP'yi kontrol edin |
| Ping 100.1.1.1 başarısız | EyeLink Host PC'nin açık olduğunu kontrol edin |
| Calibration failed | Odada ışık yeterli mi? 60cm uzaklık var mı? |
| EDF transfer yavaş | Ağ bağlantısı kontrol edin |

---

## 📋 Checklist (Hemen Başlamak İçin)

```
□ EyeLink donanımı güç kaynağına bağlı mı?
□ Ethernet kablosu bağlı mı?
□ ping 100.1.1.1 çalışıyor mu?
□ pylink kurulu mu?
□ config.py'ı güncelledin mi? (EYELINK_ENABLED = True)
□ eyelink_utils.py'ın import bölümünü açtın mı?
□ eyelink_utils.py'ın fonksiyon uygulamalarını açtın mı?
□ Test script çalıştırdın mı? (test_eyelink.py)
□ main_experiment.py çalıştırabiliyor musun?
```

---

## 🎓 Detaylı Kaynaklar

Bu klasörde:
- **EYELINK_GUIDE.md** - Tam teknik referans
- **EYELINK_SETUP_GUIDE_TR.py** - Adım adım Türkçe talimatlar
- **eyelink_utils_ACTIVE.py** - Açıklamalarla kodlanmış versiyon

External:
- https://www.sr-research.com/support/ - EyeLink SDK
- https://www.psychopy.org/ - PsychoPy docs

---

## 💡 Pro Tips

1. **Simülasyon modunda test edin** önce (EYELINK_ENABLED = False)
2. **Kalibrasyondan önce** drift check yapın
3. **Her trial'dan önce** gaze verisi çalışıyor mu kontrol edin
4. **EDF dosyalarını** düzenli olarak backup alın
5. **Interest areas'ı** analiz öncesi tanımlayın

---

**Başlamaya hazır mısınız?**

```bash
python main_experiment.py
```

Sistem otomatik olarak bağlanacak ve verileri toplayacak! 🚀
