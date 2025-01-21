from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import replicate
import os
from dotenv import load_dotenv
import shutil

app = FastAPI()

load_dotenv()

api_token = os.getenv("REPLICATE_API_TOKEN")
replicate.Client(api_token=api_token)

class ImageRequest(BaseModel):
    prompt : str
    model : str

# Funcion que crea un nuevo modelo entrenado
def create_model(model_name : str, trigger_word : str, file_path: str):
    model = replicate.models.create(
        owner="travelinglos",
        name=f"{model_name}",
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

    return training

# Función para ejecutar replicate.run y la creacion de imagen
def create_trained_image(prompt: str, model : str)-> str:
    try:
        output = replicate.run(
            f"travelinglos/{model}",
            input={
                "model": "dev",
                "prompt": f"{prompt}",
                "go_fast": False,
                "lora_scale": 1,
                "megapixels": "1",
                "num_outputs": 1,
                "aspect_ratio": "1:1",
                "output_format": "png",
                "guidance_scale": 3,
                "output_quality": 100,
                "prompt_strength": 0.8,
                "extra_lora": "https://replicate.delivery/xezq/2zFIXstgEdpzB9pHuRj5tJKqrecs1U0lJUZOeNUVWVw8C55TA/trained_model.tar",
                "extra_lora_scale": 1,
                "num_inference_steps": 28
            }
        )
        return str(output[0])
    except Exception as e:
        raise RuntimeError(f"Error generating image: {e}")

@app.post("/create_model")
async def new_model(model_name: str, trigger_word: str, file: UploadFile = File(...)):
    file_path = f"./{file.filename}"
    try:
        # Guarda el archivo temporalmente
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Llama a la función `create_model` y pasa el archivo .zip temporal
        training = create_model(model_name, trigger_word, file_path)

        # Elimina el archivo temporal
        os.remove(file_path)

        # Devuelve un mensaje de éxito con código 200
        return {
            'flux_model' : f"{model_name}:{training.version}"
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

@app.post("/create_image")
async def create_image(request: ImageRequest):
    
    return create_trained_image(prompt=request.prompt, model=request.model)
