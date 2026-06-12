import streamlit as st
import base64
import os
import random

st.set_page_config(
    page_title="Gabriel & Rilary ❤️",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# CONFIGURAÇÕES
# =========================

NOME_1 = "Gabriel Ramos"
NOME_2 = "Rilary Escobar"

PASTA_FOTOS = "fotos"
PASTA_MUSICAS = "musicas"

VOLUME_MUSICA = 0.25  # 25% do volume

# =========================
# CSS
# =========================

st.markdown("""
<style>
[data-testid="stSidebar"], [data-testid="collapsedControl"] {
    display: none;
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #1b0f1f, #3b1238, #651d4b);
    color: white;
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    padding-top: 25px;
}

.titulo {
    text-align: center;
    font-size: 52px;
    font-weight: bold;
    color: #ffb6d9;
    text-shadow: 0 0 18px #ff4fa3;
    margin-bottom: 5px;
}

.subtitulo {
    text-align: center;
    font-size: 24px;
    color: #ffe3f1;
    margin-bottom: 25px;
}

.card {
    background: rgba(255,255,255,0.11);
    padding: 25px;
    border-radius: 25px;
    text-align: center;
    box-shadow: 0 0 22px rgba(255, 105, 180, 0.35);
    margin: 18px 0;
    font-size: 20px;
}

.stButton > button {
    width: 100%;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.25);
    background: rgba(255,255,255,0.12);
    color: white;
    font-weight: bold;
    padding: 12px;
    transition: 0.3s;
}

.stButton > button:hover {
    background: rgba(255, 105, 180, 0.35);
    color: white;
    border: 1px solid #ffb6d9;
    transform: scale(1.03);
}

img {
    border-radius: 22px;
}

.footer {
    text-align: center;
    color: #ffd6eb;
    margin-top: 40px;
    opacity: 0.8;
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

    return sorted(fotos)


def tocar_musicas():
    if not os.path.exists(PASTA_MUSICAS):
        os.makedirs(PASTA_MUSICAS)

    musicas = []
    for arquivo in os.listdir(PASTA_MUSICAS):
        if arquivo.lower().endswith(".mp3"):
            musicas.append(os.path.join(PASTA_MUSICAS, arquivo))

    if not musicas:
        st.warning("Coloque músicas .mp3 na pasta /musicas.")
        return

    playlist = ""

    for musica in sorted(musicas):
        with open(musica, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            playlist += f'"data:audio/mp3;base64,{b64}",'

    st.markdown(f"""
    <audio id="player" autoplay></audio>

    <script>
    const playlist = [{playlist}];
    let index = 0;
    const player = document.getElementById("player");

    player.volume = {VOLUME_MUSICA};

    function tocarAtual() {{
        player.src = playlist[index];
        player.volume = {VOLUME_MUSICA};
        player.play().catch(() => {{
            console.log("Autoplay bloqueado pelo navegador.");
        }});
    }}

    player.addEventListener("ended", function() {{
        index++;
        if (index >= playlist.length) {{
            index = 0;
        }}
        tocarAtual();
    }});

    tocarAtual();
    </script>
    """, unsafe_allow_html=True)


def slideshow_html(fotos):
    imagens_base64 = []

    for foto in fotos:
        with open(foto, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            imagens_base64.append(f"data:image/jpeg;base64,{b64}")

    slides = ""
    for img in imagens_base64:
        slides += f"""
        <div class="slide fade" style="background-image: url('{img}')">
            <img src="{img}">
        </div>
        """

    html = f"""
    <style>
    .slideshow-container {{
        max-width: 680px;
        height: 520px;
        position: relative;
        margin: auto;
        border-radius: 32px;
        overflow: hidden;
        box-shadow: 0 0 40px rgba(255, 105, 180, 0.7);
        background: #160b19;
    }}

    .slide {{
        display: none;
        width: 100%;
        height: 100%;
        position: relative;
        background-size: cover;
        background-position: center;
    }}

    .slide::before {{
        content: "";
        position: absolute;
        inset: 0;
        background: inherit;
        filter: blur(25px);
        transform: scale(1.15);
        opacity: 0.45;
    }}

    .slide img {{
        position: relative;
        width: 100%;
        height: 100%;
        object-fit: contain;
        z-index: 2;
    }}

    .fade {{
        animation: fadeEffect 1.8s;
    }}

    @keyframes fadeEffect {{
        from {{opacity: .25}}
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

        if (slideIndex > slides.length) {{
            slideIndex = 1;
        }}

        slides[slideIndex - 1].style.display = "block";
        setTimeout(showSlides, 3000);
    }}
    </script>
    """

    st.components.v1.html(html, height=550)


def trocar_pagina(pagina):
    st.session_state.pagina = pagina


# =========================
# ESTADO
# =========================

if "pagina" not in st.session_state:
    st.session_state.pagina = "🏠 Início"

fotos = carregar_fotos()
tocar_musicas()

# =========================
# CABEÇALHO
# =========================

st.markdown(f"<div class='titulo'>{NOME_1} ❤️ {NOME_2}</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitulo'>O casal mais lindo do Brasil</div>", unsafe_allow_html=True)

# =========================
# MENU
# =========================

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    if st.button("🏠 Início"):
        trocar_pagina("🏠 Início")

with col2:
    if st.button("📸 Galeria"):
        trocar_pagina("📸 Galeria")

with col3:
    if st.button("💕 Motivos"):
        trocar_pagina("💕 Motivos")

with col4:
    if st.button("🎮 Quiz"):
        trocar_pagina("🎮 Quiz")

with col5:
    if st.button("💌 Cartinha"):
        trocar_pagina("💌 Cartinha")

with col6:
    if st.button("🌟 Futuro"):
        trocar_pagina("🌟 Futuro")

st.write("")

# =========================
# INÍCIO
# =========================

if st.session_state.pagina == "🏠 Início":
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

elif st.session_state.pagina == "📸 Galeria":
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

elif st.session_state.pagina == "💕 Motivos":
    st.markdown("<div class='titulo'>Motivos para Shippar 💕</div>", unsafe_allow_html=True)

    motivos = [
        "Porque juntos eles combinam demais.",
        "Porque um completa a loucura do outro.",
        "Porque são fofos até sem tentar.",
        "Porque esse casal tem energia de filme romântico.",
        "Porque Gabriel e Rilary simplesmente fazem sentido.",
        "Porque são o casal mais lindo do Brasil.",
        "Porque onde tem eles dois, tem risada.",
        "Porque o amor deles deixa qualquer dia mais bonito."
    ]

    if st.button("Sortear motivo ❤️"):
        st.success(random.choice(motivos))

    for motivo in motivos:
        st.markdown(f"<div class='card'>{motivo}</div>", unsafe_allow_html=True)

# =========================
# QUIZ
# =========================

elif st.session_state.pagina == "🎮 Quiz":
    st.markdown("<div class='titulo'>Quiz do Casal 🎮</div>", unsafe_allow_html=True)

    perguntas = [
        {
            "pergunta": "Quem é mais provável de sentir saudade primeiro?",
            "opcoes": ["Gabriel", "Rilary", "Os dois"],
            "resposta": "Os dois"
        },
        {
            "pergunta": "Quem é mais provável de mandar áudio gigante?",
            "opcoes": ["Gabriel", "Rilary", "Os dois"],
            "resposta": "Gabriel"
        },
        {
            "pergunta": "Quem é mais provável de roubar comida do prato do outro?",
            "opcoes": ["Gabriel", "Rilary", "Os dois"],
            "resposta": "Rilary"
        },
        {
            "pergunta": "Quem é mais provável de fazer drama?",
            "opcoes": ["Gabriel", "Rilary", "Os dois"],
            "resposta": "Os dois"
        },
        {
            "pergunta": "Quem é mais provável de pedir desculpas primeiro?",
            "opcoes": ["Gabriel", "Rilary", "Os dois"],
            "resposta": "Gabriel"
        },
        {
            "pergunta": "Quem é mais provável de escolher o filme e dormir no meio?",
            "opcoes": ["Gabriel", "Rilary", "Os dois"],
            "resposta": "Os dois"
        }
    ]

    pontos = 0

    with st.form("quiz_casal"):
        respostas_usuario = []

        for i, item in enumerate(perguntas):
            resposta = st.radio(
                item["pergunta"],
                item["opcoes"],
                key=f"quiz_{i}"
            )
            respostas_usuario.append(resposta)

        enviar = st.form_submit_button("Ver resultado ❤️")

    if enviar:
        for i, item in enumerate(perguntas):
            if respostas_usuario[i] == item["resposta"]:
                pontos += 1

        st.markdown(f"""
        <div class="card">
            Resultado: {pontos}/{len(perguntas)} acertos ❤️
        </div>
        """, unsafe_allow_html=True)

        if pontos == len(perguntas):
            st.balloons()
            st.success("Perfeito! Você conhece esse casal melhor que todo mundo 😍")
        elif pontos >= 4:
            st.success("Mandou bem! Você sabe bastante sobre eles 😄")
        else:
            st.warning("Hmm... precisa acompanhar mais esse casal kkkkk")

# =========================
# CARTINHA
# =========================

elif st.session_state.pagina == "💌 Cartinha":
    st.markdown("<div class='titulo'>Cartinha Especial 💌</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        Gabriel e Rilary,<br><br>
        Que vocês continuem sendo esse casal leve, bonito e cheio de carinho.
        Que cada momento juntos vire lembrança boa, cada sorriso vire motivo
        para continuar, e cada fase fortaleça ainda mais essa história.
        <br><br>
        Algumas histórias não precisam ser perfeitas para serem lindas.
        Elas só precisam ser verdadeiras.
        <br><br>
        E a de vocês tem aquele jeitinho especial de quem nasceu para dar certo. ❤️
    </div>
    """, unsafe_allow_html=True)

# =========================
# FUTURO
# =========================

elif st.session_state.pagina == "🌟 Futuro":
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

# =========================
# RODAPÉ
# =========================

st.markdown("""
<div class="footer">
    Feito com carinho ❤️
</div>
""", unsafe_allow_html=True)
