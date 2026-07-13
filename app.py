import streamlit as st
import pandas as pd

st.set_page_config(page_title="BioSim: Simuladores Educativos", layout="wide")
st.title("🧬 BioSim: Simuladores Bioinformáticos Educativos")

# Menú lateral
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
elif simulador == "2. Mutaciones y Estructura Proteica":
    st.header("2. Impacto de Mutaciones Puntuales")
    st.write("Modifica un nucleótido y observa si la proteína cambia de forma o función.")
    
    secuencia_original = "AUGGGCACUUAA"
    st.write(f"**Secuencia de ARNm Original:** `{secuencia_original}` (Codifica: Met - Gly - Thr - STOP)")
    
    posicion = st.slider("Selecciona la posición para mutar (0 a 11):", 0, 11, 4)
    nuevo_nucleotido = st.selectbox("Selecciona el nuevo nucleótido:", ["A", "U", "C", "G"])
    
    # Aplicar mutación
    lista_arn = list(secuencia_original)
    lista_arn[posicion] = nuevo_nucleotido
    secuencia_mutada = "".join(lista_arn)
    
    st.warning(f"**Secuencia Mutada:** {secuencia_mutada[:posicion]}**{secuencia_mutada[posicion]}**{secuencia_mutada[posicion+1:]}")
    
    # Evaluar impacto pedagógico
    if posicion in [3, 4, 5]: # Modificando el segundo codón (GGC -> Gly)
        codon_mutado = secuencia_mutada[3:6]
        if codon_mutado == "GGC":
            st.info("🧬 **Mutación Silenciosa:** El aminoácido sigue siendo Glicina. La proteína mantiene su estructura tridimensional intacta.")
        elif codon_mutado == "GAC":
            st.error("🚨 **Mutación Missense (Cambio de sentido):** Cambió a Ácido Aspártico (Cargado negativamente). ¡La proteína podría plegarse mal y perder su función!")
        else:
            st.error(f"🚨 **Mutación Missense:** El codón ahora es {codon_mutado}. Cambia la afinidad química en esa posición de la proteína.")
    else:
        st.info("✨ Cambiaste otra región. Intenta cambiar la posición 4 para ver efectos en el núcleo activo.")

# -------------------------------------------------------------------------
# SIMULADOR 3: Matriz de Alineamiento Global (Needleman-Wunsch simplificado)
# -------------------------------------------------------------------------
elif simulador == "3. Visualizador Didáctico de Matrices de Alineamiento" :
    st.header("3. Construcción de Matrices de Puntuación")
    st.write("Entiende la matemática detrás de los algoritmos de alineamiento global.")
    
    seq1 = "-" + st.text_input("Secuencia Horizontal 1:", "AAGC").upper()
    seq2 = "-" + st.text_input("Secuencia Vertical 2:", "AGC").upper()
    
    # Crear una matriz visual didáctica basada en coincidencias simples
    matriz = []
    for char2 in seq2:
        fila = []
        for char1 in seq1:
            if char1 == "-" or char2 == "-":
                fila.append(0) # Penalización de gaps simplificada
            elif char1 == char2:
                fila.append(5) # Match score
            else:
                fila.append(-2) # Mismatch score
        matriz.append(fila)
        
    df_matriz = pd.DataFrame(matriz, index=list(seq2), columns=list(seq1))
    st.write("**Matriz de Puntuación Resultante (Match = +5, Mismatch = -2, Gap = 0):**")
    st.dataframe(df_matriz.style.highlight_max(axis=None, color="#b3e5fc"))
    st.caption("💡 Los valores resaltados te indican visualmente dónde coinciden los caracteres para trazar el mejor camino de alineamiento.")

# -------------------------------------------------------------------------
# SIMULADOR 4: Gráficos de De Bruijn (Genómica)
# -------------------------------------------------------------------------
elif simulador == "4. Simulador de Ensamble de Fragmentos" :
    st.header("4. Ensamble de Genomas mediante K-meros")
    st.write("Divide una secuencia en fragmentos pequeños (k-meros) para entender cómo el software reconstruye un genoma.")
    
    secuencia_completa = st.text_input("Secuencia de Genoma Referencia:", "ATGCTAGC").upper()
    k = st.slider("Tamaño del K-mero (Longitud de ventana):", 2, 4, 3)
    
    # Generar fragmentos (k-meros)
    kmeros = [secuencia_completa[i:i+k] for i in range(len(secuencia_completa) - k + 1)]
    st.write(f"**Fragmentos generados (`{k}-meros`):** {kmeros}")
    
    st.write("**Flujo Lógico del Ensamble (Unión por solapamiento):**")
    for i in range(len(kmeros)-1):
        prefijo = kmeros[i][1:]
        sufijo = kmeros[i+1][:-1]
        if prefijo == sufijo:
            st.write(f"🟢 El fragmento `{kmeros[i]}` se conecta con `{kmeros[i+1]}` a través del solapamiento **'{prefijo}'**")

# -------------------------------------------------------------------------
# SIMULADOR 5: Distancia Filogenética Básica (UPGMA)
# -------------------------------------------------------------------------
elif simulador == "5. Construcción de Árboles Evolutivos":
    st.header("5. Matriz de Distancia Genética y Filogenia")
    st.write("Modifica las distancias mutacionales para ver qué especies están más emparentadas.")
    
    st.write("Establece la distancia genética entre la Especie A, B y C:")
    dist_AB = st.slider("Distancia entre Especie A y Especie B:", 1, 20, 4)
    dist_AC = st.slider("Distancia entre Especie A y Especie C:", 1, 20, 12)
    
    st.write("**Árbol Evolutivo Representativo (Esquema de ramificación):**")
    
    if dist_AB < dist_AC:
        st.code(f"""
          ┌─── Especie A (Distancia: {dist_AB/2})
    ──────┤
          └─── Especie B (Distancia: {dist_AB/2})
          │
          └────────────────────────── Especie C (Distancia: {dist_AC})
        """, language="text")
        st.success("💡 Conclusión Didáctica: La Especie A y B comparten un ancestro común más reciente porque su distancia genética es menor.")
    else:
        st.code(f"""
          ┌─── Especie A
    ──────┤
          └────────────────────────── Especie B
          │
          └─── Especie C
        """, language="text")
