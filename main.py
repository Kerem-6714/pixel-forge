from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
import torch
from diffusers import StableDiffusionPipeline
import io
import os
import requests  # Ollama API ile konuşabilmek için ekledik

app = FastAPI(
    title="⚡ Premium Resim Motoru", 
    description="Llama3 ve Stable Diffusion destekli gelişmiş yerel motor",
    version="1.1.0"
)

# --- MODELİ OPTİMİZE HAFIZAYA ALMA ---
device = "cuda" if torch.cuda.is_available() else "cpu"
model_id = "runwayml/stable-diffusion-v1-5"

print(f"🔄 API Başlatılıyor... Model {device.upper()} için ultra-optimize yükleniyor...")

if device == "cuda":
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    pipe.to(device)
    os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
    pipe.enable_sequential_cpu_offload()
    pipe.enable_attention_slicing()
else:
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float32)
    pipe.to(device)

print("✓ Ultra-optimize model başarıyla yüklendi!")


# --- OLLAMA PROMPT GELİŞTİRİCİ FONKSİYONU ---
def llama_ile_prompt_buyut(basit_prompt: str) -> str:
    try:
        ollama_url = "http://localhost:11434/api/generate"
        
        # Llama3'e bir yapay zeka sanat yönetmeni gibi davranmasını söylüyoruz
        # Llama3'ün SD 1.5'e uygun, somut ve abartısız kelimeler üretmesini sağlıyoruz
        sistem_talimati = (
            "You are an expert prompt engineer for Stable Diffusion 1.5. "
            "Expand the user's concept into a concise, concrete description using clear visual keywords, "
            "lighting style, and camera shot type. Do NOT use abstract, poetic, or overly complex sentences. "
            "Keep it under 30 words total. Output ONLY the raw prompt. No commentary, no introductions."
        )
        
        payload = {
            "model": "llama3", 
            "prompt": f"{sistem_talimati}\n\nUser simple concept: {basit_prompt}\nExpanded Art Prompt:",
            "stream": False
        }
        
        response = requests.post(ollama_url, json=payload, timeout=10)
        if response.status_code == 200:
            gelen_metin = response.json().get("response", basit_prompt)
            print(f"\n🤖 Llama3 Promptu Geliştirdi: {gelen_metin}\n")
            return gelen_metin.strip()
    except Exception as e:
        print(f"⚠️ Ollama bağlantı hatası (Sistem normal promptu kullanacak): {e}")
    
    return basit_prompt


# --- İSTEK ŞABLONU ---
class ResimIstege(BaseModel):
    prompt: str
    negative_prompt: str = ""
    adim_sayisi: int = 20


# --- ENDPOINT (RESİM ÜRETİM NOKTASI) ---
@app.post("/v1/generate")
async def resim_uret(istek: ResimIstege, enhance_prompt: bool = False):
    if not istek.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt boş olamaz!")
        
    try:
        # Eğer kullanıcı arayüzden "Promptu Otomatik Geliştir" seçeneğini açtıysa Llama3'ü devreye sokuyoruz
        isleme_alinacak_prompt = istek.prompt
        if enhance_prompt:
            print(f"🧠 Basit prompt Llama3'e gönderiliyor: '{istek.prompt}'")
            isleme_alinacak_prompt = llama_ile_prompt_buyut(istek.prompt)
        else:
            print(f"🎨 Standart Üretim Başladı: '{istek.prompt}'")
        
        # Profesyonel çıktılar için varsayılan bir negatif prompt havuzu
        varsayilan_negatif = "blurry, bad anatomy, extra limbs, poorly drawn face, poorly drawn hands, mutation, deformed, blurry, bad proportions, mutilated, cropped, worst quality, low quality"
        tam_negatif = f"{varsayilan_negatif}, {istek.negative_prompt}" if istek.negative_prompt else varsayilan_negatif

        # Üretim esnasında gradyan hesaplamalarını kapatarak VRAM şişmesini önlüyoruz
        with torch.inference_mode():
            output = pipe(
                prompt=isleme_alinacak_prompt, 
                negative_prompt=tam_negatif,
                num_inference_steps=istek.adim_sayisi,
                guidance_scale=7.5
            ).images[0]
        
        buffer = io.BytesIO()
        output.save(buffer, format="PNG")
        resim_baytlari = buffer.getvalue()
        
        if device == "cuda":
            torch.cuda.empty_cache()
            
        return Response(content=resim_baytlari, media_type="image/png")
        
    except Exception as e:
        print(f"💥 Hata oluştu: {str(e)}")
        if device == "cuda":
            torch.cuda.empty_cache()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)