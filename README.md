# VTuber Menggunakan Python dan Mediapipe

## Deskripsi

Sistem ini merupakan implementasi avatar 2D yang dapat bergerak secara real time mengikuti ekspresi wajah, gesture tangan, dan pose tubuh pengguna melalui input webcam. Melalui MediaPipe, sistem mampu membaca ekspresi mikro seperti kedipan dan gerakan mulut, serta gesture makro seperti pose tangan dan pergerakan tubuh secara keseluruhan. Selain itu, sistem juga menyediakan fitur penggantian latar belakang secara dinamis agar pengalaman interaksi menjadi lebih imersif.

Sistem ini dirancang untuk keperluan interaktif seperti pertemuan virtual, pendidikan, maupun hiburan, dengan fokus utama pada responsivitas, stabilitas, dan kemudahan integrasi dengan aset visual avatar.

---

## Fitur Utama

1. **Body Tracing & Visualisasi Avatar**
   - Mendukung deteksi lengkap wajah, tangan, dan pose tubuh menggunakan MediaPipe.
   - Avatar 2D menyesuaikan ekspresi wajah pengguna, termasuk kedipan dan gerakan mulut.
   - Gesture tangan seperti peace, pointing, thumbs up, dan open hand dikenali secara otomatis.
   - Gerakan tubuh, seperti mengangkat tangan kiri, kanan, atau keduanya, langsung tercermin pada avatar.

2. **Penggantian Background**
   - Mendukung pergantian latar belakang dengan transisi *crossfade* yang halus menggunakan Alpha Blending.
   - Aset background dikelola secara modular dan mudah diganti.
   - **Fitur tambahan:** Pengguna dapat mengganti background dengan menekan tombol `C` pada keyboard saat aplikasi berjalan.

3. **Animasi Idle (Pernapasan)**
   - Avatar memiliki animasi pernapasan halus saat pengguna tidak melakukan gerakan tertentu, membuat tampilan lebih hidup dan natural.

4. **Komposisi Citra Presisi**
   - Pengaturan layer antara background, tubuh, dan kepala dilakukan dengan memanfaatkan kanal alpha (RGBA).
   - Aset visual diskalakan otomatis sesuai rasio aspek dan posisi landmark.

---

## Teknologi yang Digunakan

| Pustaka         | Versi Minimum | Fungsi Utama                                        |
|-----------------|--------------|---------------------------------------------------   |
| **Python**      | 3.12         | Bahasa pemrograman utama                             |
| **OpenCV**      | 4.12.0       | Pengambilan frame kamera, manipulasi citra, blending |
| **MediaPipe**   | 0.10.21      | Deteksi landmark wajah, tangan, dan pose tubuh       |
| **NumPy**       | 1.26.4       | Operasi array dan perhitungan jarak Euclidean        |

---

## Arsitektur Project

Struktur dibuat modular untuk memudahkan pengembangann kedepannya:

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
   - Masukkan file PNG atau JPG untuk avatar dan background ke folder `assets/`.

3. **Konfigurasi Sistem**
   - Atur sensitivitas EAR/MAR dan path aset di `config.py` sesuai kebutuhan.

4. **Jalankan Program**
   ```bash
   python main.py
   ```

5. **Interaksi**
   - Pastikan webcam aktif.
   - Gerakkan wajah dan tangan di depan kamera, avatar akan mengikuti secara real-time.
   - Untuk mengganti background, tekan tombol `C` pada keyboard saat aplikasi berjalan
