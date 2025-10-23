from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# Racine de test simple (GET /)
@app.get("/")
def read_root():
    return {"message": "API opérationnelle"}


# Modèle de données entrant
class RequestModel(BaseModel):
    message: str

# Modèle de données sortant
class ResponseModel(BaseModel):
    response: str

# Exemple de logique IA (à personnaliser)
def morceau_ia(message: str) -> str:
    # Remplace par ta logique plus complexe
    return f"Je réponds à : {message}"

# Route POST /ask
@app.post("/ask", response_model=ResponseModel)
async def ask_ia(request: RequestModel):
    reponse_ia = morceau_ia(request.message)
    return ResponseModel(response=reponse_ia)
