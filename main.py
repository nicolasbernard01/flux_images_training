from fastapi import FastAPI, File, UploadFile, HTTPException
import replicate
import os
from dotenv import load_dotenv
import shutil

app = FastAPI()

load_dotenv()

api_token = os.getenv("REPLICATE_API_TOKEN")
replicate.Client(api_token=api_token)

def create_model(username : str, trigger_word : str, file_path: str):
    model = replicate.models.create(
        owner="travelinglos",
        name=f"{username}",
        visibility="private",
        hardware="gpu-t4",
        description="A fine-tuned FLUX.1 model"
    )

    # Imprimir detalles del modelo
    print(f"Model created: {model.name}")

    with open(file_path, "rb") as file:
        training = replicate.trainings.create(
            version="ostris/flux-dev-lora-trainer:4ffd32160efd92e956d39c5338a9b8fbafca58e03f791f6d8011f3e20e8ea6fa",
            input={
                "input_images": file,  # Archivo .zip con las imágenes de entrenamiento
                "steps": 1000,  # Número de pasos para el entrenamiento
                "trigger_word": f"{trigger_word}"
            },
            destination=f"{model.owner}/{model.name}"
        )


@app.post("/create_model")
async def new_model(username: str, trigger_word: str, file: UploadFile = File(...)):
    file_path = f"./{file.filename}"
    try:
        # Guarda el archivo temporalmente
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Llama a la función `create_model` y pasa el archivo .zip temporal
        create_model(username, trigger_word, file_path)

        # Elimina el archivo temporal
        os.remove(file_path)

        # Devuelve un mensaje de éxito con código 200
        return {
            "success": True,
            "message": "Model created and training started successfully."
        }
    except Exception as e:
        # Maneja errores y devuelve un código HTTP 400 (Bad Request)
        raise HTTPException(
            status_code=400,
            detail={
                "success": False,
                "message": f"An error occurred: {str(e)}"
            }
        )