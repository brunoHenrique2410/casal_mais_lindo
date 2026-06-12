import streamlit as st
import base64
import os
import random

st.set_page_config(
    page_title="Gabriel & Rilary ❤️",
    page_icon="❤️",
    layout="wide"
)

# =========================
# CONFIGURAÇÕES
# =========================

NOME_1 = "Gabriel Ramos"
NOME_2 = "Rilary Escobar"
MUSICA = "musica.mp3"
PASTA_FOTOS = "fotos"

# =========================
# CSS
# =========================

st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #1b0f1f, #3b1238, #651d4b);
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #1b0f1f, #3b1238, #651d4b);
    color: white;
}

[data-testid="stSidebar"] {
    background: #160b19;
}

.titulo {
    text-align: center;
    font-size: 55px;
    font-weight: bold;
    color: #ffb6d9;
    text-shadow: 0 0 15px #ff4fa3;
}

.subtitulo {
    text-align: center;
    font-size: 24px;
    color: #ffe3f1;
}

.card {
    background: rgba(255,255,255,0.10);
    padding: 25px;
    border-radius: 25px;
    text-align: center;
    box-shadow: 0 0 20px rgba(255, 105, 180, 0.35);
    margin: 15px 0;
}

.foto-galeria img {
    border-radius: 20px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# FUNÇÕES
# =========================

def carregar_fotos():
    if not os.path.exists(PASTA_FOTOS):
        os.makedirs(PASTA_FOTOS)

    fotos = []
    for arquivo in os.listdir(PASTA_FOTOS):
        if arquivo.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
            fotos.append(os.path.join(PASTA_FOTOS, arquivo))

    return fotos


def tocar_musica():
    if os.path.exists(MUSICA):
        with open(MUSICA, "rb") as f:
            audio = f.read()

        b64 = base64.b64encode(audio).decode()

        st.markdown(f"""
        <audio autoplay loop>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """, unsafe_allow_html=True)
    else:
        st.warning("Coloque o arquivo musica.mp3 na pasta do projeto.")


def slideshow_html(fotos):
    imagens_base64 = []

    for foto in fotos:
        with open(foto, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            imagens_base64.append(f"data:image/jpeg;base64,{b64}")

    slides = ""
    for i, img in enumerate(imagens_base64):
        slides += f"""
        <div class="slide fade">
            <img src="{img}">
        </div>
        """

    html = f"""
    <style>
    .slideshow-container {{
        max-width: 650px;
        height: 500px;
        position: relative;
        margin: auto;
        border-radius: 30px;
        overflow: hidden;
        box-shadow: 0 0 35px rgba(255, 105, 180, 0.7);
    }}

    .slide {{
        display: none;
        width: 100%;
        height: 100%;
    }}

    .slide img {{
        width: 100%;
        height: 100%;
        object-fit: cover;
    }}

    .fade {{
        animation: fadeEffect 2s;
    }}

    @keyframes fadeEffect {{
        from {{opacity: .3}}
        to {{opacity: 1}}
    }}
    </style>

    <div class="slideshow-container">
        {slides}
    </div>

    <script>
    let slideIndex = 0;
    showSlides();

    function showSlides() {{
        let slides = document.getElementsByClassName("slide");
        for (let i = 0; i < slides.length; i++) {{
            slides[i].style.display = "none";
        }}
        slideIndex++;
        if (slideIndex > slides.length) {{slideIndex = 1}}
        slides[slideIndex-1].style.display = "block";
        setTimeout(showSlides, 3000);
    }}
    </script>
    """

    st.components.v1.html(html, height=530)


# =========================
# APP
# =========================

fotos = carregar_fotos()

st.sidebar.title("❤️ Menu do Amor")
pagina = st.sidebar.radio(
    "Escolha uma página:",
    [
        "🏠 Início",
        "📸 Galeria",
        "💕 Motivos para Shippar",
        "😂 Curiosidades",
        "💌 Cartinha",
        "🌟 Futuro"
    ]
)

tocar_musica()

# =========================
# PÁGINA INICIAL
# =========================

if pagina == "🏠 Início":
    st.markdown(f"<div class='titulo'>{NOME_1} ❤️ {NOME_2}</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitulo'>O casal mais lindo do Brasil</div>", unsafe_allow_html=True)
    st.write("")

    if fotos:
        slideshow_html(fotos)
    else:
        st.info("Coloque fotos na pasta /fotos para aparecerem aqui.")

    st.markdown("""
    <div class="card">
        Algumas pessoas se encontram por acaso.<br>
        Outras parecem ter sido destinadas uma à outra. ❤️
    </div>
    """, unsafe_allow_html=True)

# =========================
# GALERIA
# =========================

elif pagina == "📸 Galeria":
    st.markdown("<div class='titulo'>Galeria de Momentos 📸</div>", unsafe_allow_html=True)

    if fotos:
        colunas = st.columns(3)

        for i, foto in enumerate(fotos):
            with colunas[i % 3]:
                st.image(foto, use_container_width=True)
    else:
        st.info("Adicione fotos na pasta /fotos.")

# =========================
# MOTIVOS
# =========================

elif pagina == "💕 Motivos para Shippar":
    st.markdown("<div class='titulo'>Motivos para Shippar 💕</div>", unsafe_allow_html=True)

    motivos = [
        "Porque juntos eles combinam demais.",
        "Porque um completa a loucura do outro.",
        "Porque são fofos até sem tentar.",
        "Porque esse casal tem energia de filme romântico.",
        "Porque Gabriel e Rilary simplesmente fazem sentido.",
        "Porque são o casal mais lindo do Brasil."
    ]

    if st.button("Sortear motivo ❤️"):
        st.success(random.choice(motivos))

    for motivo in motivos:
        st.markdown(f"<div class='card'>{motivo}</div>", unsafe_allow_html=True)

# =========================
# CURIOSIDADES
# =========================

elif pagina == "😂 Curiosidades":
    st.markdown("<div class='titulo'>Curiosidades do Casal 😂</div>", unsafe_allow_html=True)

    perguntas = [
        "Quem é mais ciumento?",
        "Quem demora mais para responder?",
        "Quem sente mais saudade?",
        "Quem é mais dramático?",
        "Quem pede desculpas primeiro?",
        "Quem é mais provável de mandar áudio gigante?"
    ]

    for p in perguntas:
        st.markdown(f"<div class='card'>💭 {p}</div>", unsafe_allow_html=True)

# =========================
# CARTINHA
# =========================

elif pagina == "💌 Cartinha":
    st.markdown("<div class='titulo'>Cartinha Especial 💌</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        Gabriel e Rilary,<br><br>
        Que vocês continuem sendo esse casal leve, bonito e cheio de carinho.
        Que cada momento juntos vire lembrança boa, cada sorriso vire motivo
        para continuar, e cada fase fortaleça ainda mais essa história.
        <br><br>
        Vocês são especiais juntos. ❤️
    </div>
    """, unsafe_allow_html=True)

# =========================
# FUTURO
# =========================

elif pagina == "🌟 Futuro":
    st.markdown("<div class='titulo'>O Futuro de Vocês 🌟</div>", unsafe_allow_html=True)

    sonhos = [
        "Viajar juntos.",
        "Criar muitas memórias.",
        "Superar fases difíceis lado a lado.",
        "Rir de coisas bobas.",
        "Construir uma história bonita.",
        "Continuar sendo o casal mais lindo do Brasil."
    ]

    for sonho in sonhos:
        st.markdown(f"<div class='card'>✨ {sonho}</div>", unsafe_allow_html=True)
