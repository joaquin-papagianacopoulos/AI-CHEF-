import streamlit as st
from agents import *
import os

def main():
    st.title("Primer API con Agentes sin usar AI")
    
    PROVEEDORES = {
        "OpenAI": {
            "models": ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"],
            "api_key_name": "OPENAI_API_KEY",
            "help_url": "https://platform.openai.com/api-keys"
        },
        "Groq": {
            "models": ["groq/llama3-8b-8192", "groq/llama3-70b-8192", "groq/mixtral-8x7b-32768"],
            "api_key_name": "GROQ_API_KEY", 
            "help_url": "https://console.groq.com"
        },
        "Anthropic": {
            "models": ["anthropic/claude-3-sonnet-20240229", "anthropic/claude-3-haiku-20240307"],
            "api_key_name": "ANTHROPIC_API_KEY",
            "help_url": "https://console.anthropic.com"
        }
    }
    
    with st.sidebar:
        st.header("Configuración") 
        proveedor = st.selectbox(
            "Proveedor de IA:", 
            options=list(PROVEEDORES.keys()),
            help="Elige tu proveedor de modelos de IA preferido"
        )
        
        # Selector de modelo basado en proveedor
        modelos_disponibles = PROVEEDORES[proveedor]["models"]
        modelo = st.selectbox(
            f"Modelo de {proveedor}:", 
            options=modelos_disponibles,
            help=f"Modelos disponibles para {proveedor}"
        )
        
        api_key_name = PROVEEDORES[proveedor]["api_key_name"]
        help_url = PROVEEDORES[proveedor]["help_url"]
        
        api_key = st.text_input(
            f"{proveedor} API Key:", 
            type="password",
            help=f"Obtén tu API key en {help_url}"
        )
        
        if api_key:
            st.success(f"✅ {proveedor} configurado")
        else:
            st.warning(f"⚠️ Configura tu API key de {proveedor}")
        
        st.subheader("⚙️ Parámetros")
        temperature = st.slider("Creatividad (Temperature):", 0.0, 1.0, 0.7, 0.1)
        max_tokens = st.number_input("Máximo de tokens:", 500, 4000, 2000, 100)

    def crear_llm(proveedor, modelo, api_key, temperature, max_tokens):
        """Crea la configuración LLM para CrewAI + litellm"""
        
        # Configurar variable de entorno según el proveedor
        if proveedor == "OpenAI":
            os.environ["OPENAI_API_KEY"] = api_key
        elif proveedor == "Groq":
            os.environ["GROQ_API_KEY"] = api_key
        elif proveedor == "Anthropic":
            os.environ["ANTHROPIC_API_KEY"] = api_key
        
        # Retornar configuración con el modelo CON prefijo para litellm
        return {
            "model": modelo,  # Mantener prefijo: groq/llama3-8b-8192
            "api_key": api_key,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

    # Interface principal
    st.write("¡Dime qué ingredientes tienes y te daré una receta perfecta!")

    # Input del usuario
    ingredientes = st.text_input("Escribe los ingredientes que tienes (separados por comas):")

    if st.button("Crear la receta"):
        if not api_key:
            st.error(f"Por favor ingresa tu {proveedor} API KEY en la barra lateral.")
        elif not ingredientes.strip():
            st.error("Por favor ingresa los ingredientes o una instrucción para crear la receta")
        else:
            with st.spinner("El chef está creando tu receta..."):
                try:
                    llm_config = crear_llm(proveedor, modelo, api_key, temperature, max_tokens)
                    
                    # Debug info
                    st.write(f"Debug - Modelo: {llm_config['model']}")
                    st.write(f"Debug - Proveedor: {proveedor}")
                    
                    # Crear y ejecutar crew
                    crew = crear_receta(ingredientes, llm_config)
                    resultado = crew.kickoff()
                    
                    st.success("¡Receta lista!")
                    st.markdown("---")
                    st.markdown(resultado)
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.error("Verifica que tu API key sea correcta y que tengas saldo disponible.").write(f"Debug - Proveedor: {proveedor}")
                    
                    # Crear y ejecutar crew
                    crew = crear_receta(ingredientes, llm_config)
                    resultado = crew.kickoff()
                    
                    st.success("¡Receta lista!")
                    st.markdown("---")
                    st.markdown(resultado)
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.error("Verifica que tu API key sea correcta y que tengas saldo disponible.")

if __name__ == "__main__":
    main()