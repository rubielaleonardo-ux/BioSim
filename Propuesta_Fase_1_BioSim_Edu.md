# Propuesta de Proyecto
## BioSim Edu: Plataforma Web Interactiva para la Enseñanza de la Bioinformática

### Integrante
- __________________

---

# 1. Descripción del Proyecto

BioSim Edu es una plataforma web interactiva desarrollada en Python utilizando Streamlit, diseñada para facilitar el aprendizaje de conceptos fundamentales de bioinformática mediante simulaciones educativas. La aplicación reúne cinco simuladores en una sola interfaz, permitiendo a los estudiantes comprender el funcionamiento de algoritmos bioinformáticos de manera visual e interactiva.

Los simuladores incluidos son:

- Alineamiento Global (Needleman-Wunsch)
- Alineamiento Local (Smith-Waterman)
- Transcripción y Traducción de ADN
- Simulación de Mutaciones
- Filogenia

# 2. Herramientas y Algoritmos Seleccionados

| Simulador | Algoritmo o Proceso Base |
|-----------|--------------------------|
| Alineamiento Global | Needleman-Wunsch |
| Alineamiento Local | Smith-Waterman |
| Transcripción y Traducción | Dogma Central de la Biología Molecular |
| Mutaciones | Sustitución, Inserción y Deleción |
| Filogenia | UPGMA (o el algoritmo utilizado) |

# 3. Público Objetivo

Estudiantes de secundaria superior y primeros años universitarios que cursan Biología, Genética o Bioinformática.

# 4. Variables Simplificadas

| Simulador | Simplificación |
|-----------|----------------|
| Alineamiento Global | Secuencias cortas y puntuación fija. |
| Alineamiento Local | Visualización simplificada de la matriz. |
| Transcripción y Traducción | Conversión directa ADN→ARN→Proteína. |
| Mutaciones | Sustituciones, inserciones y deleciones simples. |
| Filogenia | Pocas especies y distancias manuales. |

# 5. Flujo Lógico

```text
Inicio
 ↓
Pantalla Principal
 ↓
Seleccionar Simulador
 ↓
Ingresar Datos
 ↓
Validar Información
 ↓
Ejecutar Algoritmo
 ↓
Mostrar Resultados
 ↓
Explicación Didáctica
 ↓
Autoevaluación
 ↓
Fin
```

# 6. Wireframe

```text
+----------------------------------------------+
|               BioSim Edu                     |
+----------------------------------------------+
| Menú lateral                                 |
| • Inicio                                     |
| • Alineamiento Global                        |
| • Alineamiento Local                         |
| • Transcripción y Traducción                 |
| • Mutaciones                                 |
| • Filogenia                                  |
+----------------------------------------------+
| Área principal del simulador                 |
| [Ingrese datos]                              |
| [ Simular ]                                  |
| Resultados                                   |
| Explicación                                  |
| Autoevaluación                               |
+----------------------------------------------+
```

# 7. Resultado Esperado

Desarrollar una aplicación web interactiva que permita comprender de forma sencilla el funcionamiento de algoritmos bioinformáticos mediante simulaciones educativas.
