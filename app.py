from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Modèle de données entrant
class RequestModel(BaseModel):
    message: str

# Modèle de données sortant
class ResponseModel(BaseModel):
    response: str

# Exemple: fonction IA que tu dois adapter/importer
def morceau_ia(message: str) -> str:
    # Ici tu dois mettre ta logique IA qui reçoit message, renvoie réponse
    # Exemple simple:
    return f"Je réponds à : {message}"

# Route POST /ask pour poser une question à l'IA
@app.post("/ask", response_model=ResponseModel)
async def ask_ia(request: RequestModel):
    reponse_ia = morceau_ia(request.message)
    return ResponseModel(response=reponse_ia)
