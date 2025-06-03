from crewai import Agent, Task, Crew
from crewai.llm import LLM
import os
from dotenv import load_dotenv

def crear_receta(ingredientes, llm_config):
    """
    Crear receta usando CrewAI con configuración litellm
    llm_config debe ser un diccionario con: model, api_key, temperature, max_tokens
    """
    
    # Configurar variables de entorno
    if "groq/" in llm_config["model"]:
        os.environ["GROQ_API_KEY"] = llm_config["api_key"]
    elif "gpt-" in llm_config["model"]:
        os.environ["OPENAI_API_KEY"] = llm_config["api_key"]
    elif "claude-" in llm_config["model"]:
        os.environ["ANTHROPIC_API_KEY"] = llm_config["api_key"]
    
    # Crear LLM de CrewAI que usa litellm internamente
    llm = LLM(
        model=llm_config["model"],  # Con prefijo: groq/llama3-8b-8192
        temperature=llm_config["temperature"],
        max_tokens=llm_config["max_tokens"],
        api_key=llm_config["api_key"]
    )
    
    ## Agentes especializados
    chef = Agent(
        role='Chef',
        goal='Pensar paso a paso sobre una receta de cocina o pastelería y devolver la receta completa en un formato legible para un humano.',
        backstory=f'Un chef especialista en cocina y pasteleria, con una buena comprension de ideas para recetas. Quiero que hables como un argentino, con chistes y frases argentinas',
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

    ## Tareas
    devolver_idea = Task(
        description=f"""Dar una idea sobre una receta de cocina o pasteleria usando estos ingredientes o instrucciones: {ingredientes}. 
        Debe devolver al menos 5 pasos sobre como llevar a cabo la receta, pensada paso a paso para el ser humano.
        Quiero que hables como un argentino, con frases argentinas, pero no te pases""",
        agent=chef,
        expected_output="Una lista de pasos detallados para preparar una receta, en el idioma en el cual se hayan ingresado los ingredientes. En el caso de que sea en español, quiero que contestes como un argentino, con frases argentinas. "
    )

    crew = Crew(
        agents=[chef],
        tasks=[devolver_idea],
        verbose=True,
        process="sequential"
    )
    
    return crew