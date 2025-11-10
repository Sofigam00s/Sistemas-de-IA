"""
MÓDULO DE RAZONAMIENTO LÓGICO Y BÚSQUEDA INFORMADA
Contiene la lógica de inferencia MBTI y el algoritmo A* para navegación entre personalidades.
"""

import heapq
import numpy as np

# Base de conocimiento MBTI
TIPOS_MBTI = [
    "ESTJ", "ENTJ", "ESFJ", "ENFJ",
    "ISTJ", "ISFJ", "INTJ", "INFJ",
    "ESTP", "ESFP", "ENTP", "ENFP",
    "ISTP", "ISFP", "INTP", "INFP"
]

DESCRIPCIONES = {
    "INTJ": "Pensador estratégico e independiente. Enfocado en la lógica y planificación a largo plazo.",
    "INTP": "Analítico, lógico y curioso. Le gusta comprender cómo funcionan las cosas.",
    "ENTJ": "Líder natural y decidido. Se motiva por los desafíos y la eficiencia.",
    "ENTP": "Innovador y argumentativo. Disfruta los debates y las ideas nuevas.",
    "INFJ": "Idealista, empático y con visión profunda. Tiende a ayudar a otros a encontrar propósito.",
    "INFP": "Soñador y sensible. Guiado por sus valores personales y la autenticidad.",
    "ENFJ": "Sociable y altruista. Destacado en motivar e inspirar a los demás.",
    "ENFP": "Creativo y entusiasta. Vive explorando ideas y emociones nuevas.",
    "ISTJ": "Responsable, organizado y confiable. Prefiere reglas claras y estabilidad.",
    "ISFJ": "Amable y comprometido. Cuida el bienestar de quienes le rodean.",
    "ESTJ": "Práctico, decidido y buen gestor. Prefiere el orden y la estructura.",
    "ESFJ": "Sociable y cooperativo. Busca armonía y aprobación social.",
    "ISTP": "Observador, técnico y adaptable. Aprende mejor haciendo.",
    "ISFP": "Artístico y reservado. Se guía por la estética y la autenticidad.",
    "ESTP": "Activo, arriesgado y energético. Aprende mediante la experiencia directa.",
    "ESFP": "Alegre, espontáneo y divertido. Vive el momento y disfruta el presente."
}


class SistemaRazonamiento:
    @staticmethod
    def validar_tipo_mbti(tipo):
        """Valida que el tipo MBTI sea correcto"""
        if not isinstance(tipo, str) or len(tipo) != 4:
            return False
        if tipo[0] not in ['E', 'I']:
            return False
        if tipo[1] not in ['N', 'S']:
            return False
        if tipo[2] not in ['T', 'F']:
            return False
        if tipo[3] not in ['J', 'P']:
            return False
        return tipo in TIPOS_MBTI

    @staticmethod
    def obtener_descripcion(tipo):
        """Obtiene la descripción de un tipo MBTI"""
        return DESCRIPCIONES.get(tipo, "Tipo de personalidad desconocido.")

    @staticmethod
    def razonar_sobre_tipo(tipo):
        """Genera inferencias lógicas basadas en el tipo MBTI"""
        if not SistemaRazonamiento.validar_tipo_mbti(tipo):
            raise ValueError(f"Tipo MBTI inválido: {tipo}")

        razonamiento = []

        # Reglas lógicas de inferencia
        if tipo[0] == "E":
            razonamiento.append("Extrovertido: Obtiene energía de la interacción social")
        else:
            razonamiento.append("Introvertido: Obtiene energía del tiempo a solas")

        if tipo[1] == "N":
            razonamiento.append("Intuitivo: Se enfoca en ideas y patrones abstractos")
        else:
            razonamiento.append("Sensorial: Prefiere hechos concretos y experiencias reales")

        if tipo[2] == "T":
            razonamiento.append("Pensamiento: Toma decisiones basadas en lógica y objetividad")
        else:
            razonamiento.append("Sentimiento: Toma decisiones basadas en valores y empatía")

        if tipo[3] == "J":
            razonamiento.append("Juicio: Prefiere planificación, estructura y cierre")
        else:
            razonamiento.append("Percepción: Prefiere flexibilidad y espontaneidad")

        return {
            "tipo": tipo,
            "descripcion": SistemaRazonamiento.obtener_descripcion(tipo),
            "razonamiento": razonamiento
        }

    @staticmethod
    def heuristica_sofisticada(tipo_actual, tipo_objetivo):
        """
        Heurística ponderada que considera la importancia de cada dimensión MBTI.
        N/S y T/F son más fundamentales (peso 3), E/I es intermedio (peso 2), J/P es superficial (peso 1).
        """
        pesos = [2, 3, 3, 1]  # E/I, N/S, T/F, J/P
        distancia = sum(
            peso for i, peso in enumerate(pesos)
            if tipo_actual[i] != tipo_objetivo[i]
        )
        return distancia

    @staticmethod
    def generar_vecinos(tipo):
        """Genera personalidades vecinas cambiando un rasgo por su opuesto"""
        cambios = {
            0: {"E": "I", "I": "E"},
            1: {"N": "S", "S": "N"},
            2: {"T": "F", "F": "T"},
            3: {"J": "P", "P": "J"}
        }

        vecinos = []
        for i, letra in enumerate(tipo):
            nuevo = list(tipo)
            nuevo[i] = cambios[i][letra]
            vecino = "".join(nuevo)
            if vecino in TIPOS_MBTI:
                vecinos.append(vecino)
        return vecinos

    @staticmethod
    def busqueda_a_estrella(inicio, objetivo):
        """
        Algoritmo A* para encontrar el camino óptimo entre dos tipos de personalidad.
        Retorna el camino y los nodos explorados.
        """
        if not SistemaRazonamiento.validar_tipo_mbti(inicio):
            raise ValueError(f"Tipo inicio inválido: {inicio}")
        if not SistemaRazonamiento.validar_tipo_mbti(objetivo):
            raise ValueError(f"Tipo objetivo inválido: {objetivo}")

        frontera = [(SistemaRazonamiento.heuristica_sofisticada(inicio, objetivo), 0, inicio, [inicio])]
        visitados = set()
        nodos_explorados = []

        while frontera:
            _, costo, actual, camino = heapq.heappop(frontera)
            nodos_explorados.append(actual)

            if actual == objetivo:
                return {
                    "camino": camino,
                    "costo": costo,
                    "nodos_explorados": nodos_explorados,
                    "eficiencia": len(camino) / len(nodos_explorados)
                }

            if actual in visitados:
                continue
            visitados.add(actual)

            for vecino in SistemaRazonamiento.generar_vecinos(actual):
                nuevo_costo = costo + 1
                prioridad = nuevo_costo + SistemaRazonamiento.heuristica_sofisticada(vecino, objetivo)
                heapq.heappush(frontera, (prioridad, nuevo_costo, vecino, camino + [vecino]))

        return None


if __name__ == "__main__":
    # Prueba de razonamiento
    info = SistemaRazonamiento.razonar_sobre_tipo("INTP")
    print("Razonamiento:", info)

    # Prueba de búsqueda A*
    resultado = SistemaRazonamiento.busqueda_a_estrella("INTP", "ENFP")
    print(f"\nCamino: {' → '.join(resultado['camino'])}")
    print(f"Costo: {resultado['costo']} pasos")
    print(f"Eficiencia: {resultado['eficiencia']:.2%}")
