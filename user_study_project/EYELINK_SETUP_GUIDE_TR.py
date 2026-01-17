"""
ADIM ADIM: EyeLink Entegrasyonu
================================

Bu dosya EyeLink eye tracker cihazınızı deney sistemine bağlamak için
adım adım talimatları içerir.
"""

# ==============================================================================
# ADIM 1: DONANIM KONTROL LISTESI
# ==============================================================================

"""
Başlamadan önce kontrol edin:

□ EyeLink Tracker (1000 Plus, Portable, vb.)
  - Güç kaynağı bağlı mı?
  - Host PC açık mı?
  
□ Ethernet Bağlantısı
  - Ethernet kablo bağlı mı?
  - Her iki bilgisayar da aynı ağda mı?
  
□ Ağ Yapılandırması
  - EyeLink Host IP: 100.1.1.1 (varsayılan)
  - Deney bilgisayarı IP: 100.1.1.2-254 aralığında
  - Güvenlik duvarı devre dışı (EyeLink ağında) mı?
"""

# ==============================================================================
# ADIM 2: YAZILIM KURULUMU (Windows)
# ==============================================================================

"""
2.1. SR Research'ten pylink indirin
     - Git: https://www.sr-research.com/support/
     - "EyeLink Developers Kit" indir
     - İşletim sisteminizi seçin (Windows, Mac, Linux)

2.2. pylink'i kurun
     
     Option A (Pip ile - Önerilen):
     --------------------------------
     cd Downloads
     pip install EyeLinkCoreGraphicsPyAPI.whl  # İndirilen dosya adı
     
     Option B (Setup.py ile):
     --------------------------------
     cd path/to/EyeLinkPython
     python setup.py install

2.3. Kurulumu doğrulayın
     
     python -c "import pylink; print(pylink.__version__)"
     
     Çıktı: 3.x.x.xxx (versiyon numarası)
     Başarı: ✓
"""

# ==============================================================================
# ADIM 3: AĞBAĞLANTISINI TEST ETME
# ==============================================================================

"""
3.1. Ping test yapın (EyeLink Host PC'ye)
     
     macOS/Linux:
       ping -c 4 100.1.1.1
       
     Windows (PowerShell):
       Test-NetConnection 100.1.1.1 -CommonTCPPort http
     
     Beklenen çıktı:
       - 4 paket gönderildi, 4 alındı
       - Yanıt süresi (ms) görülse
       
       Sorun varsa:
       ✗ Ethernet kablosu kontrol edin
       ✗ IP adresini kontrol edin
       ✗ Güvenlik duvarını kontrol edin

3.2. Network konfigürasyonunu kontrol edin
     
     macOS:
       - System Preferences > Network
       - Ethernet adaptörü seçin
       - IP adresinin 100.1.1.x aralığında olduğunu doğrulayın
       
     Windows:
       - Control Panel > Network and Sharing Center
       - Ethernet bağlantısını seçin
       - IPv4 özelliklerini kontrol edin
"""

# ==============================================================================
# ADIM 4: CONFIG.PY'DI GÜNCELLEME
# ==============================================================================

"""
4.1. config.py dosyasını açın

4.2. EyeLink ayarlarını değiştirin:

     # Adres: EyeLink Host PC'nin IP adresi
     EYELINK_IP = "100.1.1.1"
     
     # Örnekleme hızı (Hz)
     # 250 = Düşük (CPU az), 1000 = Yüksek (daha detaylı)
     EYELINK_SAMPLE_RATE = 1000
     
     # Kalibrasyon türü
     EYELINK_CALIBRATION_TYPE = "HV9"  # 9-nokta kalibrasyon
     
     # Veri klasörü
     EYELINK_DATA_FOLDER = "eyelink_data"

4.3. EyeLink'i etkinleştirin:
     
     EYELINK_ENABLED = True
     
     UYARI: pylink kurulana kadar False tutun!
"""

# ==============================================================================
# ADIM 5: PYLINK'İ ETKİN HALE GETIRME
# ==============================================================================

"""
5.1. eyelink_utils.py dosyasını açın

5.2. Satır 22'deki import'u açın:
     
     UYARI: Bu satırları bulun
     ---------
     # === UNCOMMENT WHEN PYLINK INSTALLED ===
     # try:
     #     import pylink
     #     PYLINK_AVAILABLE = True
     
     DEĞİŞTİR:
     ---------
     try:
         import pylink
         PYLINK_AVAILABLE = True
     except ImportError:
         PYLINK_AVAILABLE = False
         print("WARNING: pylink not found...")

5.3. PYLINK_AVAILABLE'ı True olarak ayarlayın:
     
     UYARI:
     PYLINK_AVAILABLE = False
     
     DEĞİŞTİR:
     PYLINK_AVAILABLE = True

5.4. Fonksiyon uygulamalarını açın:
     
     Tüm "# === UNCOMMENT WHEN PYLINK INSTALLED ===" 
     başlığı altındaki kodları açın
     
     Satırlar:
     - connect()      (~satır 80)
     - calibrate()    (~satır 130)
     - start_recording() (~satır 160)
     - stop_recording() (~satır 175)
     - send_message()  (~satır 190)
     - get_newest_sample() (~satır 215)

5.5. Dosyayı kaydedin
"""

# ==============================================================================
# ADIM 6: BASIT TEST
# ==============================================================================

"""
6.1. Test script'i oluşturun (test_eyelink.py):
     
     from eyelink_utils import EyeLinkManager
     import config
     
     # EyeLink manager oluştur
     el = EyeLinkManager(config)
     
     # Bağlan
     if el.connect():
         print("✓ Bağlandı!")
         
         # Kalibrasyon yap
         if el.calibrate():
             print("✓ Kalibrasyon tamamlandı!")
             
             # Kayıt başlat
             el.start_recording(trial_id=1)
             
             # Mesaj gönder
             el.send_message("TEST_MESSAGE")
             
             # Kayıt durdur
             el.stop_recording()
             
             # Bağlantı kes
             el.disconnect()
             print("✓ Test başarılı!")
     else:
         print("✗ Bağlanamadı")

6.2. Test'i çalıştırın:
     
     python test_eyelink.py
     
     Beklenen çıktı:
     - [EYELINK] Connecting to 100.1.1.1...
     - [EYELINK] Connected!
     - [EYELINK] Calibration complete!
     - [EYELINK] Recording started
     - ...
     - ✓ Test başarılı!

6.3. Sorun varsa:
     - IP adresini kontrol edin
     - EyeLink Host PC'nin açık olduğunu kontrol edin
     - Bağlantıyı test edin (ping)
"""

# ==============================================================================
# ADIM 7: MAIN_EXPERIMENT.PY İLE ENTEGRASYON
# ==============================================================================

"""
7.1. main_experiment.py dosyasında EyeLink zaten entegre!
     - setup_eyelink() fonksiyonu otomatik olarak çalışır
     - EYELINK_ENABLED = True ise bağlanacak
     - EYELINK_ENABLED = False ise simülasyon modunda çalışacak

7.2. Deney sırasında otomatik olarak şunlar yapılır:
     
     Trial başında:
     - eyelink.start_recording(trial_id)
     - eyelink.send_message("TRIAL_START")
     - eyelink.define_video_interest_areas()  # Bölgeler belirleme
     
     Video sırasında:
     - eyelink.send_message("VIDEO_ONSET")
     - eyelink.send_message("VIDEO_OFFSET")
     
     Cevap sırasında:
     - eyelink.send_message("RESPONSE")
     
     Trial sonunda:
     - eyelink.stop_recording()

7.3. Verileri manuel olarak erişme:
     
     from eyelink_utils import EyeLinkManager
     
     el = EyeLinkManager(config)
     el.connect()
     el.calibrate()
     el.start_recording()
     
     # Gaze verisi al
     for i in range(100):
         sample = el.get_newest_sample()
         print(f"Gaze: {sample['gaze_x']}, {sample['gaze_y']}")
     
     el.stop_recording()
     el.disconnect()
"""

# ==============================================================================
# ADIM 8: EDF VERİLERİNİ ANALYSIS ETME
# ==============================================================================

"""
8.1. EDF dosyaları şurada kaydedilir:
     
     eyelink_data/el[timestamp].edf
     
     Örnek: eyelink_data/el150900.edf

8.2. Verileri görselleştirme:
     
     SR Research EyeLink Data Viewer'ı kullanın
     (EyeLink yazılım paketinde dahil)
     
     - Heat maps
     - Gaze paths
     - Fixation analysis
     - Saccade analysis

8.3. Python ile analiz:
     
     Python paketleri:
     - eyelinkcore
     - pygazetracker
     - pandas + numpy
     
     Örnek:
     
     import pandas as pd
     import csv
     
     # EDF'i CSV'ye dönüştür
     # (EyeLink Data Viewer kullanarak)
     
     df = pd.read_csv('eyelink_data_converted.csv')
     
     # Sabit noktaları bul (fixations)
     fixations = df[df['event'] == 'FIXATION']
     
     # Göz hareketlerini çiz
     import matplotlib.pyplot as plt
     plt.scatter(df['gaze_x'], df['gaze_y'], alpha=0.5)
     plt.title('Gaze Pattern')
     plt.show()
"""

# ==============================================================================
# ADIM 9: TROUBLESHOOTING
# ==============================================================================

"""
SORUNA:  "ModuleNotFoundError: No module named 'pylink'"
ÇÖZÜM:
  1. pylink kurulu mu? -> pip list | grep pylink
  2. Kurulu değilse: pip install EyeLinkCoreGraphicsPyAPI.whl
  3. Doğru yolu mü? -> python -c "import sys; print(sys.path)"

SORUNA:  "Failed to connect to EyeLink"
ÇÖZÜM:
  1. Ping test edin: ping 100.1.1.1
  2. EyeLink Host PC'nin açık olduğunu kontrol edin
  3. IP adresini kontrol edin (config.py)
  4. Ethernet kablosunu kontrol edin
  5. Güvenlik duvarını geçici olarak devre dışı bırakın

SORUNA:  "Calibration failed"
ÇÖZÜM:
  1. Odada yeterli aydınlatma var mı?
  2. Katılımcı ekrana 60cm uzaklıkta mı?
  3. Kalibrasyonu tekrar deneyin
  4. Bakım: Kamera lensini temizleyin

SORUNA:  "EDF file transfer failed"
ÇÖZÜM:
  1. EyeLink Host'ta disk alanı var mı?
  2. Dosya adı 8 karakter altında mı?
  3. Ağ bağlantısı stabil mi?
  4. Daha kısa Ethernet kablosu deneyin

SORUNA:  "Recording didn't start"
ÇÖZÜM:
  1. Kalibrasyonu başarıyla tamamladınız mı?
  2. EDF dosyası açılmış mı?
  3. Ağ gecikmesi sorunu mu?
  4. startRecording komutu gönderildi mi?
"""

# ==============================================================================
# ADIM 10: REFERANS - KOD ÖRNEKLERİ
# ==============================================================================

"""
BAĞLANTI ÖRNEĞI:

    from eyelink_utils import EyeLinkManager
    import config
    
    el = EyeLinkManager(config)
    
    # Bağlan
    el.connect()
    
    # Kalibre et
    el.calibrate()
    
    # İçin çalış
    el.start_recording(trial_id=1)
    el.send_message("TRIAL_START 001")
    # ... deney kodu ...
    el.send_message("TRIAL_END 001")
    el.stop_recording()
    
    # Kapat
    el.disconnect()

FAIZ ALANLARINI AYARLAMA:

    # Video bölgelerini tanımla
    left_pos = (-200, 0)    # Sol video pozisyonu
    right_pos = (200, 0)    # Sağ video pozisyonu
    video_w = 640
    video_h = 480
    
    el.define_video_interest_areas(left_pos, right_pos, video_w, video_h)

GAZE VERİSİ ALMA:

    import time
    
    el.start_recording()
    
    for i in range(100):  # 100 örnek
        sample = el.get_newest_sample()
        print(f"X={sample['gaze_x']:.1f}, Y={sample['gaze_y']:.1f}")
        time.sleep(0.01)
    
    el.stop_recording()
"""

# ==============================================================================
# SONRAKI ADIMLAR
# ==============================================================================

"""
1. ✓ Donanımı kontrol edin
2. ✓ pylink kurun
3. ✓ Ağ bağlantısını test edin
4. ✓ config.py'ı güncelleyin
5. ✓ eyelink_utils.py'ı etkinleştirin
6. ✓ Test script'ini çalıştırın
7. ✓ main_experiment.py'ı çalıştırın
8. ✓ EDF verilerini analiz edin

Sorularınız varsa:
- EyeLink: https://www.sr-research.com/support/
- PsychoPy: https://www.psychopy.org/
- Bu proje: [Proje klasöründeki README.md]
"""

print(__doc__)
