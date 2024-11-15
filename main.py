from fastapi import FastAPI, File, UploadFile
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

    training = replicate.trainings.create(
    version="ostris/flux-dev-lora-trainer:4ffd32160efd92e956d39c5338a9b8fbafca58e03f791f6d8011f3e20e8ea6fa",
    input={
        "input_images": file_path,  # Ruta al archivo de imágenes de entrenamiento en formato .zip
        "steps": 1000,  # Número de pasos para el entrenamiento

    },
    destination=f"{model.owner}/{model.name}"  # Establece el modelo como destino para el entrenamiento
)
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

    # Imprime el estado inicial del entrenamiento
    print(f"Training started: {training.status}")
    print(f"Training URL: https://replicate.com/p/{training.id}")


@app.post("/create_model")
def new_model(username : str, trigger_word : str, file : UploadFile = File(...)):
    file_path = f"./{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Llama a la función `create_model` y pasa el archivo .zip temporal
    result = create_model(username, trigger_word, file_path)

    # Elimina el archivo temporal
    os.remove(file_path)

    return result