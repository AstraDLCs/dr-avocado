import json
from typing import Optional

import typer
from agno.agent import Agent
from agno.models.groq import Groq
from storage_usage import load_social_media_storage
from rich.console import Console
from rich.json import JSON
from rich.panel import Panel
from rich.prompt import Prompt
from rich import print
from tools_turism import TurismToolkit
from dotenv import load_dotenv
system_prompt = open("system_prompt.txt", "r").read()
console = Console()
load_dotenv()

def create_agent(user: str = "user") -> Agent:
    session_id: Optional[str] = None

    # Preguntar si se desea iniciar una nueva sesión o continuar una existente
    new_session = typer.confirm("¿Deseas iniciar una nueva sesión?")

    # Utilizar el almacenamiento (en este ejemplo, la función load_social_media_storage)
    agent_storage = load_social_media_storage()

    # Si no se desea una nueva sesión, buscar las sesiones existentes para este usuario
    if not new_session:
        existing_sessions = agent_storage.get_all_session_ids(user)
        if existing_sessions:
            session_id = existing_sessions[0]  # O elegir según convenga

    # Crear el agente especificando (si se dispone) el session_id para retomar el historial
    agent = Agent(
        user_id=user,
        session_id=session_id,
        system_message=system_prompt,
        name="ChatBot de Turismo-Verde",
        model=Groq(id="deepseek-r1-distill-llama-70b"),
        storage=agent_storage,
        tools=[TurismToolkit()],
        add_history_to_messages=True,
        num_history_responses=7,
        markdown=True,
    )

    if session_id is None:
        session_id = agent.session_id
        print(f"Iniciada nueva sesión: {session_id}\n")
    else:
        print(f"Continuando sesión: {session_id}\n")

    return agent


def print_messages(agent: Agent):
    """Imprime el historial actual de chat en un panel formateado."""
    messages = [
        m.model_dump(include={"role", "content"}) for m in agent.memory.messages
    ]
    console.print(
        Panel(
            JSON(json.dumps(messages, indent=4)),
            title=f"Historial de chat (session_id: {agent.session_id})",
            expand=True,
        )
    )


def main(user: str = "user"):
    agent = create_agent(user)

    print("¡Chat con el agente!")
    exit_on = ["exit", "quit", "bye", "adios", "hasta luego"]
    while True:
        message = Prompt.ask(f"[bold] :sunglasses: {user} [/bold]")
        if message.lower() in exit_on:
            break

        # El agente procesa el mensaje y muestra la respuesta (con stream y markdown)
        agent.print_response(message=message, stream=True, markdown=True)
        #print_messages(agent)


if __name__ == "__main__":
    typer.run(main())