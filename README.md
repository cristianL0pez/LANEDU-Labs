# LANEDU Labs Backend

Backend de LANEDU Labs construido con FastAPI, PostgreSQL y Docker Compose. Incluye modelos, migraciones con Alembic, esquemas Pydantic, servicios y routers básicos (auth MVP, usuarios, labs, progreso y ranking).

## Requisitos
- Docker y Docker Compose
- Opcional: Python 3.11+ y pip (para correr comandos locales)

## Puesta en marcha rápida
```bash
docker compose up --build
```
La API quedará disponible en `http://localhost:8000`.

## Migraciones con Alembic
- Aplicar todas las migraciones:
  ```bash
  docker compose run --rm api alembic upgrade head
  ```
- Generar una nueva migración (autogenerate):
  ```bash
  docker compose run --rm api alembic revision --autogenerate -m "descripcion_corta"
  ```

## Seed de labs iniciales
```bash
docker compose exec api python -m app.db.seed_labs
```
(El script es idempotente: no duplica labs si ya existen.)

## Endpoints principales (MVP)
- `POST /auth/register` – crear usuario
- `POST /auth/login` – login simple por username (token simulado)
- `GET /users/me` – perfil del usuario autenticado (auth fake)
- `GET /labs` – lista labs con estado
- `GET /labs/{lab_id}` – detalle de un lab
- `POST /progress/complete` – completar un lab (requiere `lab_id` y `doc_url`)
- `GET /ranking` – top usuarios por XP
- `GET /health` – health check

## Checklist de pruebas manuales (curl/Postman)
1) Registro de usuario  
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","email":"alice@example.com"}'
```

2) Login (token simulado)  
```bash
curl -X POST 'http://localhost:8000/auth/login?username=alice'
```

3) Perfil `/users/me` (usa auth fake: siempre usuario 1)  
```bash
curl http://localhost:8000/users/me
```

4) Listar labs  
```bash
curl http://localhost:8000/labs
```

5) Detalle de un lab  
```bash
curl http://localhost:8000/labs/1
```

6) Completar lab (requiere `lab_id` y `doc_url`)  
```bash
curl -X POST http://localhost:8000/progress/complete \
  -H "Content-Type: application/json" \
  -d '{"lab_id":1,"doc_url":"https://example.com/entrega"}'
```

7) Ranking  
```bash
curl http://localhost:8000/ranking
```

> Nota: la autenticación es un MVP; los endpoints usan dependencias fake que devuelven siempre el mismo usuario. Sustituir por JWT/OAuth2 en producción.
