# Modul 2: Data Visualization - Spatial Weather Platform

> **Praktikum Sains Data** | Dual-Framework Real-Time Weather Dashboard

Platform visualisasi data cuaca real-time menggunakan **dua framework**: **Dash Plotly** (System Alpha) dan **Taipy** (System Beta), dengan arsitektur *Shared Brain* yang terpusat.

---

## 🏗️ Arsitektur Sistem

```
Modul_2app/
├── modul2_weather_ops/
│   ├── configs/              # Konfigurasi YAML (koordinat kota, API, interval)
│   ├── data_pipeline/        # THE SHARED BRAIN
│   │   ├── schemas.py        # Validasi data Pydantic  
│   │   ├── weather_client.py # Bulk API fetch + Atomic JSON Cache
│   │   └── geo_transformers.py # DataFrame & Plotly Mapbox Generator
│   ├── frontend_dash/        # SYSTEM ALPHA - Port 8050
│   │   ├── app.py
│   │   ├── layouts/
│   │   ├── callbacks/
│   │   └── assets/           # White Glassmorphism CSS
│   └── frontend_taipy/       # SYSTEM BETA - Port 5001
│       ├── main.py
│       ├── state_manager.py  # Background Thread polling
│       └── pages/
├── modul2_assignments/
│   ├── 5a_diabetes/          # Tugas 5A - Dash Diabetes Dashboard
│   ├── 5b_pollution/         # Tugas 5B - Taipy Real-time Pollution
│   └── 6e_dash_news/         # Tugas 6E - Dash News Network
└── README.md
```

---

## ✨ Fitur Utama

| Fitur | Detail |
|---|---|
| 🗺️ **Peta Interaktif** | Plotly Mapbox dengan zoom, pan, dan hover tooltip |
| ⚡ **Bulk API Query** | 1 HTTP request untuk semua 8 kota (vs 8 request serial) |
| 💾 **Atomic JSON Cache** | Zero-load time: data tampil instan dari cache lokal |
| 🔄 **Real-time Update** | Polling otomatis setiap 5 menit |
| 🛡️ **Fault Tolerant** | Graceful fallback ke cache jika API timeout |
| 🎨 **White Glassmorphism** | UI premium dengan efek blur & transparent |
| 🌐 **Dual Framework** | Dash (8050) + Taipy (5001) dari sumber data yang sama |

---

## 🚀 Cara Menjalankan

### Prasyarat
```bash
Python 3.10+
pip
```

### 1. Install Dependensi

```bash
# Dependensi inti
pip install -r modul2_weather_ops/requirements-core.txt

# Untuk System Alpha (Dash)
pip install -r modul2_weather_ops/requirements-dash.txt

# Untuk System Beta (Taipy)
pip install -r modul2_weather_ops/requirements-taipy.txt
```

### 2. Jalankan System Alpha - Dash (Port 8050)

```bash
cd modul2_weather_ops
python -m frontend_dash.app
```

Buka: **http://127.0.0.1:8050**

### 3. Jalankan System Beta - Taipy (Port 5001)

```bash
cd modul2_weather_ops
python -m frontend_taipy.main
```

Buka: **http://127.0.0.1:5001**

---

## 📚 Tugas Pendamping

### 5A - Dashboard Diabetes Sederhana (Port 8052)
```bash
python modul2_assignments/5a_diabetes/app.py
```

### 5B - Pemantau Polusi Real-time Taipy (Port 5002)
```bash
# Terminal 1
cd modul2_assignments/5b_pollution && python src/receiver.py

# Terminal 2 (baru)
cd modul2_assignments/5b_pollution && python src/sender.py
```

### 6E - Dash News Network (Port 8053)
```bash
cd modul2_assignments/6e_dash_news && python app.py
```

---

## 🌤️ Data Cuaca

Menggunakan **Open-Meteo API** (gratis, tanpa API Key) dengan 8 kota Indonesia:

| Kota | Koordinat |
|---|---|
| Jakarta | -6.2088, 106.8456 |
| Surabaya | -7.2504, 112.7688 |
| Bandung | -6.9175, 107.6191 |
| Medan | 3.5952, 98.6722 |
| Balikpapan | -1.2654, 116.8312 |
| Makassar | -5.1477, 119.4327 |
| Yogyakarta | -7.7956, 110.3695 |
| Denpasar | -8.6705, 115.2126 |

---

## 🛠️ Teknologi

- **Python 3.10+**
- **Dash Plotly** — Framework dashboard reaktif
- **Taipy** — Framework aplikasi data-driven
- **Plotly** — Visualisasi interaktif & Mapbox
- **Pydantic** — Validasi skema data
- **Open-Meteo API** — Sumber data cuaca real-time

---

*Dibuat untuk Modul 2 Praktikum Sains Data*
