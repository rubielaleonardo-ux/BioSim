import streamlit as st

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="BioSim Pro: Lab Bioinformático", layout="wide")

if 'paso_actual' not in st.session_state: st.session_state.paso_actual = "1. Transcripción y Traducción"
if 'secuencia_maestra' not in st.session_state: st.session_state.secuencia_maestra = ""

pasos = ["1. Transcripción y Traducción", "2. Mutaciones y Estructura Proteica", "3. Matriz de Alineamiento Global", "4. Gráficos de De Bruijn (Ensamble)", "5. Distancia Filogenética Básica"]

def adn_a_arn(adn): return "".join([{"A":"U","T":"A","C":"G","G":"C"}.get(b, "") for b in adn.upper()])

codones = {'UUU':'Fenilalanina','UUC':'Fenilalanina','AUG':'Metionina','UAA':'STOP','UAG':'STOP','UGA':'STOP'} # Simplificado para espacio

# --- INTERFAZ ---
st.title("🧬 BioSim Pro: Entorno de Análisis Genómico")

with st.expander("👤 Perfil de Usuario"):
    nombre = st.text_input("Investigador:")
    nivel = st.selectbox("Institución:", ["Secundaria", "Universidad"])

if nombre and nivel:
    st.sidebar.title("Módulos de Análisis")
    st.session_state.paso_actual = st.sidebar.radio("Selecciona:", pasos)
    
    # --- SIMULADOR 1: TRANSCRIPICCIÓN ---
    if st.session_state.paso_actual == "1. Transcripción y Traducción":
        st.header("Módulo 1: Expresión Génica")
        seq = st.text_input("Ingrese secuencia ADN molde (3'-5'):", value=st.session_state.secuencia_maestra)
        st.session_state.secuencia_maestra = seq.upper().replace(" ", "")
        if st.button("Ejecutar Transcripción"):
            arn = adn_a_arn(st.session_state.secuencia_maestra)
            st.code(f"Resultado ARNm: {arn}", language='python')
            st.write("Interpretación: El ARNm es la secuencia complementaria. El proceso de transcripción es esencial para preparar la información para el ribosoma.")

    # --- SIMULADOR 2: MUTACIONES ---
    elif st.session_state.paso_actual == "2. Mutaciones y Estructura Proteica":
        st.header("Módulo 2: Editor de Mutagénesis")
        arn = adn_a_arn(st.session_state.secuencia_maestra)
        pos = st.slider("Seleccione locus a mutar:", 0, len(arn)-1)
        nuc = st.selectbox("Nucleótido de reemplazo:", ["A", "U", "C", "G"])
        if st.button("Aplicar Mutación"):
            mut = list(arn); mut[pos] = nuc; mut_arn = "".join(mut)
            st.warning(f"Mutación detectada en posición {pos}. ARNm modificado: {mut_arn}")
            st.write(f"Impacto: Un cambio en el ARNm puede alterar el codón. Si el nuevo codón es {mut_arn[pos:pos+3]}, el aminoácido resultante cambia, afectando el plegamiento proteico.")

    # --- SIMULADOR 3: ALINEAMIENTO ---
    elif st.session_state.paso_actual == "3. Matriz de Alineamiento Global":
        st.header("Módulo 3: Motor de Alineamiento (Smith-Waterman)")
        s1 = st.session_state.secuencia_maestra
        if st.button("Generar Matriz de Puntuación"):
            matriz = [[5 if c1==c2 else -1 for c1 in list(s1)] for c2 in list("ATGC")]
            st.table(matriz)
            st.write("Interpretación: Los valores positivos (+5) indican regiones conservadas evolutivamente, vitales para la función biológica.")

    # --- SIMULADOR 4: DE BRUIJN ---
    elif st.session_state.paso_actual == "4. Gráficos de De Bruijn (Ensamble)":
        st.header("Módulo 4: Ensamble de Genoma De Bruijn")
        k = st.number_input("Tamaño k-mer:", 2, 5, 3)
        if st.button("Ejecutar Ensamble"):
            kmers = [st.session_state.secuencia_maestra[i:i+k] for i in range(len(st.session_state.secuencia_maestra)-k+1)]
            st.write(f"Nodos generados: {kmers}")
            st.write("Interpretación: Cada nodo representa un overlap. Un grafo complejo indica alta repetición en el genoma, difícil de ensamblar.")

    # --- SIMULADOR 5: FILOGENIA ---
    elif st.session_state.paso_actual == "5. Distancia Filogenética Básica":
        st.header("Módulo 5: Calculadora de Distancia Evolutiva")
        s2 = st.text_input("Ingrese secuencia de especie comparativa:")
        if st.button("Calcular Distancia p"):
            dist = sum(1 for a,b in zip(st.session_state.secuencia_maestra, s2) if a != b) / len(st.session_state.secuencia_maestra)
            st.metric("Distancia Evolutiva (p-distance)", f"{dist:.2%}")
            st.write("Interpretación: Una distancia < 5% sugiere una divergencia reciente. Distancias mayores implican procesos evolutivos más largos.")

    # --- PISTAS GLOBALES ---
    with st.sidebar:
        st.divider()
        if st.button("💡 Obtener Pista de Análisis"):
            st.info("Tip Bioinformático: Siempre verifique que la longitud de las secuencias sea múltiplo de 3 para una traducción correcta.")

else:
    st.warning("⚠️ Acceso restringido. Por favor, identifíquese.")
