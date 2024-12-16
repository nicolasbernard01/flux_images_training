from fastapi import FastAPI, File, UploadFile, HTTPException
import asyncio
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

# Funcion que crea un nuevo modelo entrenado
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

# Función para ejecutar replicate.run y la creacion de imagen
def create_trained_image(prompt: str)-> str:
    
    output = replicate.run(
    "travelinglos/fanta-lemon:3474c31a696bc0d0fbe034d544f0c43985c180a34e256f7a6e01136fe7b831ef",
        input={
            "model": "dev",
            "prompt": f"""
            {prompt}.
            Negative Prompt:
            No distortions or deformities in figures, no unnatural body proportions or poses, 
            no unmentioned elements such as weapons, animals, or unrelated objects, 
            no anachronistic clothing or accessories, no incorrect or inconsistent logos or text, 
            no unrealistic colors in any elements, no exaggerated lighting or inconsistent shadows, 
            no blurry or low-resolution details. 
            All objects and features must appear natural, seamless, and accurately integrated into the context. 
            The overall image should maintain balance and realism, avoiding clutter, irrelevant elements, or visual distractions, 
            ensuring a clean and harmonious final composition.
            """,
            "go_fast": False,
            "lora_scale": 1,
            "megapixels": "1",
            "num_outputs": 1,
            "aspect_ratio": "1:1",
            "output_format": "webp",
            "guidance_scale": 3,
            "output_quality": 80,
            "prompt_strength": 0.8,
            "extra_lora" : "https://replicate.delivery/xezq/2zFIXstgEdpzB9pHuRj5tJKqrecs1U0lJUZOeNUVWVw8C55TA/trained_model.tar",
            "extra_lora_scale": 1,
            "num_inference_steps": 28
        }
    )
    return str(output[0])

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

@app.post("/create_image")
async def create_image(request: ImageRequest):
    
    return create_trained_image(prompt=request)
