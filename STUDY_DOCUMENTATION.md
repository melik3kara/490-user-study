# Pairwise Personality Perception User Study

## Çalışma Açıklaması ve Teknik Dokümantasyon

**Proje:** Yüz Videolarından Kişilik Algısı Çalışması  
**Danışman:** Prof. Dr. Uğur Güdükbay, Bilkent Üniversitesi  
**Tarih:** Ocak 2026

---


## 1. Deneysel Tasarım

### 1.1 Kişilik Özellikleri (Big Five Modeli)

Çalışma, beş temel kişilik özelliğini kapsamaktadır:

| Özellik | İngilizce | Açıklama |
|---------|-----------|----------|
| **Dışadönüklük** | Extraversion | Sosyal, enerjik, konuşkan |
| **Uyumluluk** | Agreeableness | Arkadaş canlısı, işbirlikçi, sıcakkanlı |
| **Sorumluluk** | Conscientiousness | Organize, güvenilir, disiplinli |
| **Duygusal Denge** | Emotional Stability | Sakin, strese dayanıklı, dengeli |
| **Deneyime Açıklık** | Openness | Yaratıcı, meraklı, yeniliklere açık |

### 1.2 Deneme (Trial) Yapısı

Her deneme şu aşamalardan oluşmaktadır:

```
┌─────────────────────────────────────────────────────────────────┐
│  1. Fiksasyon (+)     │  1 saniye                               │
├─────────────────────────────────────────────────────────────────┤
│  2. "Video 1" Etiketi │  1 saniye                               │
├─────────────────────────────────────────────────────────────────┤
│  3. Video 1 Sunumu    │  ~16 saniye (video süresi kadar)        │
│     ┌─────────────┐                                             │
│     │             │  ← Ekran ortasında tek video                │
│     │   VIDEO 1   │                                             │
│     │             │                                             │
│     └─────────────┘                                             │
├─────────────────────────────────────────────────────────────────┤
│  4. Ara Fiksasyon (+) │  1 saniye                               │
├─────────────────────────────────────────────────────────────────┤
│  5. "Video 2" Etiketi │  1 saniye                               │
├─────────────────────────────────────────────────────────────────┤
│  6. Video 2 Sunumu    │  ~16 saniye (video süresi kadar)        │
│     ┌─────────────┐                                             │
│     │             │  ← Aynı pozisyonda ikinci video             │
│     │   VIDEO 2   │                                             │
│     │             │                                             │
│     └─────────────┘                                             │
├─────────────────────────────────────────────────────────────────┤
│  7. Soru Ekranı       │  Yanıt verene kadar                     │
│     "Hangi kişi daha [özellik] görünüyor?"                      │
├─────────────────────────────────────────────────────────────────┤
│  8. Yanıt             │  1 = Birinci video, 2 = İkinci video    │
├─────────────────────────────────────────────────────────────────┤
│  9. Güven Derecesi    │  1-5 arası (1=çok belirsiz, 5=çok emin) │
├─────────────────────────────────────────────────────────────────┤
│ 10. Boşluk (ITI)      │  0.5 saniye                             │
└─────────────────────────────────────────────────────────────────┘
```

**Not:** Videolar aynı ekran pozisyonunda (ortada) sırayla gösterilir. Bu tasarım, 
göz izleme heatmap'lerinin video pozisyonundan etkilenmemesini sağlar ve 
katılımcıların videoların hangi bölgelerine odaklandığını analiz etmeyi kolaylaştırır.

### 2.3 Soru Formatları

Her kişilik özelliği için açıklayıcı sorular kullanılmaktadır:

| Özellik | Soru |
|---------|------|
| Dışadönüklük | "Which person appears more outgoing, sociable, and energetic?" |
| Uyumluluk | "Which person appears more friendly, cooperative, and warm?" |
| Sorumluluk | "Which person appears more organized, responsible, and reliable?" |
| Duygusal Denge | "Which person appears more calm, emotionally stable, and resilient?" |
| Deneyime Açıklık | "Which person appears more open to new experiences, creative, and curious?" |

### 1.4 Deneme Sayısı ve Tasarım

- **Toplam video sayısı:** 50 video (5 özellik × 2 seviye × 5 video)
- **Her özellik için:** 5 YÜKSEK + 5 DÜŞÜK video
- **Eşleştirme:** Full factorial design (her YÜKSEK video, her DÜŞÜK video ile eşleşir)
- **Deneme sayısı:** 5 × 5 = 25 deneme/özellik × 5 özellik = **125 toplam deneme**
- **Tahmini süre:** ~45-60 dakika (molalar dahil)

### 1.5 Randomizasyon

- Deneme sırası rastgele karıştırılır
- **Özellik tekrarı önleme:** Aynı özellik art arda gelmez (minimum 2 deneme aralık)
- **Pozisyon dengeleme:** YÜKSEK video bazen solda, bazen sağda gösterilir

---

## 2. Stimuli (Video Uyaranlar)

### 2.1 Video Özellikleri

| Özellik | Değer |
|---------|-------|
| **Format** | MP4 (H.264 codec) |
| **Süre** | ~15-16 saniye |
| **Çözünürlük** | Orijinal (değişken) |
| **İçerik** | Yüz videoları |

### 2.2 Video Organizasyonu

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

### 2.3 Video Normalizasyonu

> ⚠️ **ÖNEMLİ:** Videolara herhangi bir normalizasyon veya ön işleme uygulanmamıştır.

**Yapılmayan işlemler:**
- Parlaklık/kontrast normalizasyonu
- Yüz hizalama (face alignment)
- Arka plan kaldırma
- Renk düzeltme
- Boyut standardizasyonu

---

## 3. Göz İzleme (Eye Tracking)

### 3.1 Ekipman

| Özellik | Değer |
|---------|-------|
| **Cihaz** | EyeLink 1000 Plus |
| **Örnekleme Hızı** | 1000 Hz |
| **Doğruluk** | < 0.5° görsel açı |
| **Bağlantı** | Ethernet (IP: 100.1.1.1) |

### 3.2 Kalibrasyon

- **Tip:** 9 noktalı HV9 kalibrasyon
- **Kabul kriteri:** < 1.0° ortalama hata
- **Doğrulama:** Her oturumun başında

### 3.3 İlgi Alanları (Areas of Interest)

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

### 3.4 Kaydedilen Göz İzleme Verileri

- Göz pozisyonu (x, y koordinatları)
- Pupil boyutu
- Fiksasyonlar ve sakkadlar
- Her deneme için zaman damgaları (onset/offset)
- İlgi alanı geçişleri

---

## 4. Veri Toplama

### 4.1 Davranışsal Veriler

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

### 4.2 Veri Dosyaları

```
data/
├── participant_P001_20260127_143052.csv      # Deneme verileri
├── participant_P001_20260127_143052_events.csv   # Olay logları
└── participant_P001_20260127_143052_summary.json # Özet istatistikler

eyelink_data/
└── el20260127_143052.edf    # EyeLink ham veri dosyası
```

### 4.3 Örnek Veri Formatı

**CSV Çıktısı:**
```csv
participant_id,trial_id,trait,video_left,video_right,high_position,response,response_correct,response_time,confidence_rating
P001,1,Extraversion,84emxO86qa8.001.mp4,3zAyM2edy1g.004.mp4,left,left,True,2.34,4
P001,2,Agreeableness,MvWDky9ZaWU.000.mp4,oxw3nT9LSsg.000.mp4,right,right,True,1.87,5
```

---

## 5. Deney Akışı

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

## 6. Teknik Altyapı

### 6.1 Yazılım

| Bileşen | Sürüm |
|---------|-------|
| **Python** | 3.10.x |
| **PsychoPy** | 2025.2.4 |
| **OpenCV** | 4.x |
| **NumPy** | 1.x |
| **Pandas** | 2.x |
| **pylink** | SR Research |

### 6.2 Donanım Gereksinimleri

| Bileşen | Minimum | Önerilen |
|---------|---------|----------|
| **İşletim Sistemi** | Windows 10 / macOS 10.15 | Windows 10/11 |
| **RAM** | 8 GB | 16 GB |
| **Ekran** | 1920×1080 | 1920×1080 @ 60Hz+ |
| **Göz İzleyici** | EyeLink 1000 Plus | EyeLink 1000 Plus |

### 6.3 Proje Dosyaları

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

## 9. Onay ve Bilgilendirme Düzenlemeleri

### 9.1 Katılımcı Onay Formu (Consent Form)

Deney başlamadan önce, katılımcılara ekranda aşağıdaki bilgilendirilmiş onam formu gösterilir. Katılımcılar "I Agree - Start Study" butonuna tıklayarak onay verdikten sonra deney başlar:

> **INFORMED CONSENT FORM**
>
> You are invited to participate in a research study on personality perception from face videos.
>
> Before you decide to participate, please read the following information carefully:
>
> • You must be at least 18 years old to participate in this study.
>
> • Your participation is completely voluntary. You may withdraw from the study at any time without any penalty or negative consequences.
>
> • All data will be collected and stored anonymously. No personally identifying information will be recorded.
>
> • The study will take approximately 15 minutes to complete.
>
> • You must not be currently enrolled in any course taught by Prof. Dr. Uğur Güdükbay.
>
> • During the study, you will view pairs of short, silent face videos displayed side-by-side on a screen while your eye movements are recorded using an EyeLink 1000 eye tracker. After viewing each pair, you will answer a personality-related comparison question and indicate your confidence in your response.
>
> • All data will be used solely for scientific research purposes.
>
> **Supervisor:** Prof. Dr. Uğur Güdükbay  
> Department of Computer Engineering  
> Bilkent University
>
> By clicking 'I Agree', you confirm that you have read and understood the above information, that you meet the eligibility criteria, and that you voluntarily agree to participate.
>
> **[I Agree - Start Study]** ← Yeşil buton

### 9.2 Etik İlkeler

| İlke | Uygulama |
|------|----------|
| **Gönüllü Katılım** | Katılımcılar istediği zaman ceza olmaksızın çalışmadan çekilebilir |
| **Yaş Kriteri** | Minimum 18 yaş |
| **Anonimlik** | Kişisel tanımlayıcı bilgi toplanmaz |
| **Veri Güvenliği** | Tüm veriler anonim olarak saklanır |
| **Bilimsel Kullanım** | Veriler yalnızca araştırma amaçlı kullanılır |
| **Ders Kısıtlaması** | Katılımcılar Prof. Dr. Uğur Güdükbay'dan ders almıyor olmalı |
| **Süre Bilgisi** | Yaklaşık 15 dakika |

### 9.3 Onay Ekranı Görseli

Deney yazılımı aşağıdaki ekranları içerir:

1. **Consent Form Ekranı** - Yukarıdaki bilgilendirilmiş onam metni ve "I Agree - Start Study" butonu
2. **Hoş Geldiniz Ekranı** - Çalışma hakkında genel bilgi ve danışman bilgisi
3. **Talimatlar Ekranı** - Görevin nasıl yapılacağına dair detaylı açıklama
4. **Teşekkür Ekranı** - Çalışma sonunda gösterilen özet ve teşekkür

---

## 10. İletişim

**Proje Danışmanı:**  
Prof. Dr. Uğur Güdükbay  
Bilkent Üniversitesi  
Bilgisayar Mühendisliği Bölümü

---

*Bu doküman, Ocak 2026 tarihinde hazırlanmıştır.*
