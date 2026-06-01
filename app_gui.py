import streamlit as st
import requests
from PIL import Image
import io

# Sayfa Genişlik ve Tema Ayarları
st.set_page_config(
    page_title="PixelForge - Free AI Generation",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Profesyonel CSS Dokunuşları (Karanlık modern tema ve buton tasarımları)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stTextArea textarea { background-color: #161b22; color: #c9d1d9; border: 1px solid #30363d; border-radius: 8px; }
    .stButton>button { background: linear-gradient(45deg, #4f46e5, #06b6d4); color: white; border: none; padding: 12px 24px; border-radius: 8px; font-weight: bold; transition: all 0.3s ease; }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(79, 70, 229, 0.4); }
    h1 { color: #f0f6fc; font-family: 'Inter', sans-serif; font-weight: 800; }
    </style>
""", unsafe_allow_html=True)

# Başlık Bölümü (Hero Section)
st.title("✨ PixelForge")
st.caption("Sınırsız, Kredisiz ve Tamamen Yerel Yeni Nesil Yapay Zeka Görsel Üretim Platformu")
st.markdown("---")

# Stil Havuzu (Prompt Sihirbazı)
STILLER = {
    "🌌 Sinematik (Cinematic)": ", cinematic shot, 8k resolution, dramatic lighting, highly detailed, masterpiece, photorealistic",
    "🎨 Dijital Sanat (Digital Art)": ", digital art, vibrant colors, concept art, trending on artstation, sharp focus",
    "🇯🇵 Anime Tarzı": ", anime style, studio ghibli, makoto shinkai, colorful, beautiful aesthetic",
    "✏️ Kara Kalem Eskiz": ", pencil sketch, hand drawn, monochrome, highly detailed graphite, artistic",
    "🗿 Gerçekçi Heykel/Mermer": ", marble statue, classical sculpture, museum quality, dramatic side lighting"
}

# Düzen: Sol Panel (Ayarlar) | Sağ Panel (Üretim ve Galeri)
with st.sidebar:
    st.image("https://img.icons8.com/nolan/96/artificial-intelligence.png", width=80)
    st.header("Stüdyo Kontrolleri")
    
    # Stil seçimi
    secilen_stil = st.selectbox("🎭 Görsel Stili", list(STILLER.keys()))
    
    # Kalite adımı
    adim_sayisi = st.slider("⚡ Üretim Hızı / Kalitesi", min_value=10, max_value=30, value=20, help="20 adım optimal kalite ve hız dengesidir.")
    
    # Yapay Zeka Asistanı Düğmesi
    st.markdown("---")
    st.markdown("### 🧠 Yapay Zeka Asistanı")
    prompt_geliştirici_aktif = st.toggle(
        "Promptu Otomatik Geliştir (Magic Enhancer)", 
        value=False,
        help="Açık olduğunda, bilgisayarınızdaki Llama3 basit kelimelerinizi profesyonel sanat promptlarına dönüştürür."
    )
    
    st.markdown("---")
    st.markdown("### 🚫 Gelişmiş Filtre")
    negatif_input = st.text_input("Görselde ne olmasın? (Negative Prompt)", placeholder="Örn: sun, red clothes, text")
    
    st.markdown("---")
    st.info("🔓 **Token Limiti Yok:** Bu platform yerel donanımınızı kullandığı için tamamen ücretsizdir. İstediğiniz kadar üretebilirsiniz.")

# Ana Üretim Alanı
sol_kolon, sag_kolon = st.columns([1.2, 1])

with sol_kolon:
    st.markdown("### 🧠 Ne Hayal Ediyorsunuz?")
    user_prompt = st.text_area(
        "Hayal gücünüzü kelimelere dökün (İngilizce daha iyi sonuç verir):",
        placeholder="A majestic neon cyber-punk owl watching over a futuristic Tokyo city...",
        height=120
    )
    
    uret_butonu = st.button("Sanatı Canlandır 🚀", use_container_width=True)

with sag_kolon:
    st.markdown("### 🖼️ Çıktı Ekranı")
    
    if uret_butonu:
        if not user_prompt.strip():
            st.warning("Lütfen bir prompt senaryosu yazın!")
        else:
            # --- AKILLI PROMPT KONTROLÜ BURADA BAŞLIYOR ---
            # Eğer asistan aktifse hazır stilleri ekleme, sadece kullanıcının yazdığını Llama'ya gönder.
            # Asistan kapalıysa hazır stilleri arkasına ekle.
            if prompt_geliştirici_aktif:
                glistirilmis_prompt = user_prompt
            else:
                glistirilmis_prompt = user_prompt + STILLER[secilen_stil]
            # --- AKILLI PROMPT KONTROLÜ BURADA BİTTİ ---
            
            with st.spinner("Pikseller yerel yapay zeka tarafından dokunuyor..."):
                try:
                    payload = {
                        "prompt": glistirilmis_prompt,
                        "negative_prompt": negatif_input,
                        "adim_sayisi": adim_sayisi
                    }
                    
                    backend_url = "http://localhost:8000/v1/generate"
                    response = requests.post(
                        backend_url, 
                        json=payload, 
                        params={"enhance_prompt": prompt_geliştirici_aktif}
                    )
                    
                    if response.status_code == 200:
                        resim_baytlari = io.BytesIO(response.content)
                        gorsel = Image.open(resim_baytlari)
                        
                        st.image(gorsel, use_container_width=True, caption="LuminaStudio tarafından üretildi.")
                        
                        st.download_button(
                            label="💾 Ustalık Eserini İndir",
                            data=response.content,
                            file_name="lumina_art.png",
                            mime="image/png",
                            use_container_width=True
                        )
                    else:
                        st.error("Motor üretim yaparken bir sorunla karşılaştı.")
                except Exception as e:
                    st.error(f"Bağlantı Hatası: Arka plan motorunun (main.py) açık olduğundan emin olun. Hata: {e}")
    else:
        st.info("Sol tarafa prompt girip 'Sanatı Canlandır' butonuna bastığınızda, şaheseriniz burada belirecektir.")