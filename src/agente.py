"""
MÓDULO AGENTE INTEGRADOR
Integra percepción, razonamiento y búsqueda en un agente inteligente unificado.
"""

import json
from percepcion import SistemaPercepcion
from razonamiento import SistemaRazonamiento
import os

class AgentePersonalidad:
    def __init__(self, ruta_modelo=None):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        if ruta_modelo is None:
            ruta_modelo = os.path.join(base_dir, "../models/modelo_personalidad.h5")
        self.percepcion = SistemaPercepcion(ruta_modelo)
        self.percepcion.cargar_modelo()
        print(f"🤖 Modelo cargado desde: {ruta_modelo}")

 #Análisis completo
    def analizar_completo(self, respuestas, tipo_objetivo=None):
        # 1. PERCEPCIÓN (Machine Learning)
        tipo_predicho, confianza = self.percepcion.predecir(respuestas)

        # 2. RAZONAMIENTO (Lógica)
        info_logica = SistemaRazonamiento.razonar_sobre_tipo(tipo_predicho)

        # 3. Resultado integrado
        resultado = {
            "tipo_predicho": tipo_predicho,
            "confianza": f"{confianza:.1f}%",
            "descripcion": info_logica["descripcion"],
            "razonamiento": info_logica["razonamiento"]
        }

        # 4. BÚSQUEDA (A* - Planificación)
        if tipo_objetivo:
            if SistemaRazonamiento.validar_tipo_mbti(tipo_objetivo):
                busqueda = SistemaRazonamiento.busqueda_a_estrella(tipo_predicho, tipo_objetivo)
                if busqueda:
                    resultado["planificacion"] = {
                        "objetivo": tipo_objetivo,
                        "camino": busqueda["camino"],
                        "pasos_necesarios": busqueda["costo"],
                        "nodos_explorados": len(busqueda["nodos_explorados"]),
                        "eficiencia": f"{busqueda['eficiencia']:.1%}"
                    }
            else:
                resultado["error_objetivo"] = f"Tipo objetivo inválido: {tipo_objetivo}"

        return resultado

    def entrenar_modelo(self, ruta_csv="../data/16P.csv"):
        """Entrena el modelo de percepción"""
        return self.percepcion.entrenar(ruta_csv)


if __name__ == "__main__":
    import numpy as np

    # Ejemplo de uso
    agente = AgentePersonalidad()
    respuestas_ejemplo = np.random.randint(-3, 4, size=60).tolist()
    resultado = agente.analizar_completo(respuestas_ejemplo, tipo_objetivo="ENFP")

    print(json.dumps(resultado, indent=2, ensure_ascii=False))

