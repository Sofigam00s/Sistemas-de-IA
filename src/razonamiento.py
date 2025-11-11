"""
MÓDULO DE RAZONAMIENTO LÓGICO Y BÚSQUEDA INFORMADA
"""

import heapq
from typing import List, Dict, Optional, Tuple

# Base de conocimiento MBTI
TIPOS_MBTI = [
    "ESTJ", "ENTJ", "ESFJ", "ENFJ",
    "ISTJ", "ISFJ", "INTJ", "INFJ",
    "ESTP", "ESFP", "ENTP", "ENFP",
    "ISTP", "ISFP", "INTP", "INFP"
]

# Descripciones
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

# Pesos por dimensión (E/I, N/S, T/F, J/P).
# Uso estos pesos en el modo 'weighted' como costo de transición
PESOS = [2, 3, 3, 1]


class SistemaRazonamiento:
    @staticmethod
    def validar_tipo_mbti(tipo: str) -> bool:
        """Valida que el tipo MBTI sea correcto."""
        if not isinstance(tipo, str) or len(tipo) != 4:
            return False
        if tipo[0] not in ['E', 'I'] or tipo[1] not in ['N', 'S'] or tipo[2] not in ['T', 'F'] or tipo[3] not in ['J', 'P']:
            return False
        return tipo in TIPOS_MBTI

    @staticmethod
    def obtener_descripcion(tipo: str) -> str:
        return DESCRIPCIONES.get(tipo, "Tipo de personalidad desconocido.")

    @staticmethod
    def razonar_sobre_tipo(tipo: str) -> Dict:
        if not SistemaRazonamiento.validar_tipo_mbti(tipo):
            raise ValueError(f"Tipo MBTI inválido: {tipo}")

        razonamiento = []
        razonamiento.append("Extrovertido: Obtiene energía de la interacción social" if tipo[0] == "E" else "Introvertido: Obtiene energía del tiempo a solas")
        razonamiento.append("Intuitivo: Se enfoca en ideas y patrones abstractos" if tipo[1] == "N" else "Sensorial: Prefiere hechos concretos y experiencias reales")
        razonamiento.append("Pensamiento: Toma decisiones basadas en lógica y objetividad" if tipo[2] == "T" else "Sentimiento: Toma decisiones basadas en valores y empatía")
        razonamiento.append("Juicio: Prefiere planificación, estructura y cierre" if tipo[3] == "J" else "Percepción: Prefiere flexibilidad y espontaneidad")

        return {
            "tipo": tipo,
            "descripcion": SistemaRazonamiento.obtener_descripcion(tipo),
            "razonamiento": razonamiento
        }

    @staticmethod
    def heuristica_hamming(tipo_actual: str, tipo_objetivo: str) -> int:
        """Heurística admisible para costo unitario: número de letras distintas (distancia de Hamming)."""
        return sum(1 for a, b in zip(tipo_actual, tipo_objetivo) if a != b)

    @staticmethod
    def heuristica_ponderada(tipo_actual: str, tipo_objetivo: str) -> int:
        """
        Heurística ponderada: suma de pesos de las dimensiones que difieren.
        Es admisible **si** las acciones tienen costo igual al peso correspondiente.
        """
        return sum(weight for i, weight in enumerate(PESOS) if tipo_actual[i] != tipo_objetivo[i])

    # Generador de vecinos (retorna (vecino, costo_transicion))
    @staticmethod
    def generar_vecinos_con_costos(tipo: str, mode: str = "weighted") -> List[Tuple[str, int]]:
        """
        Genera vecinos del tipo y devuelve una lista de (vecino, costo) según el modo.
        mode:
          - "unit": cada transición cuesta 1
          - "weighted": la transición de la dimensión i cuesta PESOS[i]
        """
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
                costo = 1 if mode == "unit" else PESOS[i]
                vecinos.append((vecino, costo))
        return vecinos

    # Búsqueda A*
    @staticmethod
    def busqueda_a_estrella(inicio: str, objetivo: str, mode: str = "weighted") -> Optional[Dict]:
        """
        Algoritmo A* para encontrar el camino óptimo entre dos tipos MBTI.
        mode: "unit" (g(n)=1 por acción) o "weighted" (g(n)=peso del rasgo cambiado).
        Devuelve dict con 'camino', 'costo', 'nodos_explorados', 'eficiencia'.
        """
        if not SistemaRazonamiento.validar_tipo_mbti(inicio):
            raise ValueError(f"Tipo inicio inválido: {inicio}")
        if not SistemaRazonamiento.validar_tipo_mbti(objetivo):
            raise ValueError(f"Tipo objetivo inválido: {objetivo}")
        if mode not in ("unit", "weighted"):
            raise ValueError("mode debe ser 'unit' o 'weighted'")

        # Selecciona heurística adecuada (admisible según el modo)
        if mode == "unit":
            heuristica = SistemaRazonamiento.heuristica_hamming
        else:
            heuristica = SistemaRazonamiento.heuristica_ponderada

        # Nodo en la frontera: (f = g + h, g, estado, camino)
        inicio_h = heuristica(inicio, objetivo)
        frontera = [(inicio_h, 0, inicio, [inicio])]
        visitados = {}
        nodos_explorados = []

        while frontera:
            f, g, actual, camino = heapq.heappop(frontera)
            # Si ya hay un mejor g registrado para 'actual', salta
            if actual in visitados and g > visitados[actual]:
                continue

            nodos_explorados.append(actual)

            if actual == objetivo:
                return {
                    "camino": camino,
                    "costo": g,
                    "nodos_explorados": nodos_explorados,
                    "eficiencia": len(camino) / len(nodos_explorados) if nodos_explorados else 0.0
                }

            visitados[actual] = g

            for vecino, costo_transicion in SistemaRazonamiento.generar_vecinos_con_costos(actual, mode=mode):
                nuevo_g = g + costo_transicion
                h_vec = heuristica(vecino, objetivo)
                prioridad = nuevo_g + h_vec
                # Si tenemos ya mejor g para vecino, saltar (mejor camino conocido)
                if vecino in visitados and nuevo_g >= visitados[vecino]:
                    continue
                heapq.heappush(frontera, (prioridad, nuevo_g, vecino, camino + [vecino]))

        return None


# Ejemplos / Pruebas (solo si se ejecuta como script)

if __name__ == "__main__":
    print("Prueba A* modo unitario (g=1, h=Hamming -> admisible):")
    r1 = SistemaRazonamiento.busqueda_a_estrella("INTP", "ENFP", mode="unit")
    print(r1)

    print("\nPrueba A* modo ponderado (g=peso, h= suma de pesos mismatched -> admisible):")
    r2 = SistemaRazonamiento.busqueda_a_estrella("ISFP", "ENFP", mode="weighted")
    print(r2)

    print("\nRazonamiento sobre tipo 'INTP':")
    print(SistemaRazonamiento.razonar_sobre_tipo("INTP"))
