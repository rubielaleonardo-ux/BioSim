import streamlit as st

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="BioSim Educativo", layout="wide")

# Inicialización del estado persistente para navegación y datos
if 'paso_actual' not in st.session_state:
    st.session_state.paso_actual = "1. Transcripción y Traducción"

pasos = [
    "1. Transcripción y Traducción",
    "2. Mutaciones y Estructura Proteica",
    "3. Matriz de Alineamiento Global",
    "4. Gráficos de De Bruijn (Ensamble)",
    "5. Distancia Filogenética Básica"
]

# Inicializar almacenamiento para que los datos no se borren
if 'inputs' not in st.session_state:
    st.session_state.inputs = {paso: {} for paso in pasos}

# Funciones de navegación
def navegar(direccion):
    idx = pasos.index(st.session_state.paso_actual)
    if direccion == "siguiente" and idx < len(pasos) - 1:
        st.session_state.paso_actual = pasos[idx + 1]
    elif direccion == "atras" and idx > 0:
        st.session_state.paso_actual = pasos[idx - 1]

# Diccionario completo
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

# --- INTERFAZ ---
st.title("🧬 BioSim: Laboratorio Virtual")
nombre = st.sidebar.text_input("Nombre del Estudiante:")

if nombre:
    st.sidebar.write(f"Bienvenido, {nombre}")
    simulador = st.sidebar.radio("Navegación:", pasos, index=pasos.index(st.session_state.paso_actual))
    st.session_state.paso_actual = simulador

    # --- SIMULADOR 1 ---
    if simulador == "1. Transcripción y Traducción":
        st.header("1. Transcripción y Traducción")
        adn = st.text_input("ADN (3' a 5'):", value=st.session_state.inputs[simulador].get("adn", ""))
        st.session_state.inputs[simulador]["adn"] = adn
        if adn:
            trans = {"A": "U", "T": "A", "C": "G", "G": "C"}
            arn = "".join([trans.get(b, "") for b in adn.upper()])
            st.write(f"**ARNm:** `{arn}`")
            aa = [codigo_genetico.get(arn[i:i+3], "??") for i in range(0, len(arn)-2, 3)]
            st.success(f"**Aminoácidos:** " + " - ".join(aa))

    # --- SIMULADOR 2 ---
    elif simulador == "2. Mutaciones y Estructura Proteica":
        st.header("2. Impacto de Mutaciones")
        sec = st.text_input("ARNm base:", value=st.session_state.inputs[simulador].get("sec", ""))
        st.session_state.inputs[simulador]["sec"] = sec
        if sec:
            pos = st.slider("Posición:", 0, len(sec)-1, 0)
            nuc = st.selectbox("Nuevo nucleótido:", ["A", "U", "C", "G"])
            mut = list(sec); mut[pos] = nuc; mut_seq = "".join(mut)
            st.warning(f"Mutada: `{mut_seq}`")

    # --- SIMULADOR 3 ---
    elif simulador == "3. Matriz de Alineamiento Global":
        st.header("3. Matriz de Alineamiento")
        s1 = st.text_input("Horizontal:", value=st.session_state.inputs[simulador].get("s1", ""))
        s2 = st.text_input("Vertical:", value=st.session_state.inputs[simulador].get("s2", ""))
        st.session_state.inputs[simulador].update({"s1": s1, "s2": s2})
        if s1 and s2:
            st.table([[""] + ["-"] + list(s1)] + [[c2] + [5 if c1==c2 else -1 for c1 in ["-"]+list(s1)] for c2 in ["-"]+list(s2)])

    # --- SIMULADOR 4 ---
    elif simulador == "4. Gráficos de De Bruijn (Ensamble)":
        st.header("4. Ensamble de ADN")
        seq = st.text_input("ADN:", value=st.session_state.inputs[simulador].get("seq", ""))
        st.session_state.inputs[simulador]["seq"] = seq
        if seq:
            k = st.slider("k-mer:", 2, 5, 3)
            kmers = [seq[i:i+k] for i in range(len(seq) - k + 1)]
            st.write(f"Fragmentos: `{kmers}`")

    # --- SIMULADOR 5 ---
    elif simulador == "5. Distancia Filogenética Básica":
        st.header("5. Distancia Evolutiva")
        s1 = st.text_input("Seq 1:", value=st.session_state.inputs[simulador].get("s1", ""))
        s2 = st.text_input("Seq 2:", value=st.session_state.inputs[simulador].get("s2", ""))
        st.session_state.inputs[simulador].update({"s1": s1, "s2": s2})
        if s1 and s2 and len(s1)==len(s2):
            st.metric("Distancia", f"{(sum(1 for a,b in zip(s1, s2) if a != b) / len(s1)):.2%}")

    # --- BOTONES NAVEGACIÓN ---
    st.divider()
    c1, c2 = st.columns(2)
    with c1: 
        if st.button("⬅️ Atrás"): navegar("atras"); st.rerun()
    with c2: 
        if st.button("Siguiente ➡️"): navegar("siguiente"); st.rerun()

else:
    st.info("⚠️ Ingresa tu nombre en el panel lateral para comenzar.")
