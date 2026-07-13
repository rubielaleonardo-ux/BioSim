import streamlit as st
import pandas as pd

# Configuración inicial
st.set_page_config(page_title="BioSim: Simuladores Educativos", layout="wide")

# --- BIENVENIDA Y PRESENTACIÓN ---
st.title("🧬 BioSim: Simuladores Bioinformáticos Educativos")
st.write("""
¡Bienvenido al portal de simulación bioinformática! 
La bioinformática es la herramienta que nos permite comprender el lenguaje de la vida. 
A través de estos simuladores, exploraremos procesos desde la transcripción del ADN 
hasta la reconstrucción de genomas y el análisis evolutivo de las especies.
""")

st.write("---")

# --- PANEL DE INSTRUCCIONES E IDENTIFICACIÓN ---
with st.expander("👋 ¡Haz clic aquí para ver las instrucciones e identificarte!", expanded=True):
    st.write("### Instrucciones:")
    st.write("1. Escribe tu nombre y selecciona tu nivel escolar.")
    st.write("2. Una vez registrado, selecciona un simulador en el menú de la izquierda.")
    st.write("3. Realiza la actividad y registra tus resultados.")
    st.write("---")
    
    nombre_estudiante = st.text_input("Nombre del Estudiante:", value="", key="nombre_input")
    grado_escolar = st.selectbox("Nivel Escolar:", ["", "1ro Secundaria", "2do Secundaria", "3ro Secundaria", "4to Secundaria", "5to Secundaria", "6to Secundaria", "Universidad"], key="grado_input")

    if nombre_estudiante and grado_escolar:
        st.success(f"¡Hola {nombre_estudiante} de {grado_escolar}, estamos listos para comenzar!")
    else:
        st.info("⚠️ Por favor, ingresa tu nombre y grado para habilitar los simuladores.")

st.write("---")

# --- LÓGICA DE ACCESO (Solo se muestra si se registró) ---
if nombre_estudiante and grado_escolar:
    
    # --- MENÚ LATERAL ---
    simulador = st.sidebar.selectbox(
        "Selecciona un Simulador:",
        [
            "1. Transcripción y Traducción",
            "2. Mutaciones y Estructura Proteica",
            "3. Matriz de Alineamiento Global",
            "4. Gráficos de De Bruijn (Ensamble)",
            "5. Distancia Filogenética Básica"
        ]
    )

    # --- SIMULADOR 1 ---
    if simulador == "1. Transcripción y Traducción":
        st.header("1. Simulador de Expresión Génica")
        st.info("💡 **Instrucciones:** Ingresa la secuencia de ADN (molde) para obtener el ARN y la cadena polipeptídica resultante.")
        adn = st.text_input("Ingresa una secuencia de ADN (Molde, 3' a 5'):", "TACGGCATTTATACT").upper()
        
        if not all(c in "ATCG" for c in adn):
            st.error("⚠️ La secuencia solo debe contener A, T, C y G.")
        else:
            transcripcion = {"A": "U", "T": "A", "C": "G", "G": "C"}
            arnm = "".join([transcripcion[base] for base in adn])
            st.success(f"**ARN mensajero (5' a 3'):** {arnm}")
            
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
            aminoacidos = []
            for i in range(0, len(arnm) - (len(arnm) % 3), 3):
                codon = arnm[i:i+3]
                aa = codigo_genetico.get(codon, "Desconocido")
                aminoacidos.append(aa)
                st.info(f"Codón **{codon}** ➡️ Aminoácido: **{aa}**")
            st.metric(label="Cadena Polipeptídica", value=" - ".join(aminoacidos))

    # --- SIMULADOR 2 ---
    elif simulador == "2. Mutaciones y Estructura Proteica":
        st.header("2. Impacto de Mutaciones Puntuales")
        st.info("💡 **Instrucciones:** Mueve el selector para cambiar un nucleótido y observa si la mutación es silenciosa, missense o nonsense.")
        secuencia_base = "AUGGGCACUUAA"
        st.write(f"**ARNm Original:** `{secuencia_base}`")
        posicion = st.slider("Posición para mutar (0 a 11):", 0, 11, 4)
        nuevo_nucleotido = st.selectbox("Nuevo nucleótido:", ["A", "U", "C", "G"])
        lista_arn = list(secuencia_base)
        lista_arn[posicion] = nuevo_nucleotido
        secuencia_mutada = "".join(lista_arn)
        st.warning(f"**Secuencia Mutada:** {secuencia_mutada}")
        
        def traducir_codon(c):
            codigo = {'AUG': 'Metionina', 'GGC': 'Glicina', 'GUA': 'Valina', 'ACU': 'Treonina', 'UAA': 'STOP', 'CAC': 'Histidina', 'GAC': 'Ácido Aspártico', 'GAA': 'Ácido Glutámico', 'GCU': 'Alanina'}
            return codigo.get(c, "Desconocido")
        
        codon_original = secuencia_base[3:6]
        codon_mutado = secuencia_mutada[3:6]
        st.write(f"Comparación: Original: **{codon_original}** vs Mutado: **{codon_mutado}**")
        if codon_original != codon_mutado:
            if "STOP" in traducir_codon(codon_mutado): st.error("🚨 ¡Mutación Nonsense!")
            else: st.info("🧬 ¡Mutación Missense!")
        else: st.success("✅ Mutación Silenciosa")

    # --- SIMULADOR 3 ---
    elif simulador == "3. Matriz de Alineamiento Global":
        st.header("3. Construcción de Matrices")
        st.info("💡 **Instrucciones:** Ingresa dos secuencias para calcular su matriz de puntuación.")
        seq1 = st.text_input("Secuencia Horizontal:", "AAGC").upper().strip()
        seq2 = st.text_input("Secuencia Vertical:", "AGC").upper().strip()
        if seq1 and seq2:
            cabecera = [""] + ["-"] + list(seq1)
            matriz_final = [cabecera]
            for i, char2 in enumerate(["-"] + list(seq2)):
                fila = [char2]
                for char1 in ["-"] + list(seq1):
                    valor = 5 if char1 == char2 else (-1 if char1 == "-" or char2 == "-" else -2)
                    fila.append(valor)
                matriz_final.append(fila)
            st.table(matriz_final)

    # --- SIMULADOR 4 ---
    elif simulador == "4. Gráficos de De Bruijn (Ensamble)":
        st.header("4. Ensamble mediante Grafos")
        st.info("💡 **Instrucciones:** Divide una secuencia en fragmentos de tamaño 'k' y observa sus conexiones.")
        secuencia = st.text_input("Ingresa ADN:", "ATGCATGC").upper().strip()
        k = st.slider("Tamaño k:", 2, 4, 3)
        if secuencia and len(secuencia) >= k:
            kmeros = [secuencia[i:i+k] for i in range(len(secuencia) - k + 1)]
            st.write(f"**Fragmentos:** `{kmeros}`")
            for km in kmeros:
                st.write(f"Nodo `{km[:-1]}` ➔ Nodo `{km[1:]}`")

    # --- SIMULADOR 5 ---
    elif simulador == "5. Distancia Filogenética Básica":
        st.header("5. Distancia Filogenética")
        st.info("💡 **Instrucciones:** Compara dos especies para ver qué tan relacionadas están.")
        col1, col2 = st.columns(2)
        with col1:
            sp1 = st.text_input("Especie 1:", "Homo sapiens")
            s1 = st.text_input("Secuencia 1:", "ATGCATGC").upper()
        with col2:
            sp2 = st.text_input("Especie 2:", "Pan troglodytes")
            s2 = st.text_input("Secuencia 2:", "ATGCGTGC").upper()
        if s1 and s2 and len(s1) == len(s2):
            diff = sum(1 for a, b in zip(s1, s2) if a != b)
            st.write(f"Distancia: {(diff / len(s1)) * 100:.2f}%")
