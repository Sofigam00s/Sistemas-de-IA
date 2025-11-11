# 🧠 PROYECTO Y EVALUACIÓN FINAL  
### 👩‍💻 **Alumna:** Sofía Antonia Gamallo  
### 🪪 **DNI:** 42.432.866  
---

## 🧩 SISTEMA INTEGRAL INTELIGENTE PARA ANÁLISIS DE PERSONALIDAD MBTI

---

### 📘 **Resumen del Proyecto**

Sistema de Inteligencia Artificial que simula un agente racional para predecir la personalidad MBTI de un usuario. El agente integra Machine Learning para la percepción y clasificación inicial, Razonamiento Lógico para la inferencia de rasgos, y el algoritmo A* para la planificación óptima de la transición entre tipos de personalidad.

### **Propósito**

Demostrar la integración de técnicas de IA para resolver un problema de clasificación y planificación en un entorno discreto (los 16 tipos MBTI).

---

## 🎯 **Objetivos del Sistema**

   * Clasificar la personalidad de un usuario a partir de 60 variables de entrada (respuestas al cuestionario) utilizando una Red Neuronal.
   * Ejecutar inferencia lógica para derivar las características detalladas asociadas al tipo de personalidad predicho.
   *  Calcular la ruta óptima y de menor costo (camino) para transformar la personalidad inicial en una personalidad objetivo mediante el algoritmo A*.
     
---

## 🧩 **Descripción de los Módulos del Sistema**

| Módulo | Descripción |
|---------|--------------|
| Módulo de Percepción y ML **🧠 percepcion.py** | Percepción y Aprendizaje. Carga, preprocesamiento y entrenamiento de la Red Neuronal para clasificación. |
| Módulo de Razonamiento Lógico y Búsqueda Informada **🔍 razonamiento.py** | Conocimiento e Inferencia: Almacena la BC (MBTI) y simula el Encadenamiento Hacia Adelante para inferir las características de personalidad. Planificación: Implementa el Algoritmo A* para encontrar la secuencia de transiciones óptima. Define el espacio de estados y las funciones heurísticas (h(n)).|
| Módulo Agente Integrador **🤖 agente.py** | Actuación. Define el flujo coherente del agente: recibe datos, consulta el ML, alimenta la lógica con el resultado y, si se requiere, planifica la ruta óptima. |
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
