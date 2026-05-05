# 🧊 Smart Fridge AI API

API desarrollada con **FastAPI** y **YOLO (Ultralytics)** para detectar ingredientes dentro de imágenes de neveras. Ideal para proyectos de cocina inteligente, reducción de desperdicio o generación automática de recetas.

---

## 🚀 Características

* 📸 Detección de ingredientes a partir de imágenes
* 🤖 Modelo de visión artificial basado en YOLO
* ⚡ API rápida y ligera con FastAPI
* 🌍 CORS habilitado (modo desarrollo)
* 📦 Respuesta estructurada con bounding boxes y confianza

---

## 🧠 ¿Cómo funciona?

1. El usuario sube una imagen (foto de una nevera)
2. La API procesa la imagen con el modelo YOLO
3. Se detectan objetos (ingredientes)
4. Se devuelve:

   * Lista de ingredientes únicos
   * Detalles de cada detección (confianza + coordenadas)

---

## 📁 Estructura del proyecto

```
.
├── models/
│   └── best.pt          # Modelo YOLO entrenado
├── main.py              # Código principal de la API
└── README.md
```

---

## ⚙️ Instalación

### 1. Clonar el repositorio

```bash
git clone <tu-repo>
cd smart-fridge-api
```

### 2. Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows
```

### 3. Instalar dependencias

```bash
pip install fastapi uvicorn ultralytics pillow
```

---

## ▶️ Ejecución

```bash
python main.py
```

La API estará disponible en:

```
http://localhost:8000
```

Documentación automática (Swagger UI):

```
http://localhost:8000/docs
```

---

## 📡 Endpoints

### 🔹 `GET /`

**Health check**

Comprueba que la API está funcionando.

**Respuesta:**

```json
{
  "status": "ok",
  "service": "smart-fridge-api",
  "num_classes": 20
}
```

---

### 🔹 `GET /classes`

Devuelve las clases (ingredientes) que el modelo puede detectar.

**Respuesta:**

```json
{
  "classes": ["milk", "egg", "apple", "cheese"]
}
```

---

### 🔹 `POST /detect`

Detecta ingredientes en una imagen.

#### 📥 Parámetros

* `file`: imagen (multipart/form-data)
* `confidence` *(opcional)*: umbral de confianza (0.0 - 1.0)

#### 📤 Respuesta

```json
{
  "ingredients": ["milk", "egg"],
  "detections": [
    {
      "ingredient": "milk",
      "confidence": 0.92,
      "bbox": {
        "x1": 120.5,
        "y1": 80.2,
        "x2": 300.1,
        "y2": 400.7
      }
    }
  ],
  "total_detections": 2,
  "image_size": {
    "width": 1024,
    "height": 768
  }
}
```

---

## 🔍 Detalles técnicos

### 📌 Carga del modelo

El modelo YOLO se carga **una sola vez al iniciar la app**, lo que mejora el rendimiento:

```python
model = YOLO("models/best.pt")
```

---

### 🖼 Procesamiento de imagen

* Se valida que el archivo sea una imagen
* Se convierte a formato RGB usando PIL
* Se ejecuta la inferencia

---

### 📦 Post-procesado

* Se recorren las detecciones del modelo
* Se extraen:

  * Clase (ingrediente)
  * Confianza
  * Bounding box
* Se eliminan duplicados para obtener ingredientes únicos

---

## ⚠️ Notas importantes

* 🔓 CORS está abierto (`*`) → **no usar así en producción**
* 📉 Ajusta el parámetro `confidence` para mejorar precisión
* 🧠 La calidad depende del entrenamiento del modelo (`best.pt`)

---

## 🛠 Futuras mejoras

* 🍳 Generación automática de recetas
* 🧾 Clasificación por categorías (lácteos, frutas, etc.)
* 📱 Integración con app móvil
* ☁️ Despliegue en la nube (Docker + GPU)

---

## 👨‍💻 Autor

Proyecto desarrollado como base para sistemas de **IA aplicada a alimentación inteligente**.

---

## 📄 Licencia

MIT License

---

✨ *Convierte tu nevera en un asistente inteligente.*
