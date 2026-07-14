import streamlit as st

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="BioSim: Laboratorio Virtual", layout="wide")

# --- ESTADO INICIAL ---
if 'paso_actual' not in st.session_state:
    st.session_state.paso_actual = "1. Transcripción y Traducción"
if 'secuencia_maestra' not in st.session_state:
    st.session_state.secuencia_maestra = ""

pasos = [
    "1. Transcripción y Traducción",
    "2. Mutaciones y Estructura Proteica",
    "3. Matriz de Alineamiento Global",
    "4. Gráficos de De Bruijn (Ensamble)",
    "5. Distancia Filogenética Básica"
]

def navegar(direccion):
    idx = pasos.index(st.session_state.paso_actual)
    if direccion == "siguiente" and idx < len(pasos) - 1:
        st.session_state.paso_actual = pasos[idx + 1]
    elif direccion == "atras" and idx > 0:
        st.session_state.paso_actual = pasos[idx - 1]

# Función auxiliar para convertir ADN a ARNm
def adn_a_arn(adn):
    trans = {"A": "U", "T": "A", "C": "G", "G": "C"}
    return "".join([trans.get(b, "") for b in adn.upper()])

# Diccionario Genético
codones = {
    'UUU':'Fenilalanina','UUC':'Fenilalanina','UUA':'Leucina','UUG':'Leucina','UCU':'Serina',
    'UCC':'Serina','UCA':'Serina','UCG':'Serina','UAU':'Tirosina','UAC':'Tirosina','UAA':'STOP',
    'UAG':'STOP','UGU':'Cisteína','UGC':'Cisteína','UGA':'STOP','UGG':'Triptófano','CUU':'Leucina',
    'CUC':'Leucina','CUA':'Leucina','CUG':'Leucina','CCU':'Prolina','CCC':'Prolina','CCA':'Prolina',
    'CCG':'Prolina','CAU':'Histidina','CAC':'Histidina','CAA':'Glutamina','CAG':'Glutamina',
    'CGU':'Arginina','CGC':'Arginina','CGA':'Arginina','CGG':'Arginina','AUU':'Isoleucina',
    'AUC':'Isoleucina','AUA':'Isoleucina','AUG':'Metionina','ACU':'Treonina','ACC':'Treonina',
    'ACA':'Treonina','ACG':'Treonina','AAU':'Asparagina','AAC':'Asparagina','AAA':'Lisina',
    'AAG':'Lisina','AGU':'Serina','AGC':'Serina','AGA':'Arginina','AGG':'Arginina','GUU':'Valina',
    'GUC':'Valina','GUA':'Valina','GUG':'Valina','GCU':'Alanina','GCC':'Alanina','GCA':'Alanina',
    'GCG':'Alanina','GAU':'Ácido Aspártico','GAC':'Ácido Aspártico','GAA':'Ácido Glutámico',
    'GAG':'Ácido Glutámico','GGU':'Glicina','GGC':'Glicina','GGA':'Glicina','GGG':'Glicina'
}

# --- INTERFAZ PRINCIPAL ---
st.title("🧬 BioSim: Laboratorio Virtual")
st.markdown("La **Bioinformática** integra biología y computación para descifrar los secretos de la vida.")

with st.expander("👋 ¡Identifícate!", expanded=True):
    nombre = st.text_input("Nombre:")
    nivel = st.selectbox("Nivel:", ["", "Secundaria", "Universidad"])

if nombre and nivel:
    st.sidebar.title("Navegación")
    simulador = st.sidebar.radio("Ir a:", pasos, index=pasos.index(st.session_state.paso_actual))
    st.session_state.paso_actual = simulador

    # --- SIMULADOR 1 ---
    if simulador == "1. Transcripción y Traducción":
        st.header("1. Transcripción y Traducción")
        seq = st.text_input("Ingresa ADN molde (3'-5'):", value=st.session_state.secuencia_maestra)
        st.session_state.secuencia_maestra = seq.upper().replace(" ", "")
        if st.session_state.secuencia_maestra:
            arn = adn_a_arn(st.session_state.secuencia_maestra)
            st.success(f"ARNm: {arn}")
            aa = [codones.get(arn[i:i+3], "??") for i in range(0, len(arn)-2, 3)]
            st.write(f"Proteína: {' - '.join(aa)}")

    # --- SIMULADOR 2 (CORREGIDO: Trabaja con ARNm) ---
    elif simulador == "2. Mutaciones y Estructura Proteica":
        st.header("2. Impacto de Mutaciones (ARNm)")
        arn_base = adn_a_arn(st.session_state.secuencia_maestra)
        st.info(f"ARNm original: `{arn_base}`")
        if arn_base:
            pos = st.slider("Posición a mutar en el ARNm:", 0, len(arn_base)-1, 0)
            nuc = st.selectbox("Nuevo nucleótido:", ["A", "U", "C", "G"])
            mut = list(arn_base)
            mut[pos] = nuc
            mut_arn = "".join(mut)
            st.warning(f"ARNm Mutado: `{mut_arn}`")
            aa_mut = [codones.get(mut_arn[i:i+3], "??") for i in range(0, len(mut_arn)-2, 3)]
            st.write(f"Nueva proteína: {' - '.join(aa_mut)}")

    # --- SIMULADOR 3 ---
    elif simulador == "3. Matriz de Alineamiento Global":
        st.header("3. Matriz de Alineamiento")
        s1 = st.text_input("Secuencia 1:", value=st.session_state.secuencia_maestra)
        s2 = st.text_input("Secuencia 2:", value=st.session_state.secuencia_maestra)
        if s1 and s2:
            st.table([[""] + ["-"] + list(s1)] + [[c2] + [5 if c1==c2 else -1 for c1 in ["-"]+list(s1)] for c2 in ["-"]+list(s2)])

    # --- SIMULADOR 4 ---
    elif simulador == "4. Gráficos de De Bruijn (Ensamble)":
        st.header("4. Ensamble de ADN")
        k = st.slider("Tamaño de k-mer:", 2, 5, 3)
        if st.session_state.secuencia_maestra:
            kmers = [st.session_state.secuencia_maestra[i:i+k] for i in range(len(st.session_state.secuencia_maestra) - k + 1)]
            st.write(f"Fragmentos: `{kmers}`")

    # --- SIMULADOR 5 ---
    elif simulador == "5. Distancia Filogenética Básica":
        st.header("5. Distancia Evolutiva")
        seq1 = st.text_input("Seq 1:", value=st.session_state.secuencia_maestra)
        seq2 = st.text_input("Seq 2 (Comparativa):", value="ATGCATGC")
        if seq1 and seq2 and len(seq1)==len(seq2):
            dist = sum(1 for a,b in zip(seq1, seq2) if a != b) / len(seq1)
            st.metric("Distancia Genética", f"{dist:.2%}")

    # --- NAVEGACIÓN ---
    st.divider()
    c1, c2 = st.columns(2)
    with c1: 
        if st.button("⬅️ Atrás"): navegar("atras"); st.rerun()
    with c2: 
        if st.button("Siguiente ➡️"): navegar("siguiente"); st.rerun()
else:
    st.warning("⚠️ Por favor, identifícate para acceder al laboratorio.")
