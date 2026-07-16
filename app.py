import streamlit as st

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="BioSim: Laboratorio Virtual", layout="wide")

# --- ESTADO INICIAL ---
if 'sim_actual' not in st.session_state: st.session_state.sim_actual = "1. Transcripción y Traducción"
if 'secuencia_maestra' not in st.session_state: st.session_state.secuencia_maestra = "ATGGCCCTGTGGATGCGCCT"

# --- DICCIONARIO DE CODONES ---
codones = {'UUU':'Fenilalanina','UUC':'Fenilalanina','UUA':'Leucina','UUG':'Leucina','UCU':'Serina','UCC':'Serina','UCA':'Serina','UCG':'Serina','UAU':'Tirosina','UAC':'Tirosina','UAA':'STOP','UAG':'STOP','UGU':'Cisteína','UGC':'Cisteína','UGA':'STOP','UGG':'Triptófano','CUU':'Leucina','CUC':'Leucina','CUA':'Leucina','CUG':'Leucina','CCU':'Prolina','CCC':'Prolina','CCA':'Prolina','CCG':'Prolina','CAU':'Histidina','CAC':'Histidina','CAA':'Glutamina','CAG':'Glutamina','CGU':'Arginina','CGC':'Arginina','CGA':'Arginina','CGG':'Arginina','AUU':'Isoleucina','AUC':'Isoleucina','AUA':'Isoleucina','AUG':'Metionina','ACU':'Treonina','ACC':'Treonina','ACA':'Treonina','ACG':'Treonina','AAU':'Asparagina','AAC':'Asparagina','AAA':'Lisina','AAG':'Lisina','AGU':'Serina','AGC':'Serina','AGA':'Arginina','AGG':'Arginina','GUU':'Valina','GUC':'Valina','GUA':'Valina','GUG':'Valina','GCU':'Alanina','GCC':'Alanina','GCA':'Alanina','GCG':'Alanina','GAU':'Ácido Aspártico','GAC':'Ácido Aspártico','GAA':'Ácido Glutámico','GAG':'Ácido Glutámico','GGU':'Glicina','GGC':'Glicina','GGA':'Glicina','GGG':'Glicina'}

simuladores = ["1. Transcripción y Traducción", "2. Mutaciones y Estructura Proteica", "3. Matriz de Alineamiento Global", "4. Gráficos de De Bruijn (Ensamble)", "5. Distancia Filogenética Básica"]

# --- LÓGICA ---
def adn_a_arn(adn):
    trans = {"A": "U", "T": "A", "C": "G", "G": "C"}
    return "".join([trans.get(b, "") for b in adn.upper()])

def navegar(direccion):
    idx = simuladores.index(st.session_state.sim_actual)
    if direccion == "siguiente" and idx < len(simuladores) - 1: st.session_state.sim_actual = simuladores[idx + 1]
    elif direccion == "atras" and idx > 0: st.session_state.sim_actual = simuladores[idx - 1]

# --- INTERFAZ ---
st.title("🧬 BioSim: Laboratorio Virtual")

with st.expander("👋 ¡Identifícate para comenzar!"):
    nombre = st.text_input("Nombre del Estudiante:")
    nivel = st.selectbox("Nivel Escolar:", ["", "Secundaria", "Universidad"])

if nombre and nivel:
    # Barra Lateral
    st.sidebar.title("Configuración")
    casos_estudio = {
        "Insulina (Conservación)": "ATGGCCCTGTGGATGCGCCT",
        "Resistencia (Variabilidad)": "ATGTCCGATCGTCTTGTCGT"
    }
    selector = st.sidebar.selectbox("Elige un caso:", list(casos_estudio.keys()))
    if st.sidebar.button("Cargar Secuencia"):
        st.session_state.secuencia_maestra = casos_estudio[selector]
        st.rerun()

    st.sidebar.divider()
    st.session_state.sim_actual = st.sidebar.radio("Navegación:", simuladores, index=simuladores.index(st.session_state.sim_actual))
    
    # --- MÓDULOS ---
    if st.session_state.sim_actual == "1. Transcripción y Traducción":
        st.header("1. Transcripción y Traducción")
        seq = st.text_input("ADN molde (3'-5'):", value=st.session_state.secuencia_maestra)
        st.session_state.secuencia_maestra = seq.upper().replace(" ", "")
        if st.session_state.secuencia_maestra:
            arn = adn_a_arn(st.session_state.secuencia_maestra)
            st.success(f"ARNm completo: {arn}")
            aa = [codones.get(arn[i:i+3], f"({arn[i:i+3]})") for i in range(0, len(arn), 3)]
            st.write(f"**Proteína:** {' - '.join(aa)}")
            st.info("Resultado: Traducción finalizada con éxito.")

    elif st.session_state.sim_actual == "2. Mutaciones y Estructura Proteica":
        st.header("2. Impacto de Mutaciones")
        arn_base = adn_a_arn(st.session_state.secuencia_maestra)
        pos = st.slider("Posición en ARNm:", 0, len(arn_base)-1, 0)
        nuc = st.selectbox("Cambiar a:", ["A", "U", "C", "G"])
        mut = list(arn_base); mut[pos] = nuc; mut_arn = "".join(mut)
        st.warning(f"ARNm Mutado: `{mut_arn}`")
        aa_orig = [codones.get(arn_base[i:i+3], "?") for i in range(0, len(arn_base), 3)]
        aa_mut = [codones.get(mut_arn[i:i+3], "?") for i in range(0, len(mut_arn), 3)]
        st.write(f"**Comparativa Proteica:**")
        st.write(f"Original: {aa_orig}")
        st.write(f"Mutado:   {aa_mut}")
        if aa_orig != aa_mut: st.error("Resultado: La mutación alteró la estructura proteica.")

    elif st.session_state.sim_actual == "3. Matriz de Alineamiento Global":
        st.header("3. Matriz de Alineamiento")
        seq = st.session_state.secuencia_maestra
        st.table([[""] + list(seq)] + [[seq[i]] + [5 if seq[i]==seq[j] else -2 for j in range(len(seq))] for i in range(len(seq))])
        st.success(f"Resultado: Matriz de identidad de {len(seq)}x{len(seq)} generada.")

    elif st.session_state.sim_actual == "4. Gráficos de De Bruijn (Ensamble)":
        st.header("4. Ensamble de ADN")
        k = st.slider("Tamaño de k-mer:", 2, 5, 3)
        kmers = [st.session_state.secuencia_maestra[i:i+k] for i in range(len(st.session_state.secuencia_maestra) - k + 1)]
        st.write(f"Fragmentos obtenidos: `{list(set(kmers))}`")
        st.success(f"Resultado: Se ensamblaron {len(set(kmers))} fragmentos únicos.")

    elif st.session_state.sim_actual == "5. Distancia Filogenética Básica":
        st.header("5. Distancia Evolutiva")
        ref = "ATGCATGCATGCATGCATGC"
        dist = sum(1 for a,b in zip(st.session_state.secuencia_maestra, ref) if a != b) / len(st.session_state.secuencia_maestra)
        st.metric("Distancia Genética", f"{dist:.2%}")
        st.info("Resultado: Distancia calculada respecto a secuencia de referencia.")

    # --- NAVEGACIÓN INFERIOR ---
    st.divider()
    c1, c2 = st.columns(2)
    with c1: 
        if st.button("⬅️ Atrás"): navegar("atras"); st.rerun()
    with c2: 
        if st.button("Siguiente ➡️"): navegar("siguiente"); st.rerun()
else:
    st.warning("⚠️ Identifícate para comenzar tu práctica de bioinformática.")
