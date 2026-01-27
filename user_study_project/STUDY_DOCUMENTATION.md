# Pairwise Personality Perception User Study

## Çalışma Açıklaması ve Teknik Dokümantasyon

**Proje:** Yüz Videolarından Kişilik Algısı Çalışması  
**Danışman:** Prof. Dr. Uğur Güdükbay, Bilkent Üniversitesi  
**Tarih:** Ocak 2026

---

## 1. Çalışmanın Amacı

Bu kullanıcı çalışması, insanların kısa yüz videolarından kişilik özelliklerini nasıl algıladığını araştırmaktadır. Katılımcılar, aynı kişilik özelliği üzerinde **YÜKSEK** ve **DÜŞÜK** olarak derecelendirilmiş iki kişinin videosunu yan yana izleyerek, hangi kişinin o özelliğe daha fazla sahip göründüğünü değerlendirmektedir.

### Araştırma Soruları

1. İnsanlar yüz videolarından kişilik özelliklerini ne kadar doğru algılayabilir?
2. Algı sürecinde göz hareketleri hangi yüz bölgelerine odaklanır?
3. Farklı kişilik özellikleri için algı doğruluğu ve göz hareketi örüntüleri nasıl değişir?

---

## 2. Deneysel Tasarım

### 2.1 Kişilik Özellikleri (Big Five Modeli)

Çalışma, beş temel kişilik özelliğini kapsamaktadır:

| Özellik | İngilizce | Açıklama |
|---------|-----------|----------|
| **Dışadönüklük** | Extraversion | Sosyal, enerjik, konuşkan |
| **Uyumluluk** | Agreeableness | Arkadaş canlısı, işbirlikçi, sıcakkanlı |
| **Sorumluluk** | Conscientiousness | Organize, güvenilir, disiplinli |
| **Duygusal Denge** | Emotional Stability | Sakin, strese dayanıklı, dengeli |
| **Deneyime Açıklık** | Openness | Yaratıcı, meraklı, yeniliklere açık |

### 2.2 Deneme (Trial) Yapısı

Her deneme şu aşamalardan oluşmaktadır:

```
┌─────────────────────────────────────────────────────────────────┐
│  1. Fiksasyon (+)     │  1 saniye                               │
├─────────────────────────────────────────────────────────────────┤
│  2. Video Sunumu      │  ~16 saniye (video süresi kadar)        │
│     ┌───────┐ ┌───────┐                                         │
│     │ Video │ │ Video │  ← Yan yana iki video                   │
│     │  SOL  │ │  SAĞ  │                                         │
│     └───────┘ └───────┘                                         │
├─────────────────────────────────────────────────────────────────┤
│  3. Soru Ekranı       │  Yanıt verene kadar                     │
│     "Hangi kişi daha [özellik] görünüyor?"                      │
├─────────────────────────────────────────────────────────────────┤
│  4. Yanıt             │  Sol/Sağ ok tuşları                     │
├─────────────────────────────────────────────────────────────────┤
│  5. Güven Derecesi    │  1-5 arası (1=çok belirsiz, 5=çok emin) │
├─────────────────────────────────────────────────────────────────┤
│  6. Boşluk (ITI)      │  0.5 saniye                             │
└─────────────────────────────────────────────────────────────────┘
```

### 2.3 Soru Formatları

Her kişilik özelliği için açıklayıcı sorular kullanılmaktadır:

| Özellik | Soru |
|---------|------|
| Dışadönüklük | "Which person appears more outgoing, sociable, and energetic?" |
| Uyumluluk | "Which person appears more friendly, cooperative, and warm?" |
| Sorumluluk | "Which person appears more organized, responsible, and reliable?" |
| Duygusal Denge | "Which person appears more calm, emotionally stable, and resilient?" |
| Deneyime Açıklık | "Which person appears more open to new experiences, creative, and curious?" |

### 2.4 Deneme Sayısı ve Tasarım

- **Toplam video sayısı:** 50 video (5 özellik × 2 seviye × 5 video)
- **Her özellik için:** 5 YÜKSEK + 5 DÜŞÜK video
- **Eşleştirme:** Full factorial design (her YÜKSEK video, her DÜŞÜK video ile eşleşir)
- **Deneme sayısı:** 5 × 5 = 25 deneme/özellik × 5 özellik = **125 toplam deneme**
- **Tahmini süre:** ~45-60 dakika (molalar dahil)

### 2.5 Randomizasyon

- Deneme sırası rastgele karıştırılır
- **Özellik tekrarı önleme:** Aynı özellik art arda gelmez (minimum 2 deneme aralık)
- **Pozisyon dengeleme:** YÜKSEK video bazen solda, bazen sağda gösterilir

---

## 3. Stimuli (Video Uyaranlar)

### 3.1 Video Özellikleri

| Özellik | Değer |
|---------|-------|
| **Format** | MP4 (H.264 codec) |
| **Süre** | ~15-16 saniye |
| **Çözünürlük** | Orijinal (değişken) |
| **İçerik** | Yüz videoları |

### 3.2 Video Organizasyonu

```
stimuli/videos/study_videos/
├── extraversion/
│   ├── high/          # 5 yüksek dışadönüklük videosu
│   │   ├── video1.mp4
│   │   ├── video2.mp4
│   │   └── ...
│   └── low/           # 5 düşük dışadönüklük videosu
├── agreeableness/
│   ├── high/
│   └── low/
├── conscientiousness/
│   ├── high/
│   └── low/
├── emotional_stability/
│   ├── high/
│   └── low/
└── openness/
    ├── high/
    └── low/
```

### 3.3 Video Normalizasyonu

> ⚠️ **ÖNEMLİ:** Videolara herhangi bir normalizasyon veya ön işleme uygulanmamıştır.

**Yapılmayan işlemler:**
- Parlaklık/kontrast normalizasyonu
- Yüz hizalama (face alignment)
- Arka plan kaldırma
- Renk düzeltme
- Boyut standardizasyonu

---

## 4. Göz İzleme (Eye Tracking)

### 4.1 Ekipman

| Özellik | Değer |
|---------|-------|
| **Cihaz** | EyeLink 1000 Plus |
| **Örnekleme Hızı** | 1000 Hz |
| **Doğruluk** | < 0.5° görsel açı |
| **Bağlantı** | Ethernet (IP: 100.1.1.1) |

### 4.2 Kalibrasyon

- **Tip:** 9 noktalı HV9 kalibrasyon
- **Kabul kriteri:** < 1.0° ortalama hata
- **Doğrulama:** Her oturumun başında

### 4.3 İlgi Alanları (Areas of Interest)

Her denemede iki ilgi alanı tanımlanmaktadır:

```
┌────────────────────────────────────────────────────┐
│                                                    │
│   ┌─────────────┐         ┌─────────────┐         │
│   │             │         │             │         │
│   │  LEFT_VIDEO │         │ RIGHT_VIDEO │         │
│   │   (AOI 1)   │         │   (AOI 2)   │         │
│   │             │         │             │         │
│   └─────────────┘         └─────────────┘         │
│                                                    │
└────────────────────────────────────────────────────┘
```

### 4.4 Kaydedilen Göz İzleme Verileri

- Göz pozisyonu (x, y koordinatları)
- Pupil boyutu
- Fiksasyonlar ve sakkadlar
- Her deneme için zaman damgaları (onset/offset)
- İlgi alanı geçişleri

---

## 5. Veri Toplama

### 5.1 Davranışsal Veriler

Her deneme için kaydedilen değişkenler:

| Değişken | Açıklama |
|----------|----------|
| `participant_id` | Katılımcı kimliği |
| `trial_id` | Deneme numarası |
| `trait` | Kişilik özelliği |
| `video_left` | Sol video dosya adı |
| `video_right` | Sağ video dosya adı |
| `high_position` | YÜKSEK videonun pozisyonu (sol/sağ) |
| `response` | Katılımcı yanıtı (sol/sağ) |
| `response_correct` | Yanıt doğru mu? (YÜKSEK seçildi mi?) |
| `response_time` | Yanıt süresi (saniye) |
| `confidence_rating` | Güven derecesi (1-5) |

### 5.2 Veri Dosyaları

```
data/
├── participant_P001_20260127_143052.csv      # Deneme verileri
├── participant_P001_20260127_143052_events.csv   # Olay logları
└── participant_P001_20260127_143052_summary.json # Özet istatistikler

eyelink_data/
└── el20260127_143052.edf    # EyeLink ham veri dosyası
```

### 5.3 Örnek Veri Formatı

**CSV Çıktısı:**
```csv
participant_id,trial_id,trait,video_left,video_right,high_position,response,response_correct,response_time,confidence_rating
P001,1,Extraversion,84emxO86qa8.001.mp4,3zAyM2edy1g.004.mp4,left,left,True,2.34,4
P001,2,Agreeableness,MvWDky9ZaWU.000.mp4,oxw3nT9LSsg.000.mp4,right,right,True,1.87,5
```

---

## 6. Deney Akışı

```
┌─────────────────────────────────────────────────────────────────┐
│                    DENEY AKIŞI                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │  Katılımcı Bilgileri │
                   │  (ID, Oturum No)     │
                   └──────────┬──────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │  Hoş Geldiniz Ekranı │
                   │  (Danışman bilgisi)  │
                   └──────────┬──────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │  Talimatlar         │
                   └──────────┬──────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │  Göz İzleme         │
                   │  Kalibrasyonu       │
                   └──────────┬──────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │  Alıştırma Denemesi │
                   │  (1 deneme)         │
                   └──────────┬──────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │  Ana Deney          │
                   │  (125 deneme)       │
                   │                     │
                   │  Her 20 denemede    │
                   │  mola               │
                   └──────────┬──────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │  Teşekkür Ekranı    │
                   └─────────────────────┘
```

---

## 7. Teknik Altyapı

### 7.1 Yazılım

| Bileşen | Sürüm |
|---------|-------|
| **Python** | 3.10.x |
| **PsychoPy** | 2025.2.4 |
| **OpenCV** | 4.x |
| **NumPy** | 1.x |
| **Pandas** | 2.x |
| **pylink** | SR Research |

### 7.2 Donanım Gereksinimleri

| Bileşen | Minimum | Önerilen |
|---------|---------|----------|
| **İşletim Sistemi** | Windows 10 / macOS 10.15 | Windows 10/11 |
| **RAM** | 8 GB | 16 GB |
| **Ekran** | 1920×1080 | 1920×1080 @ 60Hz+ |
| **Göz İzleyici** | EyeLink 1000 Plus | EyeLink 1000 Plus |

### 7.3 Proje Dosyaları

```
user_study_project/
├── main_experiment.py      # Ana deney scripti
├── config.py               # Tüm ayarlar
├── trial_manager.py        # Deneme yönetimi
├── data_logger.py          # Veri kayıt
├── eyelink_utils.py        # EyeLink entegrasyonu
├── run_experiment.sh       # macOS çalıştırma
├── run_experiment.bat      # Windows çalıştırma
├── requirements.txt        # Python bağımlılıkları
└── README.md               # Teknik dokümantasyon
```

---

## 8. Analiz Planı

### 8.1 Davranışsal Analiz

1. **Doğruluk Analizi**
   - Her özellik için ortalama doğruluk oranı
   - Şans seviyesi (%50) ile karşılaştırma
   - Özellikler arası karşılaştırma

2. **Yanıt Süresi Analizi**
   - Doğru vs yanlış yanıtlar için RT
   - Özellik bazında RT farklılıkları

3. **Güven-Doğruluk İlişkisi**
   - Yüksek güvenli yanıtlar daha doğru mu?

### 8.2 Göz İzleme Analizi

1. **Bakış Dağılımı**
   - Sol vs sağ video için toplam bakış süresi
   - Seçilen vs seçilmeyen video karşılaştırması

2. **Fiksasyon Örüntüleri**
   - Ortalama fiksasyon süresi
   - Fiksasyon sayısı
   - İlk fiksasyon lokasyonu

3. **Geçiş Analizi**
   - İki video arasındaki geçiş sayısı
   - Karar öncesi son bakış

---

## 9. Etik Hususlar

- Katılımcılar bilgilendirilmiş onam formu imzalar
- Kişisel veriler anonim tutulur
- Göz izleme verileri güvenli şekilde saklanır
- Katılımcılar istedikleri zaman çalışmadan çekilebilir

---

## 10. İletişim

**Proje Danışmanı:**  
Prof. Dr. Uğur Güdükbay  
Bilkent Üniversitesi  
Bilgisayar Mühendisliği Bölümü

---

*Bu doküman, Ocak 2026 tarihinde hazırlanmıştır.*
