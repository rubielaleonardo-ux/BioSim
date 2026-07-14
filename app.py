import streamlit as st

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="BioSim Educativo", layout="wide")

# Inicialización de estado
if 'paso_actual' not in st.session_state:
    st.session_state.paso_actual = "1. Transcripción y Traducción"

pasos = [
    "1. Transcripción y Traducción",
    "2. Mutaciones y Estructura Proteica",
    "3. Matriz de Alineamiento Global",
    "4. Gráficos de De Bruijn (Ensamble)",
    "5. Distancia Filogenética Básica"
]

def ir_al_siguiente():
    idx = pasos.index(st.session_state.paso_actual)
    if idx < len(pasos) - 1:
        st.session_state.paso_actual = pasos[idx + 1]

# --- DICCIONARIO GENÉTICO ---
codigo_genetico = {
    'UUU': 'Fenilalanina', 'UUC': 'Fenilalanina', 'UUA': 'Leucina', 'UUG': 'Leucina', 
    'UCU': 'Serina', 'UCC': 'Serina', 'UCA': 'Serina', 'UCG': 'Serina',
    'UAU': 'Tirosina', 'UAC': 'Tirosina', 'UAA': 'STOP', 'UAG': 'STOP', 
    'UGU': 'Cisteína', 'UGC': 'Cisteína', 'UGA': 'STOP', 'UGG': 'Triptófano',
    'CUU': 'Leucina', 'CUC': 'Leucina', 'CUA': 'Leucina', 'CUG': 'Leucina', 
    'CCU': 'Prolina', 'CCC': 'Prolina', 'CCA': 'Prolina', 'CCG': 'Prolina',
    'CAU': 'Histidina', 'CAC': 'Histidina', 'CAA': 'Glutamina', 'CAG': 'Glutamina', 
    'CGU': 'Arginina', 'CGC': 'Arginina', 'CGA': 'Arginina', 'CGG': 'Arginina',
    'AUU': 'Isoleucina', 'AUC': 'Isoleucina', 'AUA': 'Isoleucina', 'AUG': 'Metionina (Inicio)', 
    'ACU': 'Treonina', 'ACC': 'Treonina', 'ACA': 'Treonina', 'ACG': 'Treonina',
    'AAU': 'Asparagina', 'AAC': 'Asparagina', 'AAA': 'Lisina', 'AAG': 'Lisina', 
    'AGU': 'Serina', 'AGC': 'Serina', 'AGA': 'Arginina', 'AGG': 'Arginina',
    'GUU': 'Valina', 'GUC': 'Valina', 'GUA': 'Valina', 'GUG': 'Valina', 
    'GCU': 'Alanina', 'GCC': 'Alanina', 'GCA': 'Alanina', 'GCG': 'Alanina',
    'GAU': 'Ácido Aspártico', 'GAC': 'Ácido Aspártico', 'GAA': 'Ácido Glutámico', 'GAG': 'Ácido Glutámico', 
    'GGU': 'Glicina', 'GGC': 'Glicina', 'GGA': 'Glicina', 'GGG': 'Glicina'
}

# --- IDENTIFICACIÓN ---
st.title("🧬 BioSim: Laboratorio Virtual")
with st.expander("👋 ¡Identifícate para comenzar!", expanded=True):
    nombre = st.text_input("Nombre del Estudiante:", value="")
    nivel = st.selectbox("Nivel Escolar:", ["", "Secundaria", "Universidad"])

if nombre and nivel:
    with st.sidebar:
        simulador = st.radio("Navegación:", pasos, index=pasos.index(st.session_state.paso_actual))
        st.session_state.paso_actual = simulador

    # --- SIMULADOR 1 ---
    if simulador == "1. Transcripción y Traducción":
        st.header("1. Transcripción y Traducción de ADN")
        st.info("INSTRUCCIONES: Ingresa una secuencia de ADN molde (ej. TACGGCATTTATACT) y presiona ENTER. Observa cómo se convierte en ARNm y qué aminoácidos produce.")
        adn = st.text_input("Ingresa ADN (3' a 5'):", value="")
        if all(c in "ATCG" for c in adn) and adn:
            transc = {"A": "U", "T": "A", "C": "G", "G": "C"}
            arnm = "".join([transc.get(b, "") for b in adn])
            st.write(f"**Resultado de Transcripción (ARNm):** `{arnm}`")
            aa = [codigo_genetico.get(arnm[i:i+3], "Desconocido") for i in range(0, len(arnm)-2, 3)]
            st.success(f"**Resultado de Traducción (Polipéptido):** " + " - ".join(aa))
        if st.button("➡️ Siguiente: Mutaciones"): ir_al_siguiente(); st.rerun()

    # --- SIMULADOR 2 ---
    elif simulador == "2. Mutaciones y Estructura Proteica":
        st.header("2. Impacto de Mutaciones")
        st.info("INSTRUCCIONES: Escribe una secuencia de ARNm, selecciona una posición y cambia el nucleótido. Analiza si la proteína resultante cambia o se detiene.")
        sec_base = st.text_input("Ingresa ARNm base (ej. AUGGGCACUUAA):", value="")
        if sec_base:
            pos = st.slider("Posición para alterar:", 0, len(sec_base)-1, 0)
            nuc = st.selectbox("Nuevo nucleótido:", ["A", "U", "C", "G"])
            mut_seq = list(sec_base); mut_seq[pos] = nuc; mut_seq = "".join(mut_seq)
            st.warning(f"ARNm original: `{sec_base}` | ARNm mutado: `{mut_seq}`")
        if st.button("➡️ Siguiente: Matrices"): ir_al_siguiente(); st.rerun()

    # --- SIMULADOR 3 ---
    elif simulador == "3. Matriz de Alineamiento Global":
        st.header("3. Matriz de Puntuación")
        st.info("INSTRUCCIONES: Ingresa dos secuencias de ADN para comparar. El simulador generará una matriz de alineamiento basada en coincidencias (+5) y desajustes (-1).")
        s1 = st.text_input("Secuencia Horizontal:", value="")
        s2 = st.text_input("Secuencia Vertical:", value="")
        if s1 and s2:
            matriz = [[""] + ["-"] + list(s1)] + [[c2] + [5 if c1==c2 else -1 for c1 in ["-"]+list(s1)] for c2 in ["-"]+list(s2)]
            st.table(matriz)
        if st.button("➡️ Siguiente: Grafos"): ir_al_siguiente(); st.rerun()

    # --- SIMULADOR 4 ---
    elif simulador == "4. Gráficos de De Bruijn (Ensamble)":
        st.header("4. Ensamble de ADN mediante Grafos")
        st.info("INSTRUCCIONES: Ingresa una secuencia larga y elige un tamaño 'k'. El sistema fragmentará el ADN en 'k-mers' para visualizar el grafo de ensamble.")
        seq = st.text_input("Ingresa ADN para ensamblar:", value="")
        if seq:
            k = st.slider("Tamaño de fragmento (k):", 2, 5, 3)
            if len(seq) >= k:
                kmers = [seq[i:i+k] for i in range(len(seq) - k + 1)]
                st.write(f"Fragmentos generados: `{kmers}`")
                for km in kmers: st.write(f"Nodo `{km[:-1]}` ➔ Nodo `{km[1:]}`")
        if st.button("➡️ Siguiente: Filogenética"): ir_al_siguiente(); st.rerun()

    # --- SIMULADOR 5 ---
    elif simulador == "5. Distancia Filogenética Básica":
        st.header("5. Distancia Evolutiva")
        st.info("INSTRUCCIONES: Compara dos especies ingresando sus secuencias de ADN. El simulador calculará la distancia genética porcentual entre ambas.")
        s1 = st.text_input("Secuencia Especie 1:", value="")
        s2 = st.text_input("Secuencia Especie 2:", value="")
        if s1 and s2 and len(s1)==len(s2):
            dist = sum(1 for a,b in zip(s1, s2) if a != b) / len(s1)
            st.metric("Distancia Genética", f"{dist:.2%}")
        if st.button("🔄 Reiniciar"): st.session_state.paso_actual = pasos[0]; st.rerun()

else:
    st.info("⚠️ Por favor, ingresa tu nombre y nivel para comenzar la práctica.")
