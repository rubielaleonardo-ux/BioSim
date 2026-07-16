import streamlit as st

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="BioSim: Laboratorio Virtual", layout="wide")

# --- ESTADO INICIAL ---
if 'sim_actual' not in st.session_state: 
    st.session_state.sim_actual = "1. Transcripción y Traducción"

# --- DICCIONARIO DE CODONES ---
codones = {'UUU':'Fenilalanina','UUC':'Fenilalanina','UUA':'Leucina','UUG':'Leucina','UCU':'Serina','UCC':'Serina','UCA':'Serina','UCG':'Serina','UAU':'Tirosina','UAC':'Tirosina','UAA':'STOP','UAG':'STOP','UGU':'Cisteína','UGC':'Cisteína','UGA':'STOP','UGG':'Triptófano','CUU':'Leucina','CUC':'Leucina','CUA':'Leucina','CUG':'Leucina','CCU':'Prolina','CCC':'Prolina','CCA':'Prolina','CCG':'Prolina','CAU':'Histidina','CAC':'Histidina','CAA':'Glutamina','CAG':'Glutamina','CGU':'Arginina','CGC':'Arginina','CGA':'Arginina','CGG':'Arginina','AUU':'Isoleucina','AUC':'Isoleucina','AUA':'Isoleucina','AUG':'Metionina','ACU':'Treonina','ACC':'Treonina','ACA':'Treonina','ACG':'Treonina','AAU':'Asparagina','AAC':'Asparagina','AAA':'Lisina','AAG':'Lisina','AGU':'Serina','AGC':'Serina','AGA':'Arginina','AGG':'Arginina','GUU':'Valina','GUC':'Valina','GUA':'Valina','GUG':'Valina','GCU':'Alanina','GCC':'Alanina','GCA':'Alanina','GCG':'Alanina','GAU':'Ácido Aspártico','GAC':'Ácido Aspártico','GAA':'Ácido Glutámico','GAG':'Ácido Glutámico','GGU':'Glicina','GGC':'Glicina','GGA':'Glicina','GGG':'Glicina'}

simuladores = ["1. Transcripción y Traducción", "2. Mutaciones y Estructura Proteica", "3. Matriz de Alineamiento Global", "4. Gráficos de De Bruijn (Ensamble)", "5. Distancia Filogenética Básica"]

# --- LÓGICA ---
def adn_a_arn(adn):
    trans = {"A": "U", "T": "A", "C": "G", "G": "C"}
    return "".join([trans.get(b, "") for b in adn.upper()])

def calcular_distancia_hamming(seq1, seq2):
    if len(seq1) != len(seq2): return None
    return sum(1 for a, b in zip(seq1, seq2) if a != b)

# --- INTERFAZ ---
st.title("🧬 BioSim: Laboratorio Virtual")

with st.expander("👋 ¡Identifícate para comenzar!"):
    nombre = st.text_input("Nombre del Estudiante:")
    nivel = st.selectbox("Nivel Escolar:", ["", "Secundaria", "Universidad"])

if nombre and nivel:
    st.sidebar.title("Navegación")
    st.session_state.sim_actual = st.sidebar.radio("Selecciona módulo:", simuladores)
    st.sidebar.divider()
    
    # --- BOTONES DE NAVEGACIÓN SUPERIORES ---
    c1, c2 = st.columns(2)
    idx = simuladores.index(st.session_state.sim_actual)
    
    if c1.button("⬅️ Atrás") and idx > 0:
        st.session_state.sim_actual = simuladores[idx - 1]
        st.rerun()
    if c2.button("Siguiente ➡️") and idx < len(simuladores) - 1:
        st.session_state.sim_actual = simuladores[idx + 1]
        st.rerun()

    # --- CONTENIDO DEL MÓDULO ---
    st.header(st.session_state.sim_actual)
    seq_input = st.text_input("Introduce secuencia de ADN:", "ATGGCCCTGTGGATGCGCCT")
    seq = seq_input.upper().replace(" ", "")

    if st.session_state.sim_actual == "1. Transcripción y Traducción":
        arn = adn_a_arn(seq)
        aa = [codones.get(arn[i:i+3], f"({arn[i:i+3]})") for i in range(0, len(arn), 3)]
        st.subheader("📊 Informe de Resultados")
        st.success(f"ARNm completo: {arn}")
        st.write(f"**Proteína:** {' - '.join(aa)}")

    elif st.session_state.sim_actual == "2. Mutaciones y Estructura Proteica":
        arn_base = adn_a_arn(seq)
        pos = st.slider("Posición en ARNm:", 0, max(0, len(arn_base)-1), 0)
        nuc = st.selectbox("Cambiar a:", ["A", "U", "C", "G"])
        mut_arn = "".join([nuc if i == pos else b for i, b in enumerate(arn_base)])
        st.subheader("📊 Informe de Resultados")
        st.write(f"Original: `{arn_base}` | Mutado: `{mut_arn}`")

    elif st.session_state.sim_actual == "3. Matriz de Alineamiento Global":
        st.subheader("📊 Informe de Resultados")
        st.table([[""] + list(seq)] + [[seq[i]] + [5 if seq[i]==seq[j] else -2 for j in range(len(seq))] for i in range(len(seq))])

    elif st.session_state.sim_actual == "4. Gráficos de De Bruijn (Ensamble)":
        k = st.slider("Tamaño de k-mer:", 2, 5, 3)
        kmers = set([seq[i:i+k] for i in range(max(0, len(seq) - k + 1))])
        st.subheader("📊 Informe de Resultados")
        st.metric("Total de fragmentos únicos", len(kmers))
        st.write(f"Fragmentos: `{list(kmers)}`")

    elif st.session_state.sim_actual == "5. Distancia Filogenética Básica":
        seq2 = st.text_input("Introduce segunda secuencia:", "ATGCATGG")
        if st.button("Calcular Distancia"):
            dist = calcular_distancia_hamming(seq, seq2)
            st.subheader("📊 Informe de Resultados")
            if dist is not None:
                st.metric("Distancia de Hamming", dist)
            else:
                st.error("Error: Las secuencias deben tener la misma longitud.")

else:
    st.warning("⚠️ Identifícate para comenzar.")
