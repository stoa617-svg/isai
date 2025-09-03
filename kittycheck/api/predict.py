from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse

app = FastAPI()

# Catálogo de desparasitantes con dosis estándar
DEWORMERS = {
    "Ivermectina 1%": {"unidad": "ml/kg", "dosis": 0.02},   # 0.2 ml / 10 kg
    "Fenbendazol": {"unidad": "mg/kg", "dosis": 50},
    "Pyrantel": {"unidad": "mg/kg", "dosis": 20},
    "Praziquantel": {"unidad": "mg/kg", "dosis": 5},
    "Milbemicina": {"unidad": "mg/kg", "dosis": 2},
}

class PredictionRequest(BaseModel):
    peso_gramos: float
    desparasitante: str

@app.post("/api/predict")
def predict_dosis(data: PredictionRequest):
    peso_kg = data.peso_gramos / 1000
    if data.desparasitante not in DEWORMERS:
        return JSONResponse(
            {"error": "Desparasitante no registrado"}, status_code=400
        )

    info = DEWORMERS[data.desparasitante]
    dosis = peso_kg * info["dosis"]

    return {
        "peso_gato": f"{peso_kg:.2f} kg",
        "desparasitante": data.desparasitante,
        "dosis_recomendada": f"{dosis:.3f} {info['unidad']}"
    }
