Region of Interest (ROI) Detection dengan YOLO

Program deteksi objek real-time lewat webcam menggunakan YOLO (Ultralytics) dan OpenCV, dengan dua area poligon (ROI) untuk menentukan apakah sebuah objek berada di area yang diizinkan atau tidak.

Cara Kerja

Program menggambar dua area di atas video webcam:

Area	Warna garis	Fungsi
ACTIVE	Biru	Area utama. Objek yang titik tengahnya berada di sini ditampilkan lengkap dengan label dan nilai confidence.
GUARD	Kuning	Area pengaman (secara default seluruh frame). Objek yang berada di GUARD tetapi di luar ACTIVE diberi peringatan "Geser Ke tengah".

Penentuan posisi dilakukan dengan menghitung titik tengah (centroid) bounding box, lalu mengecek apakah titik tersebut berada di dalam poligon (algoritma point in polygon).

Struktur Project
demoroi/
├── webcam_roi.py       # Program utama
├── config.yaml         # Konfigurasi kamera, model, dan ROI
├── requirements.txt    # Daftar dependensi
└── README.md
Instalasi
Clone repo ini:
bash
   git clone https://github.com/Rebbla/Region-Of-Interest-ROI-.git
   cd Region-Of-Interest-ROI-
(Disarankan) Buat virtual environment:
bash
   python3 -m venv roi-venv
   source roi-venv/bin/activate      # Linux / macOS
   # roi-venv\Scripts\activate       # Windows
Install dependensi:
bash
   pip install -r requirements.txt
Siapkan file model YOLO (.pt) dan sesuaikan path-nya di config.yaml.
Konfigurasi

Semua pengaturan ada di config.yaml:

yaml
camera: 0                       # Index webcam (0 = kamera default)
model: "yolo26n.pt"             # Path ke file model YOLO
conf: 0.5                       # Threshold confidence (0.0 - 1.0)
imgsz: 640                      # Ukuran input gambar

# Titik poligon dalam koordinat relatif (0.0 - 1.0) terhadap lebar/tinggi frame
roi_active: [[0.25, 0.25], [0.75, 0.25], [0.75, 0.80], [0.25, 0.80]]
roi_guard:  [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]]

roi_show: true
save_output: true

Koordinat ROI memakai nilai relatif, jadi tetap sesuai di resolusi webcam berapa pun. Titik poligon bisa diubah atau ditambah untuk membuat bentuk area yang berbeda.

Menjalankan
bash
python webcam_roi.py

Kontrol keyboard:

q : keluar dari program
Dependensi
Ultralytics (YOLO)
OpenCV (opencv-python)
PyYAML
Catatan
Opsi save_output di config.yaml dan tombol s pada judul jendela belum diimplementasikan di kode saat ini.
File model (*.pt) tidak disertakan di repo, sehingga perlu disiapkan sendiri.
