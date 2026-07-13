import streamlit as st

# --- 1. MEMORIA CENTRAL: La base de datos "a prueba de errores" ---
DATOS = {
    "codigo_genetico": {
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
}

# --- 2. CONFIGURACIÓN E INTERFAZ ---
st.set_page_config(page_title="BioSim", layout="wide")
st.title("🧬 BioSim: Simuladores Bioinformáticos")

with st.expander("👋 ¡Identifícate para comenzar!", expanded=True):
    nombre = st.text_input("Nombre:", value="", key="nombre")
    nivel = st.selectbox("Nivel:", ["", "1ro Secundaria", "2do Secundaria", "3ro Secundaria", "4to Secundaria", "5to Secundaria", "6to Secundaria", "Universidad"], key="nivel")

if nombre and nivel:
    st.sidebar.title("Menú de Actividades")
    opcion = st.sidebar.selectbox("Elige un Simulador:", [
        "1. Transcripción y Traducción",
        "2. Mutaciones",
        "3. Matriz de Alineamiento",
        "4. Ensamble de Genomas",
        "5. Distancia Filogenética"
    ])

    # --- 3. LÓGICA DE SIMULADORES (Ya contiene toda la info guardada) ---
    
    if opcion == "1. Transcripción y Traducción":
        st.header("1. Transcripción y Traducción")
        adn = st.text_input("Ingresa ADN (3' a 5'):", "TACGGCATTTATACT").upper()
        if all(c in "ATCG" for c in adn):
            trans = {"A": "U", "T": "A", "C": "G", "G": "C"}
            arn = "".join([trans[b] for b in adn])
            st.success(f"ARN: {arn}")
            aa = [DATOS["codigo_genetico"].get(arn[i:i+3], "??") for i in range(0, len(arn)-2, 3)]
            st.write(f"Proteína: {' - '.join(aa)}")
        else: st.warning("Usa solo A, T, C, G")

    elif opcion == "2. Mutaciones":
        st.header("2. Mutaciones")
        st.info("Simulador de mutaciones cargado.")
        # Aquí puedes añadir tu lógica de mutaciones...

    # ... (Puedes añadir los bloques 3, 4 y 5 siguiendo este mismo estilo)

else:
    st.info("⚠️ Ingresa nombre y nivel para continuar.")
