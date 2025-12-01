# VTuber Menggunakan Python dan Mediapipe

## Deskripsi

Sistem ini merupakan implementasi avatar 2D yang dapat bergerak secara real-time mengikuti ekspresi wajah, gesture tangan, dan pose tubuh pengguna melalui input webcam. sistem ini mampu meniru ekspresi mikro (kedipan, gerakan mulut) dan gesture makro (gerakan tangan, pose tubuh), serta mendukung pergantian latar belakang secara dinamis.

Sistem dirancang untuk aplikasi interaktif seperti virtual meeting, edukasi, atau hiburan, dengan fokus pada responsivitas dan kemudahan integrasi aset visual.

---

## Fitur Utama

1. **Body Tracing & Visualisasi Avatar**
   - Deteksi dan pemetaan *landmark* wajah, tangan, dan pose tubuh menggunakan MediaPipe Holistic.
   - Avatar 2D mengikuti ekspresi wajah (kedipan, gerakan mulut, orientasi kepala).
   - Gesture tangan terdeteksi secara otomatis (Peace, Point, Thumbs Up, Open Hand).
   - Gerakan tubuh (angkat tangan kiri/kanan/keduanya) langsung tercermin pada avatar.

2. **Penggantian Background**
   - Mendukung pergantian latar belakang dengan transisi *crossfade* yang halus menggunakan Alpha Blending.
   - Pengelolaan aset background secara modular.
   - **Fitur tambahan:** Pengguna dapat mengganti background dengan menekan tombol `C` pada keyboard saat aplikasi berjalan.

3. **Animasi Idle (Pernapasan)**
   - Avatar melakukan animasi pernapasan alami saat pengguna diam.

4. **Komposisi Citra Presisi**
   - Layering cerdas antara background, body, dan head menggunakan kanal Alpha (RGBA).
   - Scaling otomatis aset visual sesuai rasio aspek.

---

## Teknologi yang Digunakan

| Pustaka         | Versi Minimum | Fungsi Utama                                      |
|-----------------|--------------|---------------------------------------------------|
| **Python**      | 3.12         | Bahasa pemrograman utama                          |
| **OpenCV**      | 4.12.0       | Akuisisi frame kamera, manipulasi citra, blending |
| **MediaPipe**   | 0.10.21      | Deteksi *landmark* wajah, tangan, pose tubuh      |
| **NumPy**       | 1.26.4       | Operasi array, perhitungan jarak Euclidean        |

---

## Arsitektur Project

Struktur kode modular untuk memudahkan pengembangan dan pemeliharaan:

```text
Project Root/
│
├── main.py                  # [Core] Loop utama, integrasi modul, rendering akhir
├── config.py                # [Config] Konstanta threshold, path aset
├── asset_loader.py          # [IO] Loader PNG, scaling otomatis
├── detection.py             # [Logic] Interpretasi landmark menjadi status logika
├── gesture_detection.py     # [Algorithm] Deteksi gesture tangan berbasis aturan
├── animation.py             # [Visual] Offset animasi sinus, transisi background
├── geometry_utils.py        # [Math] Fungsi Euclidean Distance, Aspect Ratio
├── image_utils.py           # [Processing] Resize & overlay PNG transparan
│
└── assets/                  # Direktori aset visual (PNG/JPG)
```

---

## Cara Menggunakan

1. **Instalasi Dependensi**
   ```bash
   pip install opencv-python mediapipe numpy
   ```

2. **Siapkan Aset Visual**
   - Tempatkan file PNG/JPG avatar dan background di folder `assets/`.

3. **Konfigurasi Threshold & Path**
   - Atur sensitivitas EAR/MAR dan path aset di `config.py` sesuai kebutuhan.

4. **Jalankan Program**
   ```bash
   python main.py
   ```

5. **Interaksi**
   - Pastikan webcam aktif.
   - Gerakkan wajah dan tangan di depan kamera, avatar akan mengikuti secara real-time.
   - Untuk mengganti background, tekan tombol `C` pada keyboard saat aplikasi berjalan.

---

## Catatan Tambahan

- Sistem mendukung penambahan aset visual baru dengan mudah.
- Threshold EAR/MAR dapat disesuaikan untuk berbagai kondisi pencahayaan dan bentuk wajah.
- Kode dapat dikembangkan lebih lanjut untuk integrasi dengan platform lain (Zoom, Discord, dll).

---


---
