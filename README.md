# Bazar Universal API

API REST para la aplicación PWA Bazar Universal, construida con FastAPI y SQLAlchemy.

## Características

- ✅ API REST completa con FastAPI
- ✅ Base de datos SQLAlchemy con SQLite (desarrollo) / PostgreSQL (producción)
- ✅ Modelos Pydantic para validación
- ✅ Operaciones CRUD para productos y ventas
- ✅ Búsqueda de productos
- ✅ Estadísticas de ventas
- ✅ Documentación automática con Swagger UI
- ✅ CORS configurado para frontend
- ✅ Preparado para deployment en Netlify/Railway

## Estructura del Proyecto

```
Api_Bazar_Universal/
├── app/
│   ├── api/
│   │   └── api_v1/
│   │       ├── endpoints/
│   │       │   ├── products.py
│   │       │   └── sales.py
│   │       └── api.py
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   ├── crud/
│   │   ├── crud_product.py
│   │   └── crud_sale.py
│   ├── models/
│   │   ├── product.py
│   │   └── sale.py
│   └── schemas/
│       ├── product.py
│       └── sale.py
├── data/
│   ├── products.json
│   └── init_db.py
├── .env
├── .env.example
├── main.py
├── requirements.txt
└── README.md
```

## Instalación Local

1. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

2. **Configurar variables de entorno:**
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

3. **Inicializar la base de datos:**
```bash
python data/init_db.py
```

4. **Ejecutar el servidor:**
```bash
python main.py
# o
uvicorn main:app --reload
```

5. **Acceder a la documentación:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints de la API

### Productos
- `GET /api/v1/products/` - Obtener todos los productos
- `GET /api/v1/products/search?q={query}` - Buscar productos
- `GET /api/v1/products/{id}` - Obtener producto específico
- `GET /api/v1/products/category/{category}` - Productos por categoría
- `POST /api/v1/products/` - Crear producto
- `PUT /api/v1/products/{id}` - Actualizar producto
- `DELETE /api/v1/products/{id}` - Eliminar producto

### Ventas
- `GET /api/v1/sales/` - Obtener todas las ventas con estadísticas
- `GET /api/v1/sales/stats` - Obtener solo estadísticas
- `GET /api/v1/sales/{id}` - Obtener venta específica
- `POST /api/v1/sales/` - Crear nueva venta
- `DELETE /api/v1/sales/{id}` - Eliminar venta

## Deployment

### Opción 1: Railway (Recomendado para API)

1. **Crear cuenta en Railway:** https://railway.app
2. **Conectar repositorio de GitHub**
3. **Configurar variables de entorno en Railway:**
   - `DATABASE_URL` - URL de PostgreSQL (Railway la proporciona automáticamente)
   - `ENVIRONMENT=production`
   - `CORS_ORIGINS=["https://tu-app.netlify.app"]`

4. **Railway detectará automáticamente Python y ejecutará:**
```bash
pip install -r requirements.txt
python main.py
```

### Opción 2: Render

1. **Crear cuenta en Render:** https://render.com
2. **Crear nuevo Web Service**
3. **Configurar:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`

### Base de Datos en la Nube

#### PostgreSQL en Railway (Gratis)
1. En Railway, añadir PostgreSQL addon
2. Copiar la DATABASE_URL generada
3. La base de datos se inicializará automáticamente

#### PostgreSQL en Supabase (Gratis)
1. Crear proyecto en https://supabase.com
2. Ir a Settings > Database
3. Copiar la connection string
4. Formato: `postgresql://user:pass@host:port/dbname`

## Variables de Entorno para Producción

```env
DATABASE_URL=postgresql://user:password@host:port/database
ENVIRONMENT=production
CORS_ORIGINS=["https://tu-frontend.netlify.app"]
API_V1_STR=/api/v1
PROJECT_NAME=Bazar Universal API
VERSION=1.0.0
```

## Conectar con el Frontend

En tu aplicación React, cambiar las URLs de la API:

```javascript
// Desarrollo
const API_BASE_URL = 'http://localhost:8000/api/v1'

// Producción
const API_BASE_URL = 'https://tu-api.railway.app/api/v1'
```

## Scripts de Base de Datos

### Inicializar con datos de ejemplo:
```bash
python data/init_db.py
```

### Reset completo de la base de datos:
```bash
rm bazar_universal.db  # Solo para SQLite local
python data/init_db.py
```

## Monitoreo y Logs

- Railway y Render proporcionan logs automáticamente
- Endpoint de salud: `GET /health`
- Métricas disponibles en el dashboard de la plataforma
