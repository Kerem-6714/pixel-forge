import torch
from diffusers import StableDiffusionPipeline
import time

print("🔄 Yerel yapay zeka motoru hazırlanıyor...")
start_time = time.time()

# Bilgisayarında NVIDIA ekran kartı (CUDA) varsa onu, yoksa işlemciyi (CPU) seçer
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"💻 Kullanılan Donanım: {device.upper()}")

# Dünya çapında en popüler açık kaynaklı temel model: Stable Diffusion 1.5
model_id = "runwayml/stable-diffusion-v1-5"

# Modeli yüklüyoruz. Bilgisayarın durumuna göre hafıza yönetimini optimize ediyoruz.
if device == "cuda":
    # GPU varsa daha az VRAM harcaması için float16 (yarı hassasiyet) kullanıyoruz
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
else:
    # CPU varsa standart float32 kullanıyoruz
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float32)

pipe.to(device)
print(f"✓ Model {time.time() - start_time:.2f} saniyede hafızaya yüklendi!")

# --- GÖRSEL ÜRETİM ALANI ---
print("\n🎨 İlk görsel üretimi başlatılıyor, lütfen bekleyin...")
prompt = "A majestic cinematic shot of a futuristic neon city, cyberpunk style, highly detailed, 8k resolution"
image_start = time.time()

# Bilgisayarı yormamak için adım sayısını (steps) 15'te tutuyoruz (Normalde 30-50 arasıdır)
output = pipe(prompt=prompt, num_inference_steps=15).images[0]

# Üretilen resmi klasöre kaydet
output.save("ilk_cyberpunk_sehir.png")

print(f"\n🎉 BAŞARILI! Görsel {time.time() - image_start:.2f} saniyede üretildi.")
print("📁 Klasörüne bak: 'ilk_cyberpunk_sehir.png' dosyası oluşturuldu!")