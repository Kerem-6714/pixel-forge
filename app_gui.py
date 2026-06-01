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

# Profesyonel CSS Dokunuşları (Karanlık modern tema, butonlar ve galeri kartları)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stTextArea textarea { background-color: #161b22; color: #c9d1d9; border: 1px solid #30363d; border-radius: 8px; }
    .stButton>button { background: linear-gradient(45deg, #4f46e5, #06b6d4); color: white; border: none; padding: 12px 24px; border-radius: 8px; font-weight: bold; transition: all 0.3s ease; }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(79, 70, 229, 0.4); }
    h1 { color: #f0f6fc; font-family: 'Inter', sans-serif; font-weight: 800; }
    /* Galeri kutusu tasarımı */
    .galeri-kutu { border: 1px solid #30363d; border-radius: 8px; padding: 5px; background-color: #161b22; }
    </style>
""", unsafe_allow_html=True)

# --- GALERİ HAFIZASI (SESSION STATE) BAŞLATMA ---
# Tarayıcı sekmesi açık kaldığı sürece üretilen resimleri burada saklayacağız
if "gorsel_gecmisi" not in st.session_state:
    st.session_state.gorsel_gecmisi = []  # Boş bir liste olarak başlatıyoruz

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

# Düzen: Sol Panel (Ayarlar) | Sağ Panel (Üretim ve Ana Ekran)
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
            if prompt_geliştirici_aktif:
                glistirilmis_prompt = user_prompt
            else:
                glistirilmis_prompt = user_prompt + STILLER[secilen_stil]
            
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
                        resim_baytlari = response.content
                        gorsel = Image.open(io.BytesIO(resim_baytlari))
                        
                        # --- YENİ: Üretilen resmi galeri hafızasına (en başa) ekliyoruz ---
                        st.session_state.gorsel_gecmisi.insert(0, {
                            "resim": gorsel,
                            "prompt": user_prompt,
                            "bayt": resim_baytlari
                        })
                        
                        # En son üretilen resmi ekranda göster
                        st.image(gorsel, use_container_width=True, caption=f"Son Sonuç: {user_prompt}")
                        
                        st.download_button(
                            label="💾 Ustalık Eserini İndir",
                            data=resim_baytlari,
                            file_name="pixel_forge_art.png",
                            mime="image/png",
                            use_container_width=True
                        )
                    else:
                        st.error("Motor üretim yaparken bir sorunla karşılaştı.")
                except Exception as e:
                    st.error(f"Bağlantı Hatası: Arka plan motorunun (main.py) açık olduğundan emin olun. Hata: {e}")
    else:
        # Eğer henüz yeni resim üretilmediyse ama geçmişte resimler varsa, en sonuncuyu ekranda tut
        if st.session_state.gorsel_gecmisi:
            st.image(st.session_state.gorsel_gecmisi[0]["resim"], use_container_width=True, caption="Son Üretilen Görsel")
        else:
            st.info("Sol tarafa prompt girip 'Sanatı Canlandır' butonuna bastığınızda, şaheseriniz burada belirecektir.")

# --- YENİ BÖLÜM: ALT TARAFTAKİ PREMIUM GALERİ ŞERİDİ ---
if st.session_state.gorsel_gecmisi:
    st.markdown("---")
    st.markdown("### 📸 Bu Oturumdaki Sanatlarınız (Geçmiş Şeridi)")
    
    # Yan yana en fazla 4 adet küçük kart gösterecek şekilde kolonlar oluşturuyoruz
    # Listeden en fazla son 4 resmi çekiyoruz
    gosterilecek_adet = min(4, len(st.session_state.gorsel_gecmisi))
    kolonlar = st.columns(4)
    
    for sira in range(gosterilecek_adet):
        veri = st.session_state.gorsel_gecmisi[sira]
        with kolonlar[sira]:
            # Şık bir kutu efekti içinde resmi ve altına kısa promptunu yazıyoruz
            st.image(veri["resim"], use_container_width=True)
            # Prompt çok uzunsa kırpıp şık gösterelim
            kisa_prompt = veri["prompt"][:35] + "..." if len(veri["prompt"]) > 35 else veri["prompt"]
            st.caption(f"📝 {kisa_prompt}")
            
            # Galeri içinden de indirmek isteyenler için küçük bir buton
            st.download_button(
                label="📥 İndir",
                data=veri["bayt"],
                file_name=f"forge_gallery_{sira}.png",
                mime="image/png",
                key=f"galeri_down_{sira}", # Her butonun benzersiz bir anahtarı olmalı
                use_container_width=True
            )