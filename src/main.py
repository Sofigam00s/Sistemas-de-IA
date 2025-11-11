'''
MÓDULO INTEGRADOR Y EJECUTOR DEL AGENTE
'''

from agente import AgentePersonalidad
import numpy as np
import json

PREGUNTAS = [
    "Haces nuevos amigos regularmente",
    "Pasas mucho de tu tiempo libre explorando varios temas aleatorios que despiertan tu interés",
    "Ver a otras personas llorar puede fácilmente hacer que sientas que quieres llorar también",
    "A menudo haces un plan de respaldo para un plan de respaldo",
    "Usualmente mantienes la calma incluso bajo mucha presión",
    "En eventos sociales rara vez intentas presentarte a nuevas personas y principalmente hablas con los que ya conoces",
    "Prefieres terminar completamente un proyecto antes de comenzar otro",
    "Eres muy sentimental",
    "Te gusta usar herramientas de organización como horarios y listas",
    "Incluso un pequeño error puede hacer que dudes de tus habilidades y conocimientos generales",
    "Te sientes cómodo simplemente acercándote a alguien que te parece interesante e iniciando una conversación",
    "No estás demasiado interesado en discutir varias interpretaciones y análisis de obras creativas",
    "Eres más propenso a seguir tu cabeza que tu corazón",
    "Por lo general prefieres simplemente hacer lo que te apetece en un momento dado en lugar de planificar una rutina diaria particular",
    "Rara vez te preocupas por si causas una buena impresión en las personas que conoces",
    "Disfrutas participando en actividades grupales",
    "Te gustan los libros y películas que te hacen llegar a tu propia interpretación del final",
    "Tu felicidad proviene más de ayudar a otros a lograr cosas que de tus propios logros",
    "Estás interesado en tantas cosas que te resulta difícil elegir qué probar a continuación",
    "Eres propenso a preocuparte de que las cosas empeoren",
    "Evitas los roles de liderazgo en entornos grupales",
    "Definitivamente no eres una persona de tipo artístico",
    "Crees que el mundo sería un lugar mejor si la gente confiara más en la racionalidad y menos en sus sentimientos",
    "Prefieres hacer tus tareas antes de permitirte relajarte",
    "Disfrutas viendo a la gente discutir",
    "Tiendes a evitar llamar la atención sobre ti mismo",
    "Tu estado de ánimo puede cambiar muy rápidamente",
    "Pierdes la paciencia con las personas que no son tan eficientes como tú",
    "A menudo terminas haciendo cosas en el último momento posible",
    "Siempre te ha fascinado la pregunta de qué si acaso algo sucede después de la muerte",
    "Generalmente prefieres estar rodeado de otros en lugar de estar solo",
    "Te aburres o pierdes interés cuando la discusión se vuelve altamente teórica",
    "Te resulta fácil empatizar con una persona cuyas experiencias son muy diferentes a las tuyas",
    "Generalmente pospones la finalización de decisiones tanto como sea posible",
    "Rara vez cuestionas las decisiones que has tomado",
    "Después de una semana larga y agotadora un evento social animado es justo lo que necesitas",
    "Disfrutas ir a museos de arte",
    "A menudo te cuesta entender los sentimientos de otras personas",
    "Te gusta tener una lista de tareas pendientes para cada día",
    "Rara vez te sientes inseguro",
    "Evitas hacer llamadas telefónicas",
    "A menudo pasas mucho tiempo tratando de comprender puntos de vista que son muy diferentes a los tuyos",
    "En tu círculo social a menudo eres el que contacta a tus amigos e inicia actividades",
    "Si tus planes son interrumpidos tu máxima prioridad es volver a encarrilarte tan pronto como sea posible",
    "Todavía te molestan los errores que cometiste hace mucho tiempo",
    "Rara vez contemplas las razones de la existencia humana o el significado de la vida",
    "Tus emociones te controlan más de lo que tú las controlas",
    "Tienes mucho cuidado de no hacer que la gente se vea mal incluso cuando es completamente su culpa",
    "Tu estilo de trabajo personal se acerca más a arranques espontáneos de energía que a esfuerzos organizados y consistentes",
    "Cuando alguien te tiene en alta estima te preguntas cuánto tardarán en sentirse decepcionados contigo",
    "Te encantaría un trabajo que requiera que trabajes solo la mayor parte del tiempo",
    "Crees que reflexionar sobre preguntas filosóficas abstractas es una pérdida de tiempo",
    "Te sientes más atraído por lugares con ambientes concurridos y bulliciosos que por lugares tranquilos e íntimos",
    "Sabes a primera vista cómo se siente alguien",
    "A menudo te sientes abrumado",
    "Completas las cosas de manera metódica sin saltarte ningún paso",
    "Te sientes muy intrigado por las cosas etiquetadas como controversiales",
    "Cederías una buena oportunidad si pensaras que alguien más la necesita más",
    "Tienes problemas con los plazos",
    "Te sientes seguro de que las cosas te saldrán bien"
]

def menu():
    print("\n🧩 Bienvenido al Sistema de Inteligencia Artificial — Test de Personalidad MBTI")
    print("1️⃣  Generar respuestas aleatorias")
    print("2️⃣  Ingresar respuestas manualmente (-3 a +3)")
    print("0️⃣  Salir")

def ejecutar():
    agente = AgentePersonalidad()

    while True:
        menu()
        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            respuestas = np.random.randint(-3, 4, size=60).tolist()
            tipo_objetivo = input("Ingrese un tipo MBTI objetivo (por ej. ENFP, INTJ): ").upper()
            resultado = agente.analizar_completo(respuestas, tipo_objetivo)
            print("\n🧠 Resultado completo:\n")
            print(json.dumps(resultado, indent=4, ensure_ascii=False))


        elif opcion == "2":
            print("\nIngrese 60 respuestas del test (-3 a +3).")
            print("Escala: -3 (Totalmente en desacuerdo) a +3 (Totalmente de acuerdo)\n")
            respuestas = []
            for i in range(60):
                print(f"\n[{i+1}/60] {PREGUNTAS[i]}")
                while True:
                    try:
                        val = int(input("Tu respuesta (-3 a +3): "))
                        if val < -3 or val > 3:
                            raise ValueError
                        respuestas.append(val)
                        break
                    except ValueError:
                        print("⚠️ Ingrese un número entre -3 y 3.")
            tipo_objetivo = input("\nIngrese un tipo MBTI objetivo: ").upper()
            resultado = agente.analizar_completo(respuestas, tipo_objetivo)
            print("\n🧠 Resultado completo:\n")
            print(json.dumps(resultado, indent=4, ensure_ascii=False))

        elif opcion == "0":
            print("👋 Finalizando el agente...")
            break
        else:
            print("❌ Opción no válida.")

if __name__ == "__main__":
    ejecutar()
