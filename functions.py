from agents import *

def function(result):
    # Podrías pasarle el input como contexto a la Crew si configurás `Task.input`
    result = crew.kickoff()
    print(result)
    return result  # <- para mostrarlo en el chat
