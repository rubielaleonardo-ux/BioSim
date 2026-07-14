import streamlit as st

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="BioSim Educativo", layout="wide")

# Inicialización del estado
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

# --- DICCIONARIO COMPLETO ---
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
st.title("🧬 BioSim: Simuladores Bioinformáticos")
with st.expander("👋 ¡Identifícate para comenzar!", expanded=True):
    nombre = st.text_input("Nombre del Estudiante:", key="nombre_user")
    nivel = st.selectbox("Nivel Escolar:", ["", "1ro Secundaria", "6to Secundaria", "Universidad"], key="nivel_user")

# --- LÓGICA DE ACCESO ---
if nombre and nivel:
    with st.sidebar:
        simulador = st.radio("Selecciona un Simulador:", pasos, index=pasos.index(st.session_state.paso_actual))
        st.session_state.paso_actual = simulador

    # --- SIMULADOR 1 ---
    if simulador == "1. Transcripción y Traducción":
        st.header("1. Expresión Génica")
        adn = st.text_input("ADN (Molde):", "TACGGCATTTATACT").upper().strip()
        if all(c in "ATCG" for c in adn) and adn:
            transc = {"A": "U", "T": "A", "C": "G", "G": "C"}
            arnm = "".join([transc.get(b, "") for b in adn])
            st.success(f"ARN: {arnm}")
            aa = [codigo_genetico.get(arnm[i:i+3], "Desconocido") for i in range(0, len(arnm)-2, 3)]
            st.metric("Polipéptido", " - ".join(aa))
        if st.button("➡️ Siguiente"): ir_al_siguiente(); st.rerun()

    # --- SIMULADOR 2 ---
    elif simulador == "2. Mutaciones y Estructura Proteica":
        st.header("2. Impacto de Mutaciones")
        sec_base = "AUGGGCACUUAA"
        pos = st.slider("Posición:", 0, 11, 4)
        nuc = st.selectbox("Nuevo nucleótido:", ["A", "U", "C", "G"])
        mut = list(sec_base); mut[pos] = nuc; mut_seq = "".join(mut)
        st.warning(f"Mutada: {mut_seq}")
        if st.button("➡️ Siguiente"): ir_al_siguiente(); st.rerun()

    # --- SIMULADOR 3 ---
    elif simulador == "3. Matriz de Alineamiento Global":
        st.header("3. Construcción de Matrices")
        s1 = st.text_input("Seq 1:", "AAGC").upper().strip()
        s2 = st.text_input("Seq 2:", "AGC").upper().strip()
        if s1 and s2:
            matriz = [[""] + ["-"] + list(s1)] + [[c2] + [5 if c1==c2 else -1 for c1 in ["-"]+list(s1)] for c2 in ["-"]+list(s2)]
            st.table(matriz)
        if st.button("➡️ Siguiente"): ir_al_siguiente(); st.rerun()

    # --- SIMULADOR 4 ---
    elif simulador == "4. Gráficos de De Bruijn (Ensamble)":
        st.header("4. Ensamble mediante Grafos")
        seq = st.text_input("ADN:", "ATGCATGC").upper().strip()
        k = st.slider("k-mer:", 2, 4, 3)
        if seq and len(seq) >= k:
            kmers = [seq[i:i+k] for i in range(len(seq) - k + 1)]
            st.write(f"Nodos: {kmers}")
        if st.button("➡️ Siguiente"): ir_al_siguiente(); st.rerun()

    # --- SIMULADOR 5 ---
    elif simulador == "5. Distancia Filogenética Básica":
        st.header("5. Distancia Filogenética")
        s1 = st.text_input("Seq 1:", "ATGC").upper()
        s2 = st.text_input("Seq 2:", "ATGG").upper()
        if s1 and s2 and len(s1)==len(s2):
            dist = sum(1 for a,b in zip(s1, s2) if a != b) / len(s1)
            st.write(f"Distancia: {dist:.2%}")
        if st.button("🔄 Reiniciar"): st.session_state.paso_actual = pasos[0]; st.rerun()

else:
    st.info("⚠️ Ingresa nombre y nivel para comenzar.")
