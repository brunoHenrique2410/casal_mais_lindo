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

NOME_1 = "Gabriel Ramos"
NOME_2 = "Rilary Escobar"

PASTA_FOTOS = "fotos"
PASTA_MUSICAS = "musicas"
VOLUME_MUSICA = 0.25

st.markdown("""
<style>
[data-testid="stSidebar"], [data-testid="collapsedControl"] {display:none;}
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #1b0f1f, #3b1238, #651d4b);
    color: white;
}
[data-testid="stHeader"] {background: transparent;}
.block-container {padding-top: 25px;}

.titulo {
    text-align:center;
    font-size:52px;
    font-weight:bold;
    color:#ffb6d9;
    text-shadow:0 0 18px #ff4fa3;
}
.subtitulo {
    text-align:center;
    font-size:24px;
    color:#ffe3f1;
    margin-bottom:25px;
}
.card {
    background:rgba(255,255,255,0.11);
    padding:25px;
    border-radius:25px;
    text-align:center;
    box-shadow:0 0 22px rgba(255,105,180,0.35);
    margin:18px 0;
    font-size:20px;
}
.stButton > button {
    width:100%;
    border-radius:18px;
    border:1px solid rgba(255,255,255,0.25);
    background:rgba(255,255,255,0.12);
    color:white;
    font-weight:bold;
    padding:12px;
}
.stButton > button:hover {
    background:rgba(255,105,180,0.35);
    border:1px solid #ffb6d9;
}
img {border-radius:22px;}
.footer {
    text-align:center;
    color:#ffd6eb;
    margin-top:40px;
    opacity:0.8;
}
</style>
""", unsafe_allow_html=True)


def carregar_fotos():
    os.makedirs(PASTA_FOTOS, exist_ok=True)
    return sorted([
        os.path.join(PASTA_FOTOS, a)
        for a in os.listdir(PASTA_FOTOS)
        if a.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))
    ])


def carregar_musicas():
    os.makedirs(PASTA_MUSICAS, exist_ok=True)
    return sorted([
        os.path.join(PASTA_MUSICAS, a)
        for a in os.listdir(PASTA_MUSICAS)
        if a.lower().endswith(".mp3")
    ])


def tocar_musica_html(musica):
    with open(musica, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()

    st.markdown(f"""
    <audio controls autoplay style="width:100%;">
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>

    <script>
    const audios = window.parent.document.querySelectorAll("audio");
    audios.forEach(a => a.volume = {VOLUME_MUSICA});
    </script>
    """, unsafe_allow_html=True)


def slideshow_html(fotos):
    imagens = []
    for foto in fotos:
        with open(foto, "rb") as f:
            imagens.append("data:image/jpeg;base64," + base64.b64encode(f.read()).decode())

    slides = ""
    for img in imagens:
        slides += f"""
        <div class="slide fade" style="background-image:url('{img}')">
            <img src="{img}">
        </div>
        """

    st.components.v1.html(f"""
    <style>
    .slideshow-container {{
        max-width:680px;
        height:520px;
        margin:auto;
        border-radius:32px;
        overflow:hidden;
        box-shadow:0 0 40px rgba(255,105,180,0.7);
        background:#160b19;
    }}
    .slide {{
        display:none;
        width:100%;
        height:100%;
        position:relative;
        background-size:cover;
        background-position:center;
    }}
    .slide::before {{
        content:"";
        position:absolute;
        inset:0;
        background:inherit;
        filter:blur(25px);
        transform:scale(1.15);
        opacity:0.45;
    }}
    .slide img {{
        position:relative;
        width:100%;
        height:100%;
        object-fit:contain;
        z-index:2;
    }}
    .fade {{animation: fadeEffect 1.8s;}}
    @keyframes fadeEffect {{
        from {{opacity:.25}}
        to {{opacity:1}}
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
        if (slideIndex > slides.length) {{slideIndex = 1;}}
        slides[slideIndex - 1].style.display = "block";
        setTimeout(showSlides, 3000);
    }}
    </script>
    """, height=550)


def trocar_pagina(pagina):
    st.session_state.pagina = pagina


if "pagina" not in st.session_state:
    st.session_state.pagina = "🏠 Início"

if "site_liberado" not in st.session_state:
    st.session_state.site_liberado = False

if "musica_atual" not in st.session_state:
    st.session_state.musica_atual = 0


fotos = carregar_fotos()
musicas = carregar_musicas()

st.markdown(f"<div class='titulo'>{NOME_1} ❤️ {NOME_2}</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitulo'>O casal mais lindo do Brasil</div>", unsafe_allow_html=True)


if not st.session_state.site_liberado:
    st.markdown("""
    <div class="card">
        Clique para entrar no cantinho do casal e ativar a música ❤️
    </div>
    """, unsafe_allow_html=True)

    if st.button("❤️ Entrar e ativar música ❤️"):
        st.session_state.site_liberado = True
        st.rerun()

    st.stop()


if musicas:
    col_m1, col_m2 = st.columns([4, 1])

    with col_m1:
        tocar_musica_html(musicas[st.session_state.musica_atual])

    with col_m2:
        if st.button("🎵 Próxima"):
            st.session_state.musica_atual += 1
            if st.session_state.musica_atual >= len(musicas):
                st.session_state.musica_atual = 0
            st.rerun()
else:
    st.warning("Coloque músicas .mp3 dentro da pasta /musicas.")


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


if st.session_state.pagina == "🏠 Início":
    if fotos:
        slideshow_html(fotos)
    else:
        st.info("Coloque fotos na pasta /fotos.")

    st.markdown("""
    <div class="card">
        Algumas pessoas se encontram por acaso.<br>
        Outras parecem ter sido destinadas uma à outra. ❤️
    </div>
    """, unsafe_allow_html=True)


elif st.session_state.pagina == "📸 Galeria":
    st.markdown("<div class='titulo'>Galeria de Momentos 📸</div>", unsafe_allow_html=True)

    if fotos:
        colunas = st.columns(3)
        for i, foto in enumerate(fotos):
            with colunas[i % 3]:
                st.image(foto, use_container_width=True)
    else:
        st.info("Adicione fotos na pasta /fotos.")


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


elif st.session_state.pagina == "🎮 Quiz":
    st.markdown("<div class='titulo'>Quiz do Casal 🎮</div>", unsafe_allow_html=True)

    perguntas = [
        ("Quem é mais provável de sentir saudade primeiro?", ["Gabriel", "Rilary", "Os dois"], "Os dois"),
        ("Quem é mais provável de mandar áudio gigante?", ["Gabriel", "Rilary", "Os dois"], "Gabriel"),
        ("Quem é mais provável de roubar comida do prato do outro?", ["Gabriel", "Rilary", "Os dois"], "Rilary"),
        ("Quem é mais provável de fazer drama?", ["Gabriel", "Rilary", "Os dois"], "Os dois"),
        ("Quem é mais provável de pedir desculpas primeiro?", ["Gabriel", "Rilary", "Os dois"], "Gabriel"),
        ("Quem é mais provável de escolher o filme e dormir no meio?", ["Gabriel", "Rilary", "Os dois"], "Os dois"),
    ]

    with st.form("quiz_casal"):
        respostas = []
        for i, (pergunta, opcoes, correta) in enumerate(perguntas):
            respostas.append(st.radio(pergunta, opcoes, key=f"quiz_{i}"))

        enviar = st.form_submit_button("Ver resultado ❤️")

    if enviar:
        pontos = 0
        for i, item in enumerate(perguntas):
            if respostas[i] == item[2]:
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


st.markdown("""
<div class="footer">
    Feito com carinho ❤️
</div>
""", unsafe_allow_html=True)
