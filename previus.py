from agno.agent import Agent
from agno.models.groq import Groq
from agno.agent import Agent, RunResponse
from typing import Iterator
from dotenv import load_dotenv
import sqlite3
import json
from tools_turism import TurismToolkit
from storage_usage import load_social_media_storage

load_dotenv()
system_prompt = open("system_prompt.txt", "r").read()

# Configurar el agente con las herramientas (funciones) para el bot de turismo
agent = Agent(
    
    model=Groq(
    id="deepseek-r1-distill-llama-70b"),
    system_message=system_prompt,

    #tools=[get_ciudades, get_lugares_por_ciudad, registrar_usuario, crear_reserva, obtener_reservas_usuario],
    tools=[TurismToolkit()],
    
    markdown=True
)

""" while True == True:
    answer = input("USER: ")
    run_response: Iterator[RunResponse] = agent.run(answer, stream=True)

    full_response = ""
    for chunk in run_response:
        full_response += chunk.content

    print("BOT:" + full_response)
    if answer == "adios":
        break """

while True == True:
    answer = input("USER: ")
    agent.print_response(answer, stream=True)

    if answer == "adios":
        break