from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
from PIL import Image
import io

# Crear la app
app = FastAPI(
    title="Smart Fridge AI",
    description="API que detecta ingredientes en fotos de neveras",
    version="0.1.0"
)

# CORS abierto para desarrollo (en producción restringir)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cargar el modelo UNA SOLA VEZ al arrancar la app

model = YOLO("models/best.pt")
print(f"Modelo cargado. Clases disponibles: {len(model.names)}")


@app.get("/")
def root():
    """Endpoint de salud — comprueba que la API está viva."""
    return {
        "status": "ok",
        "service": "smart-fridge-api",
        "num_classes": len(model.names)
    }


@app.get("/classes")
def list_classes():
    """Devuelve la lista de ingredientes que el modelo sabe detectar."""
    return {"classes": list(model.names.values())}


@app.post("/detect")
async def detect_ingredients(
    file: UploadFile = File(...),
    confidence: float = 0.4
):
    """
    Recibe una imagen de nevera y devuelve los ingredientes detectados.

    Parámetros:
    - file: imagen (jpg, png, etc.)
    - confidence: umbral mínimo de confianza (0.0 a 1.0). Por defecto 0.4.
    """
    # Validar tipo de archivo
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="El archivo debe ser una imagen"
        )

    # Leer y abrir la imagen
    contents = await file.read()
    try:
        image = Image.open(io.BytesIO(contents)).convert("RGB")
    except Exception:
        raise HTTPException(status_code=400, detail="Imagen inválida o corrupta")

    # Inferencia con YOLO
    results = model.predict(image, conf=confidence, verbose=False)

    # Procesar las detecciones
    detections = []
    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            class_name = model.names[class_id]
            conf_score = float(box.conf[0])
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            detections.append({
                "ingredient": class_name,
                "confidence": round(conf_score, 3),
                "bbox": {
                    "x1": round(x1, 1),
                    "y1": round(y1, 1),
                    "x2": round(x2, 1),
                    "y2": round(y2, 1),
                }
            })

    # Lista única de ingredientes (sin duplicados, ordenada)
    unique_ingredients = sorted(set(d["ingredient"] for d in detections))

    return {
        "ingredients": unique_ingredients,
        "detections": detections,
        "total_detections": len(detections),
        "image_size": {"width": image.width, "height": image.height}
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)