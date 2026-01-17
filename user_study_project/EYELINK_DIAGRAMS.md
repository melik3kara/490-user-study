"""
EyeLink Entegrasyon - GÖRSEL AKİŞ ŞEMASI
==========================================
"""

# ==============================================================================
# 1. BAĞLANTI DIYAGRAMI
# ==============================================================================

"""
    EyeLink Cihazı (Host PC)
    [████████████████]
         ║ Ethernet (IP: 100.1.1.1)
         ║ 
         ║
    ┌────┴─────────────────────────────┐
    │                                  │
    │   Deney Bilgisayarınız           │
    │   (IP: 100.1.1.2+)               │
    │                                  │
    │  main_experiment.py              │
    │      ↓                           │
    │  EyeLinkManager                  │
    │      ↓                           │
    │  pylink library                  │
    │      ↓                           │
    │  eyelink_data/[*.edf]            │
    │                                  │
    └────────────────────────────────┘
"""

# ==============================================================================
# 2. DOSYA YAPISI
# ==============================================================================

"""
user_study_project/
│
├── 📄 main_experiment.py          ← Ana deney scripti
│   ├── PsychoPy penceresini oluştur
│   ├── EyeLink'i bağla (EyeLinkManager)
│   └── Trial'ları çalıştır
│
├── 📋 config.py                  ← Ayarlar (IP, Örnekleme Hızı, vb.)
│   ├── EYELINK_ENABLED = True/False
│   ├── EYELINK_IP = "100.1.1.1"
│   └── EYELINK_SAMPLE_RATE = 1000
│
├── 🔗 eyelink_utils.py           ← Manager sınıfı (KULLAN!)
│   ├── connect()                 → EyeLink'e bağlan
│   ├── calibrate()               → Kalibrasyon yap
│   ├── start_recording()         → Trial kaydını başlat
│   ├── send_message()            → EDF'ye mesaj gönder
│   └── disconnect()              → Bağlantıyı kes
│
├── 📚 eyelink_utils_ACTIVE.py    ← Uygulamalarla versiyon (REF)
│   ├── Tüm kodlar açıklamalarla
│   └── Ne açmalı gösterilmiş
│
├── 📖 EYELINK_QUICK_START.md     ← 5-DAKIKA BAŞLANGIC (BAŞLA BURADAN!)
│
├── 📖 EYELINK_SETUP_GUIDE_TR.py  ← Adım-adım Türkçe rehber
│   ├── 10 ana adım
│   ├── Komutlar
│   └── Sorun giderme
│
├── 📖 EYELINK_GUIDE.md           ← Teknik referans
│   ├── Bağlantı kodları
│   ├── Veri analizi
│   └── İleri konular
│
└── 📁 eyelink_data/              ← EDF dosyaları buraya kaydedilir
    ├── el150900.edf              (gaze, pupil, events, timestamps)
    └── el151030.edf
"""

# ==============================================================================
# 3. KÜÇÜKTEPEDEKİ AKIŞ
# ==============================================================================

"""
┌─────────────────────────────────────────────────────────────┐
│                 DENEY BAŞLAMADAN ÖNCE                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Hardware Check                                          │
│     ├─ EyeLink PC açık mı?                                 │
│     ├─ Ethernet kablosu bağlı mı?                          │
│     └─ ping 100.1.1.1 ✓                                    │
│                                                             │
│  2. Software Check                                          │
│     ├─ pip install pylink ✓                                │
│     ├─ config.py: EYELINK_ENABLED = True ✓                 │
│     ├─ eyelink_utils.py açık (uncomment) ✓                 │
│     └─ python test_eyelink.py ✓                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│              DENEY BAŞLADIĞINDA (otomatik)                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  main_experiment.py çalıştırılır                           │
│         ↓                                                   │
│  setup_eyelink()                                            │
│         ├─ EyeLinkManager(config)                          │
│         ├─ .connect()      → EyeLink'e bağlan              │
│         ├─ .calibrate()    → 9-nokta kalibrasyon           │
│         └─ Katılımcı hazır                                 │
│         ↓                                                   │
│  Trial başında                                              │
│         ├─ .start_recording(trial_id=1)                    │
│         ├─ .send_message("TRIAL_START")                    │
│         └─ EDF dosyasına yazma başla                       │
│         ↓                                                   │
│  Video gösterilirken                                        │
│         ├─ .send_message("VIDEO_ONSET")                    │
│         ├─ Gaze verisi toplanıyor (1000 Hz = 1ms)          │
│         └─ .send_message("VIDEO_OFFSET")                   │
│         ↓                                                   │
│  Cevap alınırken                                            │
│         ├─ Katılımcı sol/sağ basıyor                       │
│         ├─ .send_message("RESPONSE left")                  │
│         └─ Yanıt zamanı kaydedilir                         │
│         ↓                                                   │
│  Trial sonunda                                              │
│         ├─ .stop_recording()                               │
│         └─ Bir trial'ın EDF verisi kaydedildi              │
│         ↓                                                   │
│  (Tüm trial'lar tekrarla)                                  │
│         ↓                                                   │
│  Deney sonunda                                              │
│         ├─ .disconnect()                                   │
│         └─ EDF dosyası eyelink_data/ klasörüne transfer et │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│              DENEY BİTTİKTEN SONRA (analiz)                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  eyelink_data/el150900.edf oluşturulmuş                    │
│         ↓                                                   │
│  EyeLink Data Viewer ile aç                                │
│  (SR Research tarafından sağlanır)                         │
│         ├─ Heat maps                                       │
│         ├─ Gaze paths                                      │
│         ├─ Fixations                                       │
│         └─ Saccades                                        │
│         ↓                                                   │
│  Veya Python ile analiz et                                 │
│         ├─ import eyelinkcore                              │
│         ├─ df = pd.read_csv('converted.csv')               │
│         └─ Grafikleri çiz                                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
"""

# ==============================================================================
# 4. COD ÖRNEĞİ (STEP-BY-STEP)
# ==============================================================================

"""
ADIM 1: İmport ve Başlangıç
─────────────────────────────

    from eyelink_utils import EyeLinkManager
    import config
    
    el = EyeLinkManager(config)

ADIM 2: Bağlan
──────────────

    el.connect()  # EyeLink'e bağlan
    
    Arka planda:
    ├─ pylink.EyeLink("100.1.1.1") çağrılır
    ├─ Ağ bağlantısı kurulur
    ├─ EDF dosyası oluşturulur
    └─ Tracker yapılandırılır

ADIM 3: Kalibre Et
──────────────────

    el.calibrate()  # 9-nokta kalibrasyon
    
    Bu sırada:
    ├─ EyeLink Host PC ekranında 9 nokta görünür
    ├─ Katılımcı noktalara bakıyor
    ├─ Tracker gözü kalibre ediyor
    └─ Kalibrasyon data kaydediliyor

ADIM 4: Recording Başlat
────────────────────────

    el.start_recording(trial_id=1)
    
    Arka planda:
    ├─ pylink startRecording() çağrılır
    ├─ EDF dosyasına yazma başlar
    └─ 1000 Hz'de veri toplanmaya başlanır

ADIM 5: Olayları İşaretle
─────────────────────────

    el.send_message("VIDEO_ONSET")
    
    EDF dosyasına yazılır:
    [1234.567] MESSAGE VIDEO_ONSET
    
    Analiz sırasında kullanılır:
    "VIDEO 6 saniye sonra başladı"

ADIM 6: Recording Durdur
────────────────────────

    el.stop_recording()
    
    Arka planda:
    ├─ Veri toplanması durur
    └─ Trial'ın verisi kaydedilmiş sayılır

ADIM 7: Bağlantıyı Kes
──────────────────────

    el.disconnect()
    
    Arka planda:
    ├─ EDF dosyası EyeLink Host'ta kapatılır
    ├─ eyelink_data/el150900.edf'ye transfer edilir
    ├─ Lokal bilgisayarda kaydedilir
    └─ Bağlantı kesilir

EDF Dosyasının İçeriği
──────────────────────

    el150900.edf (Binary format):
    ├─ Metadata (Tracker info, sample rate, vb.)
    │
    ├─ SAMPLES (1000/saniye = 1000 satır/saniye)
    │  ├─ [0.0] L: 640, 480, pupil=2.5  (Sol gözün pozisyonu)
    │  ├─ [0.001] L: 641, 479, pupil=2.4
    │  ├─ [0.002] L: 642, 480, pupil=2.5
    │  └─ ... (6 saniye = 6000 örnek)
    │
    ├─ EVENTS (İşaretli anlar)
    │  ├─ FIXATION 0.5 500 (0.5-0.5 sek aralığında 500,500'de sabit)
    │  ├─ SACCADE 0.51 0.55 (0.51-0.55 sek arasında hareket)
    │  └─ MESSAGE [1.0] TRIAL_START (1.0 sn'de işaret)
    │
    └─ TRIAL VARIABLES
       ├─ !V TRIAL_VAR video_left extraversion_high_01.mp4
       ├─ !V TRIAL_VAR video_right extraversion_low_01.mp4
       └─ !V TRIAL_VAR high_position left
"""

# ==============================================================================
# 5. VERI AKIŞI DİYAGRAMI
# ==============================================================================

"""
KAYNAKLAR (Sources)
═════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────┐
│   EyeLink Tracker Cihazı (Host PC)                          │
│   (Kızılötesi kamera katılımcının gözünü izler)             │
│                                                             │
│   ├─ Sol Göz  ┐                                             │
│   │           ├─→ Gaze (x, y)                              │
│   └─ Sağ Göz  ┘     Pupil Size                             │
│                                                             │
│   Sample Rate: 1000 Hz (1 örnek = 1 ms)                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                    ↓ (Ethernet → Network)
┌─────────────────────────────────────────────────────────────┐
│   main_experiment.py (Deney PC)                             │
│                                                             │
│   Alır:                    Gönderir:                        │
│   ├─ Gaze x, y             ├─ "TRIAL_START"                │
│   ├─ Pupil size            ├─ "VIDEO_ONSET"                │
│   └─ Sample timestamps      ├─ "RESPONSE left"              │
│                             └─ "TRIAL_END"                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────────────┐
│   EDF Dosyası (Deney PC'de eyelink_data/ klasörü)           │
│                                                             │
│   [0.000] SAMPLE: L 640 480 2.5                             │
│   [0.001] SAMPLE: L 641 480 2.4                             │
│   ...                                                       │
│   [1.000] MESSAGE: TRIAL_START 001                          │
│   [1.500] MESSAGE: VIDEO_ONSET                              │
│   [1.510] FIXATION start 640 480                            │
│   [1.650] FIXATION end (duration 140ms)                     │
│   [1.700] MESSAGE: RESPONSE left                            │
│   [7.500] MESSAGE: VIDEO_OFFSET                             │
│   [7.600] MESSAGE: TRIAL_END 001                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────────────┐
│   Analiz (EyeLink Data Viewer veya Python)                  │
│                                                             │
│   ├─ Heat maps (nereyi baktılar)                            │
│   ├─ Fixations (kalış noktaları)                            │
│   ├─ Saccades (göz hareketleri)                             │
│   ├─ Pupil dilation (beyin aktivitesi)                      │
│   └─ Response time correlation                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
"""

# ==============================================================================
# 6. SAMAN ÇIZELGESI
# ==============================================================================

"""
DENEY TIMELINE (Bir Trial İçin)
═════════════════════════════════════════════════════════════════

         0.0s: TRIAL_START
              Tracker recording başlıyor
              │
    ┌────────┴────────┐
    │                 │
    │                 │
    │
   0.0s: FIXATION ONSET
   [████████████] 1.0s duration
   │
   │
  1.0s: FIXATION OFFSET
        VIDEO_ONSET
        (İki video yan yana görünüyor)
        
        LEFT VIDEO          RIGHT VIDEO
        [████████]          [████████]
        (Participant bakıyor)
        
        Track:
        - Gaze x, y (1000 Hz)
        - Pupil size
        - Fixation times
        - Saccade times
        │
   1.0────────────────────────────7.0s (6 saniye video)
        [████████████████████████████]
        │
   7.0s: VIDEO_OFFSET
        (Videolar kaybolur)
        │
   7.0s: QUESTION SCREEN
        "Which person looks more extraverted?"
        │
        ← RESPONSE (katılımcı basıyor)
        │
   Response Time: 2.5 saniye (baseline'dan sonra)
   Response: LEFT (left arrow)
   │
   7.5s: CONFIDENCE RATING
        "How confident? 1-5"
        │
        Confidence: 4
        │
   8.0s: ITI (Inter-Trial Interval)
   [████] 0.5s blank screen
        │
   8.5s: TRIAL_COMPLETE
        (Sonraki trial'a geç)


TOPLAM TRIAL DÜREMİ: ~8.5 saniye (deney süresi değişebilir)
EDF DOSYASINDA KAYIT: ~8500 sample (1000 Hz × 8.5s)
"""

# ==============================================================================
# 7. HATA KODLARI VE ÇÖZÜMLER
# ==============================================================================

"""
Exception Handler Flowchart:
═════════════════════════════════════════════════════════════════

    pylink.EyeLinkException
    │
    ├─ "Failed to connect"
    │  ├─ Sebep: ping 100.1.1.1 başarısız
    │  ├─ Sebep: Yanlış IP (config.py)
    │  └─ Çözüm: Ethernet, IP, firewall kontrol et
    │
    ├─ "Calibration failed"
    │  ├─ Sebep: Kötü aydınlatma
    │  ├─ Sebep: Katılımcı sabit durmamış
    │  └─ Çözüm: Tekrar kalibre et
    │
    ├─ "Failed to open EDF file"
    │  ├─ Sebep: Host'ta disk alanı yok
    │  ├─ Sebeb: Dosya adı 8 karakterden uzun
    │  └─ Çözüm: Disk alanı kontrol et, adı kısalt
    │
    ├─ "startRecording failed"
    │  ├─ Sebep: Kalibrasyon yapılmamış
    │  ├─ Sebep: EDF açılmamış
    │  └─ Çözüm: Sırasını kontrol et
    │
    └─ "File transfer failed"
       ├─ Sebep: Ağ bağlantısı kopmuş
       ├─ Sebep: Path geçersiz
       └─ Çözüm: mkdir eyelink_data & ping test et
"""

print(__doc__)
