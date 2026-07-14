import streamlit as st

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="BioSim: Laboratorio Virtual", layout="wide")

# --- ESTADO INICIAL ---
if 'sim_actual' not in st.session_state:
    st.session_state.sim_actual = "1. Transcripción y Traducción"
if 'secuencia_maestra' not in st.session_state:
    st.session_state.secuencia_maestra = ""

simuladores = [
    "1. Transcripción y Traducción",
    "2. Mutaciones y Estructura Proteica",
    "3. Matriz de Alineamiento Global",
    "4. Gráficos de De Bruijn (Ensamble)",
    "5. Distancia Filogenética Básica"
]

# --- DICCIONARIO DE CODONES (MANTENIDO ÍNTEGRO) ---
codones = {
    'UUU':'Fenilalanina','UUC':'Fenilalanina','UUA':'Leucina','UUG':'Leucina','UCU':'Serina','UCC':'Serina','UCA':'Serina','UCG':'Serina','UAU':'Tirosina','UAC':'Tirosina','UAA':'STOP','UAG':'STOP','UGU':'Cisteína','UGC':'Cisteína','UGA':'STOP','UGG':'Triptófano','CUU':'Leucina','CUC':'Leucina','CUA':'Leucina','CUG':'Leucina','CCU':'Prolina','CCC':'Prolina','CCA':'Prolina','CCG':'Prolina','CAU':'Histidina','CAC':'Histidina','CAA':'Glutamina','CAG':'Glutamina','CGU':'Arginina','CGC':'Arginina','CGA':'Arginina','CGG':'Arginina','AUU':'Isoleucina','AUC':'Isoleucina','AUA':'Isoleucina','AUG':'Metionina','ACU':'Treonina','ACC':'Treonina','ACA':'Treonina','ACG':'Treonina','AAU':'Asparagina','AAC':'Asparagina','AAA':'Lisina','AAG':'Lisina','AGU':'Serina','AGC':'Serina','AGA':'Arginina','AGG':'Arginina','GUU':'Valina','GUC':'Valina','GUA':'Valina','GUG':'Valina','GCU':'Alanina','GCC':'Alanina','GCA':'Alanina','GCG':'Alanina','GAU':'Ácido Aspártico','GAC':'Ácido Aspártico','GAA':'Ácido Glutámico','GAG':'Ácido Glutámico','GGU':'Glicina','GGC':'Glicina','GGA':'Glicina','GGG':'Glicina'
}

def navegar(direccion):
    idx = simuladores.index(st.session_state.sim_actual)
    if direccion == "siguiente" and idx < len(simuladores) - 1:
        st.session_state.sim_actual = simuladores[idx + 1]
    elif direccion == "atras" and idx > 0:
        st.session_state.sim_actual = simuladores[idx - 1]

def adn_a_arn(adn):
    trans = {"A": "U", "T": "A", "C": "G", "G": "C"}
    return "".join([trans.get(b, "") for b in adn.upper()])

# --- INTERFAZ ---
st.title("🧬 BioSim: Laboratorio Virtual")

with st.expander("👋 ¡Identifícate para comenzar!"):
    nombre = st.text_input("Nombre del Estudiante:")
    nivel = st.selectbox("Nivel Escolar:", ["", "Secundaria", "Universidad"])

if nombre and nivel:
    st.sidebar.title("Navegación")
    st.session_state.sim_actual = st.sidebar.radio("Ir a:", simuladores, index=simuladores.index(st.session_state.sim_actual))
    
    # --- SIMULADOR 1 ---
    if st.session_state.sim_actual == "1. Transcripción y Traducción":
        st.header("1. Transcripción y Traducción")
        st.subheader("🎯 Objetivo: Convertir el ADN molde en proteína.")
        if st.button("💡 Pista"): st.info("El ARNm es el 'azúcar' del ADN; recuerda que la Timina (T) se convierte en Uracilo (U).")
        seq = st.text_input("Ingresa ADN molde (3'-5'):", value=st.session_state.secuencia_maestra)
        st.session_state.secuencia_maestra = seq.upper().replace(" ", "")
        if st.session_state.secuencia_maestra:
            arn = adn_a_arn(st.session_state.secuencia_maestra)
            st.success(f"ARNm: {arn}")
            aa = [codones.get(arn[i:i+3], "??") for i in range(0, len(arn)-2, 3)]
            st.write(f"Proteína: {' - '.join(aa)}")
            st.info("**Explicación:** El proceso pasa de información genética estática (ADN) a una forma activa (ARNm) para construir proteínas.")

    # --- SIMULADOR 2 ---
    elif st.session_state.sim_actual == "2. Mutaciones y Estructura Proteica":
        st.header("2. Impacto de Mutaciones")
        st.subheader("🎯 Objetivo: Observar cómo cambia la proteína al modificar el ARNm.")
        if st.button("💡 Pista"): st.info("Una sola letra cambiada puede causar un codón STOP prematuro. ¡Cuidado!")
        arn_base = adn_a_arn(st.session_state.secuencia_maestra)
        st.write(f"ARNm base: `{arn_base}`")
        if arn_base:
            pos = st.slider("Posición en ARNm:", 0, len(arn_base)-1, 0)
            nuc = st.selectbox("Cambiar a:", ["A", "U", "C", "G"])
            mut = list(arn_base); mut[pos] = nuc; mut_arn = "".join(mut)
            st.warning(f"ARNm Mutado: `{mut_arn}`")
            st.info("**Explicación:** Las mutaciones son alteraciones en la secuencia de nucleótidos; pueden ser silenciosas, missense o nonsense.")

    # --- SIMULADOR 3 ---
    elif st.session_state.sim_actual == "3. Matriz de Alineamiento Global":
        st.header("3. Matriz de Alineamiento")
        st.subheader("🎯 Objetivo: Identificar coincidencias entre secuencias.")
        if st.button("💡 Pista"): st.info("Las diagonales de la matriz indican dónde las letras coinciden exactamente entre ambas secuencias.")
        st.table([[""] + ["-"] + list(st.session_state.secuencia_maestra)] + [[c2] + [5 if c1==c2 else -1 for c1 in ["-"]+list(st.session_state.secuencia_maestra)] for c2 in ["-"]+list("ATGC")])
        st.info("**Explicación:** Alineamos secuencias para determinar el grado de similitud (homología) entre genes de diferentes especies.")

    # --- SIMULADOR 4 ---
    elif st.session_state.sim_actual == "4. Gráficos de De Bruijn (Ensamble)":
        st.header("4. Ensamble de ADN")
        st.subheader("🎯 Objetivo: Reconstruir ADN mediante fragmentos (k-mers).")
        if st.button("💡 Pista"): st.info("Un k-mer pequeño genera un grafo más simple pero menos preciso.")
        k = st.slider("Tamaño de k-mer:", 2, 5, 3)
        kmers = [st.session_state.secuencia_maestra[i:i+k] for i in range(len(st.session_state.secuencia_maestra) - k + 1)]
        st.write(f"Fragmentos: `{kmers}`")
        st.info("**Explicación:** El ensamble bioinformático une piezas pequeñas (k-mers) para reconstruir genomas largos, vital para la medicina personalizada.")

    # --- SIMULADOR 5 ---
    elif st.session_state.sim_actual == "5. Distancia Filogenética Básica":
        st.header("5. Distancia Evolutiva")
        st.subheader("🎯 Objetivo: Calcular qué tan lejanas están dos especies.")
        if st.button("💡 Pista"): st.info("Divide el número de diferencias entre la longitud total de la secuencia.")
        dist = sum(1 for a,b in zip(st.session_state.secuencia_maestra, "ATGCATGC") if a != b) / len(st.session_state.secuencia_maestra) if st.session_state.secuencia_maestra else 0
        st.metric("Distancia Genética", f"{dist:.2%}")
        st.info("**Explicación:** La distancia genética indica cuánto tiempo ha pasado desde que dos especies se separaron de un ancestro común.")

    # --- NAVEGACIÓN ---
    st.divider()
    c1, c2 = st.columns(2)
    with c1: 
        if st.button("⬅️ Atrás"): navegar("atras"); st.rerun()
    with c2: 
        if st.button("Siguiente ➡️"): navegar("siguiente"); st.rerun()
else:
    st.warning("⚠️ Identifícate para comenzar tu práctica de bioinformática.")
