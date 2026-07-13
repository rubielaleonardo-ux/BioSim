import streamlit as st
import pandas as pd

# Configuración inicial
st.set_page_config(page_title="BioSim: Simuladores Educativos", layout="wide")

st.title("🧬 BioSim: Simuladores Bioinformáticos Educativos")

# --- PANEL DE INSTRUCCIONES E IDENTIFICACIÓN ---
with st.expander("👋 ¡Bienvenido! Haz clic aquí para ver las instrucciones e identificarte"):
    st.write("### Instrucciones:")
    st.write("1. Escribe tu nombre y selecciona tu grado escolar.")
    st.write("2. Selecciona un simulador en el menú de la izquierda.")
    st.write("3. Realiza la actividad y registra tus resultados.")
    
    st.write("---")
    
    # Campos que aparecerán vacíos cada vez que recarguen
    nombre_estudiante = st.text_input("Nombre del Estudiante:", value="")
    grado_escolar = st.selectbox("Nivel Escolar:", ["", "1ro Secundaria", "2do Secundaria", "3ro Secundaria", "4to Secundaria", "5to Secundaria", "6to Secundaria"])

    if nombre_estudiante and grado_escolar:
        st.success(f"¡Hola {nombre_estudiante} de {grado_escolar}, estamos listos para comenzar!")
st.write("---")
# -------------------------------------------------------------------------
# SIMULADOR 1: Transcripción y Traducción (Corregido)
# -------------------------------------------------------------------------
if simulador == "1. Transcripción y Traducción":
    st.header("1. Simulador de Expresión Génica")
    adn = st.text_input("Ingresa una secuencia de ADN (Molde, 3' a 5'):", "TACGGCATTTATACT").upper()
    
    if not all(c in "ATCG" for c in adn):
        st.error("⚠️ La secuencia solo debe contener A, T, C y G.")
    else:
        # Transcripción limpia: A->U, T->A, C->G, G->C
        transcripcion = {"A": "U", "T": "A", "C": "G", "G": "C"}
        arnm = "".join([transcripcion[base] for base in adn])
        st.success(f"**ARN mensajero (5' a 3'):** {arnm}")
        
      # Diccionario de traducción con nombres completos
        codigo_genetico = {
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
        st.write("**Paso a paso de la Traducción:**")
        aminoacidos = []
        if len(arnm) % 3 != 0:
            st.warning(f"⚠️ Atención: Tu secuencia de ARN tiene {len(arnm)} nucleótidos. Los últimos {len(arnm) % 3} no forman un codón completo y serán ignorados.")
        
        for i in range(0, len(arnm) - (len(arnm) % 3), 3):
            codon = arnm[i:i+3]
            aa = codigo_genetico.get(codon, "Desconocido")
            aminoacidos.append(aa)
            st.info(f"Codón **{codon}** ➡️ Aminoácido: **{aa}**")
        
        st.metric(label="Cadena Polipeptídica", value=" - ".join(aminoacidos))
# -------------------------------------------------------------------------
# El resto de tus simuladores (2 al 5) funcionan bien tal como los tenías.
# Puedes simplemente reemplazar la sección 1 en tu archivo con este código.
# -------------------------------------------------------------------------
# -------------------------------------------------------------------------
# SIMULADOR 2: Mutaciones y Estructura Proteica
# -------------------------------------------------------------------------
# -------------------------------------------------------------------------
# SIMULADOR 2: Mutaciones y Estructura Proteica (Actualizado)
# -------------------------------------------------------------------------
elif simulador == "2. Mutaciones y Estructura Proteica":
    st.header("2. Impacto de Mutaciones Puntuales")
    st.write("Modifica un nucleótido y observa cómo cambia el aminoácido resultante.")
    
    secuencia_base = "AUGGGCACUUAA"
    st.write(f"**ARNm Original:** `{secuencia_base}`")
    
    posicion = st.slider("Selecciona la posición para mutar (0 a 11):", 0, 11, 4)
    nuevo_nucleotido = st.selectbox("Selecciona el nuevo nucleótido:", ["A", "U", "C", "G"])
    
    lista_arn = list(secuencia_base)
    lista_arn[posicion] = nuevo_nucleotido
    secuencia_mutada = "".join(lista_arn)
    
    st.warning(f"**Secuencia Mutada:** {secuencia_mutada}")
    
    # Esta es la lista que tienes que actualizar
    def traducir_codon(c):
        codigo = {
            'AUG': 'Metionina', 'GGC': 'Glicina', 'GUA': 'Valina', 
            'ACU': 'Treonina', 'UAA': 'STOP', 'CAC': 'Histidina',
            'GAC': 'Ácido Aspártico', 'GAA': 'Ácido Glutámico', 'GCU': 'Alanina'
        }
        return codigo.get(c, "Desconocido")

    codon_original = secuencia_base[3:6]
    codon_mutado = secuencia_mutada[3:6]
    
    st.write("---")
    st.write(f"Comparación del codón en posición 3-5:")
    st.write(f"Original: **{codon_original}** ({traducir_codon(codon_original)})")
    st.write(f"Mutado: **{codon_mutado}** ({traducir_codon(codon_mutado)})")
    
    if codon_original != codon_mutado:
        if "STOP" in traducir_codon(codon_mutado):
            st.error("🚨 ¡Mutación Nonsense! Se creó un codón de parada prematuro.")
        else:
            st.info("🧬 ¡Mutación Missense! El aminoácido cambió. Esto altera la estructura de la proteína.")
    else:
        st.success("✅ Mutación Silenciosa: El aminoácido no cambió.")
# -------------------------------------------------------------------------
# SIMULADOR 3: Matriz de Alineamiento Global (Versión a Prueba de Errores)
# -------------------------------------------------------------------------
elif simulador == "3. Matriz de Alineamiento Global":
    st.header("3. Construcción de Matrices de Puntuación")
    seq1 = st.text_input("Secuencia Horizontal:", "AAGC").upper().strip()
    seq2 = st.text_input("Secuencia Vertical:", "AGC").upper().strip()
    
    if seq1 and seq2:
        # Creamos una lista de listas para los datos, sin índices complejos
        # Añadimos cabeceras como primera fila
        cabecera = [""] + ["-"] + list(seq1)
        matriz_final = [cabecera]
        
        seq1_list = ["-"] + list(seq1)
        seq2_list = ["-"] + list(seq2)
        
        for i, char2 in enumerate(seq2_list):
            fila = [char2] # El primer elemento es la letra de la fila
            for char1 in seq1_list:
                if char1 == char2: valor = 5
                elif char1 == "-" or char2 == "-": valor = -1
                else: valor = -2
                fila.append(valor)
            matriz_final.append(fila)
        
        # Mostramos como tabla simple sin forzar conversión a DataFrame de Pandas
        st.write("**Matriz de puntuación:**")
        st.table(matriz_final) 
        st.caption("💡 Match=5, Mismatch=-2, Gap=-1.")
    else:
        st.info("Ingresa ambas secuencias.")
# -------------------------------------------------------------------------
# SIMULADOR 4: Ensamble de Fragmentos (K-meros)
# -------------------------------------------------------------------------
elif simulador == "4. Gráficos de De Bruijn (Ensamble)":
    st.header("4. Ensamble mediante Grafos de De Bruijn")
    st.write("Entiende cómo se reconstruye el genoma uniendo fragmentos (k-meros).")
    
    secuencia = st.text_input("Ingresa la secuencia de ADN:", "ATGCATGC").upper().strip()
    k = st.slider("Tamaño del fragmento (k):", 2, 4, 3)
    
    if secuencia and len(secuencia) >= k:
        # Generar k-meros
        kmeros = [secuencia[i:i+k] for i in range(len(secuencia) - k + 1)]
        st.write(f"**Fragmentos (k={k}):** `{kmeros}`")
        
        # Construcción básica del Grafo de De Bruijn
        # Un nodo es (k-1)-mer, una arista es un k-mer
        nodos = set()
        aristas = []
        for km in kmeros:
            prefijo = km[:-1]
            sufijo = km[1:]
            nodos.add(prefijo)
            nodos.add(sufijo)
            aristas.append((prefijo, sufijo))
            
        st.write("---")
        st.subheader("Grafo de De Bruijn simplificado:")
        st.write("El ensamble consiste en encontrar un camino que recorra todas las conexiones.")
        
        # Mostrar conexiones (nodos y aristas)
        for origen, destino in aristas:
            st.write(f"Nodo `{origen}` ➔ Nodo `{destino}` (vía fragmento `{origen}{destino[-1]}`)")
            
        st.info("💡 En la bioinformática real, el ensamble busca el 'camino euleriano' para reconstruir la secuencia completa.")
    else:
        st.warning("Ingresa una secuencia válida (mínimo longitud de k).")
# -------------------------------------------------------------------------
# SIMULADOR 5: Distancia Filogenética Básica (UPGMA)
# -------------------------------------------------------------------------
elif simulador == "5. Distancia Filogenética Básica":
    st.header("5. Distancia Filogenética")
    st.write("Compara secuencias de dos especies para medir su distancia evolutiva.")
    
    # Nueva entrada para nombres de especies
    col1, col2 = st.columns(2)
    with col1:
        sp1 = st.text_input("Nombre Especie 1:", "Homo sapiens")
        seq_org1 = st.text_input("Secuencia Especie 1:", "ATGCATGC").upper().strip()
    with col2:
        sp2 = st.text_input("Nombre Especie 2:", "Pan troglodytes")
        seq_org2 = st.text_input("Secuencia Especie 2:", "ATGCGTGC").upper().strip()
    
    if seq_org1 and seq_org2:
        if len(seq_org1) != len(seq_org2):
            st.error("⚠️ Error: Las secuencias deben tener la misma longitud para compararse.")
        elif not (all(c in "ATCG" for c in seq_org1) and all(c in "ATCG" for c in seq_org2)):
            st.error("⚠️ Error: Solo se permiten nucleótidos A, T, C y G.")
        else:
            # Cálculo de distancia
            diferencias = sum(1 for a, b in zip(seq_org1, seq_org2) if a != b)
            distancia_relativa = (diferencias / len(seq_org1)) * 100
            
            st.write("---")
            st.write(f"### Comparación: {sp1} vs {sp2}")
            st.write(f"**Diferencias detectadas:** {diferencias} nucleótidos distintos.")
            st.write(f"**Distancia evolutiva:** {distancia_relativa:.2f}%")
            
            # Mapa visual
            comparacion = "".join([a if a == b else f"**{b}**" for a, b in zip(seq_org1, seq_org2)])
            st.write("**Mapa de variabilidad (las diferencias están en negrita):**")
            st.code(comparacion, language="python")
            
            # Conclusión pedagógica
            if distancia_relativa == 0:
                st.success(f"✅ Las secuencias de {sp1} y {sp2} son idénticas.")
            elif distancia_relativa < 20:
                st.info(f"🧬 {sp1} y {sp2} muestran una relación evolutiva cercana.")
            else:
                st.warning(f"⚠️ {sp1} y {sp2} son evolutivamente distantes.")
    else:
        st.info("Ingresa los nombres y las secuencias de ambas especies para comenzar.")
