import streamlit as st

# --- 1. MEMORIA CENTRAL (Datos guardados) ---
DATOS = {
    "codigo_genetico": {
        'UUU': 'Fenilalanina', 'UUC': 'Fenilalanina', 'UUA': 'Leucina', 'UUG': 'Leucina', 
        'UCU': 'Serina', 'UCC': 'Serina', 'UCA': 'Serina', 'UCG': 'Serina',
        'UAU': 'Tirosina', 'UAC': 'Tirosina', 'UAA': 'STOP (Final)', 'UAG': 'STOP (Final)', 
        'UGU': 'Cisteína', 'UGC': 'Cisteína', 'UGA': 'STOP (Final)', 'UGG': 'Triptófano',
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
}

# --- 2. CONFIGURACIÓN ---
st.set_page_config(page_title="BioSim", layout="wide")
st.title("🧬 BioSim: Simuladores Bioinformáticos")

# --- 3. IDENTIFICACIÓN ---
with st.expander("👋 ¡Identifícate para comenzar!", expanded=True):
    nombre = st.text_input("Nombre del Estudiante:", value="")
    nivel = st.selectbox("Nivel Escolar:", ["", "1ro Secundaria", "2do Secundaria", "3ro Secundaria", "4to Secundaria", "5to Secundaria", "6to Secundaria", "Universidad"])

if nombre and nivel:
    # --- 4. MENÚ LATERAL ---
    opcion = st.sidebar.selectbox("Selecciona un Simulador:", [
        "1. Transcripción y Traducción",
        "2. Mutaciones y Estructura Proteica",
        "3. Matriz de Alineamiento Global",
        "4. Gráficos de De Bruijn (Ensamble)",
        "5. Distancia Filogenética Básica"
    ])

    # --- SIMULADOR 1 ---
    if opcion == "1. Transcripción y Traducción":
        st.header("1. Simulador de Expresión Génica")
        adn = st.text_input("Ingresa ADN (3' a 5'):", "TACGGCATTTATACT").upper()
        if all(c in "ATCG" for c in adn):
            transcripcion = {"A": "U", "T": "A", "C": "G", "G": "C"}
            arnm = "".join([transcripcion[b] for b in adn])
            st.success(f"**ARN mensajero:** {arnm}")
            aa = [DATOS["codigo_genetico"].get(arnm[i:i+3], "Desconocido") for i in range(0, len(arnm)-2, 3)]
            st.metric("Cadena Polipeptídica", " - ".join(aa))
        else: st.error("⚠️ Solo A, T, C, G")

    # --- SIMULADOR 2 ---
    elif opcion == "2. Mutaciones y Estructura Proteica":
        st.header("2. Impacto de Mutaciones")
        seq = "AUGGGCACUUAA"
        pos = st.slider("Posición (0-11):", 0, 11, 4)
        nuc = st.selectbox("Nuevo nucleótido:", ["A", "U", "C", "G"])
        seq_m = list(seq); seq_m[pos] = nuc; seq_m = "".join(seq_m)
        st.warning(f"Mutada: {seq_m}")
        st.write(f"Comparación: {seq[3:6]} -> {seq_m[3:6]}")

    # --- SIMULADOR 3 ---
    elif opcion == "3. Matriz de Alineamiento Global":
        st.header("3. Matriz de Alineamiento")
        s1 = st.text_input("Secuencia H:", "AAGC").upper()
        s2 = st.text_input("Secuencia V:", "AGC").upper()
        if s1 and s2:
            st.write("Matriz calculada...")
            # Aquí tu lógica de matriz

    # --- SIMULADOR 4 ---
    elif opcion == "4. Gráficos de De Bruijn (Ensamble)":
        st.header("4. Ensamble de Genomas")
        seq = st.text_input("Secuencia:", "ATGCATGC").upper()
        k = st.slider("k-mer:", 2, 4, 3)
        if seq: st.write([seq[i:i+k] for i in range(len(seq)-k+1)])

    # --- SIMULADOR 5 ---
    elif opcion == "5. Distancia Filogenética Básica":
        st.header("5. Distancia Filogenética")
        s1 = st.text_input("Secuencia 1:", "ATGC").upper()
        s2 = st.text_input("Secuencia 2:", "ATGG").upper()
        if s1 and s2: st.write(f"Distancia: {sum(1 for a,b in zip(s1,s2) if a!=b)} cambios.")

else:
    st.info("⚠️ Ingresa tu nombre y nivel para habilitar los simuladores.")
