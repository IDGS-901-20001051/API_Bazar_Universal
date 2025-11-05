# 📝 GUÍA PASO A PASO: Deployment de Bazar Universal

## 🎯 Resumen del Proyecto

Has creado exitosamente:
- ✅ **Frontend PWA** en React + Vite (puerto 5174)
- ✅ **API REST** en Python + FastAPI (puerto 8000)
- ✅ **Base de datos** SQLite (desarrollo) / PostgreSQL (producción)
- ✅ **Integración completa** Frontend ↔ API

---

## 🚀 PASO 1: Preparar el Deployment de la API

### Opción A: Railway (Recomendado - GRATIS)

1. **Crear cuenta**: https://railway.app
2. **Conectar GitHub**:
   - Haz push de tu código a GitHub
   - Conecta tu repositorio en Railway
3. **Configurar variables de entorno**:
   ```
   DATABASE_URL=postgresql://... (Railway lo genera automáticamente)
   ENVIRONMENT=production
   CORS_ORIGINS=["https://tu-frontend.netlify.app"]
   ```
4. **Railway detectará automáticamente** el archivo `railway.json`

### Opción B: Render (Alternativa GRATUITA)

1. **Crear cuenta**: https://render.com
2. **Nuevo Web Service** desde GitHub
3. **Configurar**:
   - Build Command: `pip install -r requirements.txt && python data/init_db.py`
   - Start Command: `python start.py`

---

## 🗄️ PASO 2: Base de Datos en la Nube (GRATIS)

### Opción A: Railway PostgreSQL (Recomendado)
- Railway añade automáticamente PostgreSQL
- Copia la `DATABASE_URL` generada
- ✅ Se inicializa automáticamente

### Opción B: Supabase PostgreSQL
1. **Crear proyecto**: https://supabase.com
2. **Settings > Database**
3. **Copiar Connection String**:
   ```
   postgresql://postgres:[PASSWORD]@[HOST]:5432/postgres
   ```

### Opción C: PlanetScale (MySQL)
1. **Crear cuenta**: https://planetscale.com
2. **Crear base de datos**
3. **Copiar connection string**

---

## 🌐 PASO 3: Deployment del Frontend

### Netlify (Recomendado - GRATIS)

1. **Crear cuenta**: https://netlify.com
2. **Conectar repositorio** de GitHub
3. **Configurar build**:
   - Build command: `npm run build`
   - Publish directory: `dist`
4. **Variables de entorno**:
   ```
   VITE_API_URL=https://tu-api.railway.app/api/v1
   ```

### Vercel (Alternativa)
1. **Crear cuenta**: https://vercel.com
2. **Import proyecto** desde GitHub
3. **Configurar**:
   - Framework: Vite
   - Output directory: `dist`

---

## 🔧 PASO 4: Configuración Final

### 1. Actualizar URLs en el Frontend

Edita `src/services/apiService.js`:
```javascript
const API_BASE_URL = import.meta.env.PROD 
  ? 'https://TU-API-RAILWAY.railway.app/api/v1'  // 👈 Cambiar por tu URL
  : 'http://localhost:8000/api/v1'
```

### 2. Actualizar CORS en la API

En tu API desplegada, actualiza las variables de entorno:
```
CORS_ORIGINS=["https://tu-frontend.netlify.app"]
```

---

## 🧪 PASO 5: Testing Local

### Servidor de API (Puerto 8000):
```bash
cd "Api_Bazar_Universal"
pip install -r requirements.txt
python data/init_db.py
python main.py
```

### Servidor Frontend (Puerto 5174):
```bash
cd "Bazar Universal"
npm install
npm run dev
```

### 🎯 Pruebas:
- ✅ Frontend: http://localhost:5174
- ✅ API Docs: http://localhost:8000/docs
- ✅ Health Check: http://localhost:8000/health

---

## 📋 CHECKLIST Final

### Pre-Deployment:
- [ ] Código subido a GitHub
- [ ] Variables de entorno configuradas
- [ ] URLs actualizadas en apiService.js

### Deployment API:
- [ ] Railway/Render conectado
- [ ] Base de datos PostgreSQL creada
- [ ] API funcionando (verificar /health)
- [ ] Datos iniciales cargados

### Deployment Frontend:
- [ ] Netlify/Vercel conectado
- [ ] Build exitoso
- [ ] Variables de entorno configuradas
- [ ] CORS configurado en API

### Testing Final:
- [ ] Búsqueda de productos funciona
- [ ] Detalle de producto funciona
- [ ] Agregar a compras funciona
- [ ] Historial de compras funciona
- [ ] PWA instalable

---

## 🆘 Resolución de Problemas

### Error de CORS:
```javascript
// En API: actualizar CORS_ORIGINS
CORS_ORIGINS=["https://tu-frontend.netlify.app", "http://localhost:5174"]
```

### Error de Base de Datos:
```bash
# Verificar conexión
python data/init_db.py
```

### Error de Build Frontend:
```bash
# Limpiar cache
rm -rf node_modules dist
npm install
npm run build
```

---

## 🎉 URLs Finales

Una vez deployado tendrás:

- 🌐 **Frontend PWA**: https://tu-app.netlify.app
- 🔌 **API REST**: https://tu-api.railway.app
- 📚 **API Docs**: https://tu-api.railway.app/docs
- 💾 **Base de Datos**: PostgreSQL en la nube

---

## 💡 Próximos Pasos

1. **Monitoreo**: Configurar logs y métricas
2. **Dominio personalizado**: Configurar tu propio dominio
3. **CI/CD**: Automatizar deployments
4. **Analytics**: Añadir Google Analytics
5. **Performance**: Optimizar carga y SEO

---

**¡Tu aplicación PWA Bazar Universal está lista para producción! 🚀**
