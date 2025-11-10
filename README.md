# 🧠 PROYECTO Y EVALUACIÓN FINAL  
### 👩‍💻 **Alumna:** Sofía Antonia Gamallo  
### 🪪 **DNI:** 42.432.866  
---

## 🧩 SISTEMA INTEGRAL INTELIGENTE PARA ANÁLISIS DE PERSONALIDAD MBTI

---

### 📘 **Resumen del Proyecto**

Este proyecto consiste en el desarrollo de un **Sistema Inteligente Integral** capaz de analizar las **16 personalidades del modelo MBTI (Myers–Briggs Type Indicator)**, integrando tres pilares fundamentales de la inteligencia artificial:

1. 🧠 **Percepción:**  
   Mediante una **red neuronal profunda (Deep Learning)** entrenada con datos del cuestionario MBTI, el sistema es capaz de **predecir el tipo de personalidad** de un usuario a partir de sus respuestas.

2. 🔍 **Razonamiento lógico:**  
   A través de un conjunto de **reglas simbólicas de inferencia**, el agente interpreta los rasgos psicológicos asociados a cada tipo MBTI y genera **explicaciones coherentes y personalizadas** del resultado.

3. 🗺️ **Planificación y búsqueda informada:**  
   Utiliza el **algoritmo A\*** junto con una **heurística cognitiva ponderada** para calcular el **camino óptimo entre personalidades**, simulando un proceso de evolución o afinidad entre tipos.

---

## 🎯 **Objetivos del Sistema**

### ✅ **Funcionales**
- Permitir al usuario completar un test de 60 preguntas MBTI de manera interactiva (valores de -3 a +3).  
- Analizar las respuestas utilizando un modelo de aprendizaje profundo previamente entrenado.  
- Mostrar el tipo de personalidad MBTI resultante junto con su nivel de confianza.  
- Generar una **explicación textual** razonada del resultado.  
- Calcular y visualizar el **camino más corto entre dos tipos MBTI** (por ejemplo, entre el actual y un tipo objetivo).  

### ⚙️ **No Funcionales**
- Interfaz visual e intuitiva desarrollada en **Streamlit**.  
- Alta precisión de predicción (> 98%).  
- Modularidad y escalabilidad del código.  
- Explicabilidad y trazabilidad de las decisiones del modelo.  

---

## 🧩 **Descripción de los Módulos del Sistema**

| Módulo | Descripción |
|---------|--------------|
| **🧠 percepcion.py** | Maneja la **carga de datos**, preprocesamiento, entrenamiento y predicción del modelo neuronal (Keras / TensorFlow). Convierte las respuestas humanas en datos numéricos procesables. |
| **🔍 razonamiento.py** | Implementa la **base de conocimiento MBTI** y el **algoritmo de búsqueda A\***. Contiene las funciones de inferencia (`razonar_sobre_tipo`) y la heurística personalizada (`heuristica_sofisticada`). |
| **🤖 agente.py** | Integra todos los componentes (percepción + razonamiento + planificación) y actúa como **agente inteligente unificado**. |
| **🧩 app.py** | Interfaz gráfica desarrollada con **Streamlit**. Presenta el test, gestiona las respuestas, muestra los resultados y permite descargar el informe en JSON. |
| **main.py** | Permite la **ejecución directa del agente** desde consola, ideal para pruebas y depuración. |

---

## 🔄 **Flujo de Datos y Decisiones**

### 🧭 Arquitectura del Agente Inteligente

**Entorno:**  
El entorno es el **usuario**, quien responde las preguntas del test MBTI.

**Agente Inteligente:**  
El sistema MBTI actúa como un agente racional compuesto por:
- 👁️ **Sensor (Percepción):** recibe y procesa las respuestas.  
- 🧩 **Razonamiento:** analiza la información y genera una explicación.  
- 🗺️ **Planificación:** busca el camino óptimo hacia un tipo objetivo.  
- 💬 **Actuador (Interfaz):** muestra los resultados al usuario.

---

### 📊 **Flujo del Sistema**

[Usuario responde Test MBTI en Streamlit]
            │
            ▼
 [Respuestas numéricas (-3 a +3)]
            │
            ▼
 [🧠 Módulo de Percepción]
 - Escala y normaliza los datos
 - Carga el modelo Keras preentrenado
 - Predice el tipo MBTI (ej. INFP)
            │
            ▼
 [🔍 Módulo de Razonamiento]
 - Interpreta los rasgos del tipo
 - Genera una explicación textual lógica
            │
            ▼
 [🗺️ Módulo de Planificación (A*)]
 - Calcula el camino entre tipo actual y tipo objetivo
 - Devuelve pasos, nodos explorados y eficiencia
            │
            ▼
 [💻 Interfaz Streamlit]
 - Muestra el resultado, confianza y descripción
 - Permite descargar el informe en JSON


---

## 🧠 **Explicación de la Inteligencia del Sistema**

### 🔹 **Razonamiento Lógico (`razonar_sobre_tipo`)**

Implementa reglas simbólicas del tipo **“si el rasgo es I → entonces es introvertido”**, generando una descripción explicativa del tipo MBTI.  
Cada letra del tipo (E/I, N/S, T/F, J/P) corresponde a un eje de comportamiento:

| Letra | Dimensión | Interpretación |
|--------|-------------|----------------|
| E / I | Energía | Extroversión o Introversión |
| N / S | Percepción | Intuición o Sensorialidad |
| T / F | Decisión | Pensamiento o Sentimiento |
| J / P | Estilo | Juicio o Percepción |

De esta forma, el sistema **explica el resultado de forma textual**, ofreciendo **transparencia cognitiva**, un aspecto clave en la IA moderna.

---

### 🔹 **Búsqueda Informada (`busqueda_a_estrella`)**

El sistema utiliza el **algoritmo A\*** para simular cómo una persona podría “moverse” o “transformarse” entre tipos MBTI.

Cada tipo de personalidad es un **nodo del grafo**, y cada cambio de rasgo (por ejemplo, de “I” a “E”) representa una **transición entre estados**.

El objetivo es encontrar el **camino más corto y coherente psicológicamente** entre un tipo actual y uno deseado.

#### ⚙️ **Heurística Cognitiva Ponderada**

La función `heuristica_sofisticada()` asigna pesos distintos a cada rasgo según su relevancia psicológica:

| Dimensión | Peso | Significado |
|------------|-------|-------------|
| E / I | 2 | Nivel de energía (moderado) |
| N / S | 3 | Tipo de percepción (clave) |
| T / F | 3 | Forma de decidir (clave) |
| J / P | 1 | Estilo de vida (superficial) |

Esta heurística guía la búsqueda de manera más natural e inteligente, priorizando caminos **más realistas y coherentes** entre tipos.

#### 💡 **Ejemplo:**

ISFP → INFP → ENFP

✅ Camino óptimo en 2 pasos  
💬 Representa una evolución de una personalidad artística reservada hacia una más extrovertida y creativa.  
📈 Eficiencia: 100%

---

## 💻 **Tecnologías y Herramientas Utilizadas**

| Categoría | Herramientas |
|------------|--------------|
| **Lenguaje principal** | Python 3.11 |
| **Machine Learning / Deep Learning** | TensorFlow, Keras, Scikit-learn |
| **Análisis y manipulación de datos** | Pandas, NumPy |
| **Visualización e interfaz gráfica** | Streamlit, Plotly |
| **Gestión de entorno virtual** | `venv` |
| **Persistencia del modelo** | `.h5` (modelo Keras), `.npy` (scaler, label encoder) |
| **Exportación de resultados** | JSON |

---

## 🧪 **Pruebas y Evaluación de Resultados**

El modelo fue entrenado sobre un dataset con **59.999 registros y 60 atributos** correspondientes a las respuestas del test.  

| Métrica | Resultado |
|----------|------------|
| **Exactitud (accuracy)** | 0.985 |
| **Precisión promedio** | 0.98 |
| **Recall promedio** | 0.97 |
| **F1-score promedio** | 0.98 |
| **Número de clases (MBTI)** | 16 |

🔬 Los resultados muestran un rendimiento **altamente estable y equilibrado** en todas las clases, demostrando **una generalización robusta del modelo**.

---

## 🧾 **Conclusiones Finales**

- Se logró integrar los tres componentes esenciales de la IA:
  - **Percepción:** modelo neuronal (aprendizaje automático).  
  - **Razonamiento simbólico:** inferencia lógica sobre rasgos MBTI.  
  - **Planificación:** búsqueda informada con heurística cognitiva.  

- El sistema no solo predice, sino que **explica y razona**, ofreciendo una experiencia **transparente y comprensible** para el usuario.  

- La **búsqueda A\*** permite representar **afinidades psicológicas** entre personalidades, funcionando como una herramienta de exploración cognitiva.  

- Se desarrolló una **interfaz interactiva y moderna**, integrando todos los componentes de manera coherente.
