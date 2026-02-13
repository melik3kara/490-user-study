# Pairwise Personality Perception Experiment

**EyeLink 1000 Plus + PsychoPy** tabanlı kişilik algısı kullanıcı çalışması.

Katılımcılar ardışık olarak gösterilen iki kısa yüz videosunu izler ve bir kişilik özelliği sorusuna yanıt verir.
Göz hareketleri EyeLink 1000 Plus göz izleyici ile kaydedilir.

---

## İçindekiler

- [Hızlı Başlangıç](#hızlı-başlangıç)
- [Deney Akışı](#deney-akışı)
- [Proje Yapısı](#proje-yapısı)
- [Kurulum](#kurulum)
  - [Gereksinimler](#gereksinimler)
  - [Python Ortamı (Conda)](#python-ortamı-conda)
  - [pylink Kurulumu](#pylink-kurulumu)
  - [EyeLink Developers Kit](#eyelink-developers-kit)
- [Lab Kurulumu (2 Bilgisayar)](#lab-kurulumu-2-bilgisayar)
- [Deneyi Çalıştırma](#deneyi-çalıştırma)
- [Konfigürasyon](#konfigürasyon)
- [Veri Çıktıları](#veri-çıktıları)
- [Sorun Giderme](#sorun-giderme)

---

## Hızlı Başlangıç

```bash
# 1. Conda ortamını aktifle
conda activate psychopy-env

# 2. Proje klasörüne git
cd ~/Documents/GitHub/490-user-study/user_study_project

# 3. Deneyi başlat
python main_experiment.py
```

Veya script dosyalarını kullan:

| Platform | Komut |
|----------|-------|
| **macOS/Linux** | `./run_experiment.sh` |
| **Windows** | `run_experiment.bat` |

---

## Deney Akışı

### Genel Akış

```
Katılımcı Bilgileri Dialog → Onay Formu → Hoşgeldiniz → Talimatlar
    → (EyeLink Kalibrasyon) → Alıştırma Denemesi → Ana Deney → Bitiş
```

### Tek Deneme (Trial) Yapısı

Videolar **ardışık** (sequential) olarak ekranın ortasında **1600×900 piksel** boyutunda gösterilir.

```
┌─────────────────────────────────────────────────────────────────┐
│  1. SORU ÖNİZLEME       │ 3 saniye │ Soru ekranda gösterilir  │
│  2. FİKSASYON ÇARPISI   │ 1 saniye │ Ekran ortasında (+)       │
│  3. "Video 1" ETİKETİ   │ 1 saniye │ Hangi videonun geleceği   │
│  4. VİDEO 1             │ ~16 sn   │ Ortada, 1600×900          │
│  5. ARA FİKSASYON       │ 1 saniye │ İki video arasında (+)    │
│  6. "Video 2" ETİKETİ   │ 1 saniye │ Hangi videonun geleceği   │
│  7. VİDEO 2             │ ~16 sn   │ Ortada, 1600×900          │
│  8. SEÇİM EKRANI        │ Yanıta  │ Soru + "1" veya "2" tuşu │
│                          │  kadar   │                           │
│  9. GÜVEN DERECESİ       │ Yanıta  │ 1-5 arası puan           │
│                          │  kadar   │                           │
│ 10. DENEME ARASI (ITI)   │ 0.5 sn  │ Boş ekran                │
└─────────────────────────────────────────────────────────────────┘
```

### Tuş Kontrolleri

| Tuş | İşlev |
|-----|-------|
| **1** | Birinci videoyu seç |
| **2** | İkinci videoyu seç |
| **1-5** | Güven derecesi puanla |
| **SPACE** | Devam et / Onayla |
| **ESC** | Deneyi sonlandır |

### Deney Parametreleri

| Parametre | Değer |
|-----------|-------|
| Kişilik özellikleri | 5 (Extraversion, Agreeableness, Conscientiousness, Emotional Stability, Openness) |
| Özellik başına deneme | 25 (5 HIGH × 5 LOW video) |
| Toplam deneme | 125 |
| Alıştırma denemesi | 1 |
| Mola sıklığı | Her 20 denemede bir |
| Video boyutu | 1600 × 900 piksel |
| Video süresi | ~16 saniye |

---

## Proje Yapısı

```
user_study_project/
├── main_experiment.py              # Ana deney scripti
├── config.py                       # Tüm yapılandırma parametreleri
├── trial_manager.py                # Deneme oluşturma ve yönetimi
├── data_logger.py                  # Veri kayıt aracı
├── eyelink_utils.py                # EyeLink 1000 Plus entegrasyonu (pylink API)
├── EyeLinkCoreGraphicsPsychoPy.py  # SR Research kalibrasyon grafikleri
├── requirements.txt                # Python bağımlılıkları
├── README.md                       # Bu dosya
│
├── run_experiment.sh               # macOS/Linux çalıştırma scripti
├── run_experiment.bat              # Windows çalıştırma scripti
├── lab_setup.bat                   # Windows lab kurulum scripti
│
├── error.wav                       # EyeLink kalibrasyon ses dosyaları
├── qbeep.wav
├── type.wav
│
├── stimuli/
│   └── videos/
│       └── study_videos/           # Kişilik özelliğine göre organize
│           ├── extraversion/
│           │   ├── high/           # 5 yüksek extraversion videosu
│           │   └── low/            # 5 düşük extraversion videosu
│           ├── agreeableness/
│           ├── conscientiousness/
│           ├── emotional_stability/
│           └── openness/
│
├── data/                           # Davranışsal veri çıktısı (CSV)
├── trials/                         # Oluşturulan deneme listeleri
└── eyelink_data/                   # EyeLink göz izleme verileri (EDF)
```

---

## Kurulum

### Gereksinimler

| Gereksinim | Minimum | Önerilen |
|------------|---------|----------|
| **İşletim Sistemi** | Windows 10 / macOS 10.15 | Windows 10/11 |
| **Python** | 3.10.x | 3.10.x (⚠️ 3.11+ desteklenmiyor) |
| **RAM** | 8 GB | 16 GB |
| **Disk** | 5 GB boş alan | 10 GB+ |
| **Ekran** | 1920×1080 | 1920×1080 @ 60Hz+ |

### Python Ortamı (Conda)

```bash
# 1. Miniconda yükle (yoksa): https://docs.conda.io/en/latest/miniconda.html

# 2. Yeni ortam oluştur (Python 3.10)
conda create -n psychopy-env python=3.10 -y

# 3. Ortamı aktifle
conda activate psychopy-env

# 4. Bağımlılıkları yükle
cd ~/Documents/GitHub/490-user-study/user_study_project
pip install psychopy numpy pandas opencv-python Pillow

# 5. Kurulumu test et
python -c "from psychopy import visual, core, event; print('✓ PsychoPy çalışıyor!')"
python -c "import cv2; print('✓ OpenCV çalışıyor!')"
```

### pylink Kurulumu

pylink, SR Research'ün EyeLink donanımını Python'dan kontrol etmek için kullandığı kütüphanedir.

#### Yöntem 1: pip ile kurulum (Önerilen)

```bash
conda activate psychopy-env
pip install sr-research-pylink
```

> ⚠️ **DİKKAT:** `sr-research-pylink` paketinin `__init__.py` dosyası eksik olabiliyor.
> Import hatası alırsanız aşağıdaki düzeltmeyi uygulayın:

```bash
# __init__.py konumunu bul
python -c "import importlib.util; spec = importlib.util.find_spec('pylink'); print(spec.submodule_search_locations[0] if spec else 'pylink bulunamadı')"
```

Eğer klasör mevcutsa ama import başarısızsa, o klasöre `__init__.py` oluşturun:

```python
# <pylink_klasörü>/__init__.py dosyasının içeriği:
from pylink.constants import *
from pylink.eyelink import *
from pylink.tracker import *
from pylink.pylink_c import msecDelay, pumpDelay
```

#### Yöntem 2: EyeLink Developers Kit ile

1. SR Research hesabı oluşturun: https://www.sr-research.com/support/
2. **EyeLink Developers Kit** indirin (işletim sisteminize göre)
3. Kurulum sırasında pylink otomatik yüklenir

#### Doğrulama

```bash
python -c "
import pylink
print('✓ pylink modülü yüklendi')
print(f'  EyeLink class: {pylink.EyeLink}')
print(f'  TRIAL_OK: {pylink.TRIAL_OK}')
print(f'  pumpDelay: {pylink.pumpDelay}')
"
```

> ⚠️ **ÖNEMLİ:** `pip install pylink` komutu ile SR Research'ün pylink'ini **karıştırmayın**.
> `pylink` (PyLink) farklı bir serial link kütüphanesidir. Eğer yanlışlıkla yüklediyseniz:
> ```bash
> pip uninstall pylink
> pip install sr-research-pylink
> ```

### EyeLink Developers Kit

EyeLink Developers Kit (EDK), Display PC'de gerekli olan tüm araçları içerir:

1. **SR Research Support Forum'a kayıt olun:** https://www.sr-research.com/support/
2. **Downloads bölümüne gidin**
3. İşletim sisteminize uygun **EyeLink Developers Kit** indirin:
   - **macOS:** `EyeLink Developers Kit for Mac`
   - **Windows:** `EyeLink Developers Kit for Windows`
4. Kurulum sırasında gelen tüm bileşenleri yükleyin:
   - `pylink` (Python kütüphanesi)
   - `edf2asc` (EDF → ASCII dönüştürücü)
   - Örnek kodlar ve dokümantasyon

> **Not:** Kit ücretsizdir ancak forum hesabı gerektirir. Hesap onayı 1-2 iş günü sürebilir.

---

## Lab Kurulumu (2 Bilgisayar)

EyeLink 1000 Plus, **2 bilgisayarlı mimari** kullanır:

```
┌──────────────────────┐  Ethernet  ┌──────────────────────┐
│    HOST PC            │◄──────────►│    DISPLAY PC         │
│    (SR Research)      │ 100.1.1.x  │    (Deney bilgisayarı)│
│                       │            │                       │
│  • EyeLink Host App  │            │  • PsychoPy + pylink  │
│  • Kamera kontrolü    │            │  • Video gösterimi     │
│  • Göz izleme         │            │  • Yanıt toplama       │
│  • Kalibrasyon        │            │  • main_experiment.py  │
│                       │            │                       │
│  IP: 100.1.1.1        │            │  IP: 100.1.1.2         │
└──────────────────────┘            └──────────────────────┘
```

### Host PC (SR Research bilgisayarı)

- EyeLink Host yazılımı önceden kurulu gelir
- Kamerayı kontrol eder, göz pozisyonunu hesaplar
- IP adresi: `100.1.1.1` (varsayılan)
- **Bizim kodumuz bu bilgisayarda çalışmaz**

### Display PC (Deney bilgisayarı)

Bu bilgisayarda yapılması gerekenler:

1. **Ağ ayarları:**
   - Ethernet IP: `100.1.1.2`
   - Subnet Mask: `255.255.255.0`
   - Gateway: boş bırakın

2. **Yazılım kurulumu:**
   - Conda + Python 3.10 (`psychopy-env`)
   - PsychoPy, OpenCV, pylink
   - Bu proje dosyaları

3. **Test:**
   ```bash
   # EyeLink bağlantı testi
   ping 100.1.1.1

   # pylink testi
   python -c "import pylink; el = pylink.EyeLink('100.1.1.1'); print('Bağlandı!'); el.close()"
   ```

### Windows Lab Hızlı Kurulum

`lab_setup.bat` dosyasını çift tıklayarak otomatik kurulum yapabilirsiniz:

```cmd
cd C:\Users\...\490-user-study\user_study_project
lab_setup.bat
```

---

## Deneyi Çalıştırma

### Her Oturum Öncesi

1. EyeLink Host PC'yi açın ve Host yazılımını başlatın
2. Display PC'de terminal açın:

```bash
conda activate psychopy-env
cd ~/Documents/GitHub/490-user-study/user_study_project
python main_experiment.py
```

### Katılımcı Bilgileri Diyaloğu

Deney başladığında şu bilgiler istenir:

| Alan | Açıklama | Örnek |
|------|----------|-------|
| **Participant ID** | Benzersiz katılımcı kodu | P001 |
| **Session** | Oturum numarası | 1 |
| **Enable Eye Tracking** | EyeLink checkbox'ı | ☑ (işaretli) |
| **Include Practice** | Alıştırma denemeleri dahil mi | ☑ (işaretli) |

> **Enable Eye Tracking** kutucuğu işaretlendiğinde `config.EYELINK_ENABLED = True` olur
> ve EyeLink bağlantısı/kalibrasyon otomatik başlatılır.

### EyeLink Kalibrasyon

EyeLink etkinse, deney başlamadan önce:

1. **Kalibrasyon ekranı** açılır (9 noktalı HV9)
2. Katılımcı her noktaya bakar
3. Kalibrasyon başarılı olduktan sonra deney başlar
4. Her denemede (alıştırma hariç) **drift correction** yapılır

### EyeLink'siz Çalıştırma

EyeLink bağlı değilken deney yine çalışır:
- Checkbox'ı işaretlemeyin → göz izleme devre dışı
- Tüm EyeLink çağrıları `[EYELINK SIMULATED]` olarak loglanır
- Davranışsal veriler normal şekilde kaydedilir

### Dummy Mode

EyeLink donanımı olmadan göz izleme akışını test etmek için:

```python
# config.py içinde:
EYELINK_DUMMY_MODE = True
EYELINK_ENABLED = True  # veya dialog'dan checkbox'ı işaretleyin
```

Bu modda pylink simüle edilmiş bir tracker oluşturur, kalibrasyon ve drift correction ekranları açılır ama gerçek göz verisi kaydedilmez.

---

## Konfigürasyon

Tüm parametreler `config.py` dosyasında düzenlenebilir:

### Zamanlama

| Parametre | Varsayılan | Açıklama |
|-----------|-----------|----------|
| `FIXATION_DURATION` | 1.0 sn | Fiksasyon çarpısı süresi |
| `VIDEO_DURATION` | 16.0 sn | Video gösterim süresi |
| `INTER_VIDEO_INTERVAL` | 1.0 sn | İki video arası bekleme |
| `VIDEO_LABEL_DURATION` | 1.0 sn | "Video 1/2" etiketi süresi |
| `INTER_TRIAL_INTERVAL` | 0.5 sn | Denemeler arası bekleme |

### Video Görüntüleme

| Parametre | Varsayılan | Açıklama |
|-----------|-----------|----------|
| `VIDEO_WIDTH` | 1600 px | Video genişliği |
| `VIDEO_HEIGHT` | 900 px | Video yüksekliği |
| `VIDEO_POSITION` | (0, 0) | Ekran ortası |

### Yanıt Tuşları

| Parametre | Varsayılan | Açıklama |
|-----------|-----------|----------|
| `KEY_FIRST` | "1" | Birinci video seçimi |
| `KEY_SECOND` | "2" | İkinci video seçimi |
| `KEY_QUIT` | "escape" | Deneyi sonlandır |

### EyeLink

| Parametre | Varsayılan | Açıklama |
|-----------|-----------|----------|
| `EYELINK_ENABLED` | False | EyeLink aktif mi |
| `EYELINK_DUMMY_MODE` | False | Simülasyon modu |
| `USE_RETINA` | False | Retina ekran düzeltmesi |
| `EYELINK_IP` | "100.1.1.1" | Host PC IP adresi |
| `EYELINK_SAMPLE_RATE` | 1000 Hz | Örnekleme hızı |
| `EYELINK_CALIBRATION_TYPE` | "HV9" | 9 noktalı kalibrasyon |

---

## Veri Çıktıları

### Davranışsal Veri (`data/`)

Her katılımcı için CSV dosyası oluşturulur:

**Dosya adı:** `participant_P001_2026-01-27_1430.csv`

| Sütun | Açıklama |
|-------|----------|
| `participant_id` | Katılımcı kodu |
| `session` | Oturum numarası |
| `trial_id` | Deneme numarası |
| `trait` | Kişilik özelliği |
| `video_first` | İlk gösterilen video |
| `video_second` | İkinci gösterilen video |
| `high_position` | HIGH video'nun konumu ("first" / "second") |
| `response` | Katılımcı yanıtı ("first" / "second") |
| `response_correct` | HIGH video seçildi mi? |
| `response_time` | Yanıt süresi (saniye) |
| `confidence_rating` | Güven derecesi (1-5) |

### Göz İzleme Verisi (`eyelink_data/`)

EyeLink verileri EDF (EyeLink Data File) formatında kaydedilir:

**Dosya adı:** `P001.edf` (deney bitiminde Host PC'den Display PC'ye aktarılır)

| Veri Türü | Örnekleme | Açıklama |
|-----------|-----------|----------|
| Bakış pozisyonu | 1000 Hz | X, Y koordinatları (piksel) |
| Pupil boyutu | 1000 Hz | Göz bebeği çapı |
| Fiksasyonlar | Olay bazlı | Konum, süre |
| Sakkadlar | Olay bazlı | Genlik, hız, yön |
| Göz kırpmalar | Olay bazlı | Süre, zamanlama |

### EDF İçindeki Mesajlar

Deney sırasında EDF dosyasına gönderilen SR Research Data Viewer uyumlu mesajlar:

```
TRIALID 1
QUESTION_PREVIEW_ONSET
QUESTION_PREVIEW_OFFSET
FIXATION_ONSET
FIXATION_OFFSET
VIDEO_1_ONSET
!V VFRAME <frame_no> <x> <y> <video.avi>
VIDEO_1_OFFSET
VIDEO_2_ONSET
VIDEO_2_OFFSET
SELECTION_SCREEN_ONSET
SELECTION_SCREEN_OFFSET
CONFIDENCE_SCREEN_ONSET
CONFIDENCE_SCREEN_OFFSET
TRIAL_END
```

### EDF İçindeki Deneme Değişkenleri

Data Viewer'da analiz için her denemeye eklenen değişkenler:

```
!V TRIAL_VAR trait Extraversion
!V TRIAL_VAR video_first extraversion_high_01.mp4
!V TRIAL_VAR video_second extraversion_low_03.mp4
!V TRIAL_VAR high_position first
!V TRIAL_VAR response first
!V TRIAL_VAR response_correct True
!V TRIAL_VAR response_time 1.234
!V TRIAL_VAR confidence 4
!V TRIAL_VAR is_practice False
TRIAL_RESULT 0
```

### İlgi Alanları (Interest Areas)

Video gösterim bölgesi etrafında otomatik tanımlanan dikdörtgen ilgi alanı:

```
┌──────────────────────────────────────┐
│              1920 × 1080             │
│    ┌──────────────────────────┐      │
│    │                          │      │
│    │     VIDEO (1600×900)     │      │
│    │     Interest Area 1      │      │
│    │     (20px padding)       │      │
│    │                          │      │
│    └──────────────────────────┘      │
│                                      │
└──────────────────────────────────────┘
```

### EDF → ASCII Dönüşümü

```bash
# SR Research edf2asc aracı ile (EDK ile birlikte gelir)
edf2asc P001.edf
# Çıktı: P001.asc
```

---

## Sorun Giderme

### Sık Karşılaşılan Hatalar

**1. `ModuleNotFoundError: No module named 'psychopy'`**
```bash
conda activate psychopy-env
pip install psychopy
```

**2. `import pylink` hatası**
```bash
# sr-research-pylink yüklü mü kontrol et
pip list | grep pylink

# Yanlış pylink yüklüyse kaldır
pip uninstall pylink
pip install sr-research-pylink

# __init__.py eksikse yukarıdaki talimatları uygula
```

**3. EyeLink bağlantı hatası**
- Ethernet kablosu bağlı mı?
- Host PC IP: `100.1.1.1` mi?
- Display PC IP: `100.1.1.2` mi?
- EyeLink Host yazılımı çalışıyor mu?
- `ping 100.1.1.1` başarılı mı?

**4. Video oynatma hatası**
```bash
pip install opencv-python Pillow
# Video codec'i H.264 olmalı
```

**5. Retina ekran sorunu (macOS)**
```python
# config.py içinde:
USE_RETINA = True
```

**6. `Could not measure frame rate`**
- Monitör ölçümü desteklemeyebilir
- Varsayılan 60Hz kullanılır
- Tam ekran modunda çalıştırın

---

## Teknoloji Yığını

| Bileşen | Versiyon | Kullanım |
|---------|---------|----------|
| Python | 3.10.x | Programlama dili |
| PsychoPy | 2025.2.4 | Deney çerçevesi, görsel uyaran, zamanlama |
| OpenCV | 4.x | Video okuma (cv2.VideoCapture) |
| Pillow | - | Kare dönüşümü (BGR→RGB→PIL.Image) |
| pylink (sr-research) | 2.1.x | EyeLink donanım kontrolü |
| NumPy | 1.x | Sayısal hesaplama |
| Pandas | 1.x | Veri kayıt / CSV |

---

## Kurulum Kontrol Listesi

```
┌─────────────────────────────────────────────────────────────────┐
│                     KURULUM KONTROL LİSTESİ                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  □ Git yüklü                    → git --version                 │
│  □ Conda yüklü                  → conda --version               │
│  □ Repo klonlandı               → git clone ...                 │
│  □ Python 3.10 ortamı           → conda activate psychopy-env   │
│  □ PsychoPy yüklü               → python -c "import psychopy"   │
│  □ OpenCV yüklü                  → python -c "import cv2"        │
│  □ pylink yüklü (sr-research)   → python -c "import pylink"     │
│  □ EyeLink Developers Kit       → edf2asc komutu çalışıyor      │
│  □ Dizinler oluşturuldu         → data/, trials/, eyelink_data/ │
│  □ Videolar eklendi             → stimuli/videos/study_videos/   │
│  □ EyeLink Host PC bağlı       → ping 100.1.1.1                 │
│  □ Display PC IP ayarlandı      → 100.1.1.2                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Bağlantılar

- [PsychoPy Dokümantasyonu](https://www.psychopy.org/)
- [SR Research Destek](https://www.sr-research.com/support/)
- [PsychoPy Forum](https://discourse.psychopy.org/)
- [EyeLink 1000 Plus Kullanım Kılavuzu](../EyeLink_1000_Plus_User_Manual_1.0.12.pdf)

---

## Versiyon Geçmişi

- **2.0.0** — EyeLink 1000 Plus entegrasyonu, ardışık video gösterim, soru-önce akışı
- **1.0.0** — İlk sürüm (placeholder uyaranlar)

---

**Danışman:** Prof. Dr. Uğur Güdükbay — Bilkent Üniversitesi, Bilgisayar Mühendisliği Bölümü
