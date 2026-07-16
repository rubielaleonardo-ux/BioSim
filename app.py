import streamlit as st

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="BioSim: Laboratorio Virtual", layout="wide")

# --- ESTADO INICIAL ---
if 'sim_actual' not in st.session_state:
    st.session_state.sim_actual = "1. Transcripción y Traducción"
if 'secuencia_maestra' not in st.session_state:
    st.session_state.secuencia_maestra = "ATGGCCCTGTGGATGCGCCT"

simuladores = [
    "1. Transcripción y Traducción",
    "2. Mutaciones y Estructura Proteica",
    "3. Matriz de Alineamiento Global",
    "4. Gráficos de De Bruijn (Ensamble)",
    "5. Distancia Filogenética Básica"
]

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
    
    # Campo global para mantener la coherencia de la secuencia en los módulos
    st.session_state.secuencia_maestra = st.text_input("Secuencia de ADN de trabajo:", st.session_state.secuencia_maestra).upper().replace(" ", "")

    # --- SIMULADORES ---
    if st.session_state.sim_actual == "1. Transcripción y Traducción":
        st.header("1. Transcripción y Traducción")
        if st.session_state.secuencia_maestra:
            arn = adn_a_arn(st.session_state.secuencia_maestra)
            st.success(f"ARNm: {arn}")
            aa = [codones.get(arn[i:i+3], "??") for i in range(0, len(arn)-2, 3)]
            st.write(f"**Proteína:** {' - '.join(aa)}")

    elif st.session_state.sim_actual == "2. Mutaciones y Estructura Proteica":
        st.header("2. Impacto de Mutaciones")
        arn_base = adn_a_arn(st.session_state.secuencia_maestra)
        if arn_base:
            pos = st.slider("Posición en ARNm:", 0, len(arn_base)-1, 0)
            nuc = st.selectbox("Cambiar a:", ["A", "U", "C", "G"])
            mut = list(arn_base); mut[pos] = nuc; mut_arn = "".join(mut)
            st.warning(f"ARNm Mutado: `{mut_arn}`")

    elif st.session_state.sim_actual == "3. Matriz de Alineamiento Global":
        st.header("3. Matriz de Alineamiento")
        st.table([[""] + list(st.session_state.secuencia_maestra)] + [[c2] + [5 if c1==c2 else -1 for c1 in list(st.session_state.secuencia_maestra)] for c2 in ["A","T","G","C"]])

    elif st.session_state.sim_actual == "4. Gráficos de De Bruijn (Ensamble)":
        st.header("4. Ensamble de ADN")
        k = st.slider("Tamaño de k-mer:", 2, 5, 3)
        kmers = [st.session_state.secuencia_maestra[i:i+k] for i in range(len(st.session_state.secuencia_maestra) - k + 1)]
        st.write(f"Fragmentos: `{kmers}`")

    elif st.session_state.sim_actual == "5. Distancia Filogenética Básica":
        st.header("5. Distancia Evolutiva y Árbol")
        especies_db = {
            "Drosophila melanogaster": "ATGGCCCTGTGG",
            "Arabidopsis thaliana": "ATGTCCGATCGT",
            "Caenorhabditis elegans": "ATGGGCCTAGGG"
        }
        seq_usuario = st.session_state.secuencia_maestra
        if seq_usuario:
            distancias = {esp: sum(1 for a, b in zip(seq_usuario, seq_ref)) / len(seq_ref) for esp, seq_ref in especies_db.items()}
            st.bar_chart(distancias)
            st.success(f"Especie más cercana: **{min(distancias, key=distancias.get)}**")

    # --- NAVEGACIÓN ---
    st.divider()
    c1, c2 = st.columns(2)
    with c1: 
        if st.button("⬅️ Atrás"): navegar("atras"); st.rerun()
    with c2: 
        if st.button("Siguiente ➡️"): navegar("siguiente"); st.rerun()
else:
    st.warning("⚠️ Identifícate para comenzar tu práctica.")
