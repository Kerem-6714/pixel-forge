# 🎨 PixelForge - Yerel AI Sanat Stüdyosu

Bu proje, donanım kısıtlamalarını (6 GB VRAM) akıllı yazılım optimizasyonlarıyla aşan, tamamen yerel bilgisayarınızda çalışan, kredisiz ve sınırsız bir yeni nesil yapay zeka görsel üretim platformudur.

## 🧠 Özellikler
* **Sınırsız & Ücretsiz:** Herhangi bir API anahtarına veya aboneliğe ihtiyaç duymaz.
* **Magic Enhancer (Llama3):** Basit kelimelerinizi, yerel Llama3 modelini kullanarak Stable Diffusion için profesyonel sanat promptlarına dönüştürür.
* **VRAM Dostu:** Gelişmiş bellek boşaltma (`sequential_cpu_offload`) ve çıkarım modu (`inference_mode`) optimizasyonları içerir.
* **Modern Mimari:** FastAPI backend ve Streamlit frontend mikroservis yapısı.

## 🛠️ Kurulum
1. `main.py` dosyasını çalıştırarak backend motorunu başlatın.
2. `streamlit run app_gui.py` ile arayüze bağlanın.
