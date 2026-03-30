# KLEOS Ecommerce API

Backend para la tienda local de deportes KLEOS.

## Tecnologias
- FastAPI
- PostgreSQL
- Docker

## Como ejecutar

1. Levantar base de datos:

```bash
docker compose up -d
```

2. Ejecutar backend:

```bash
uvicorn app.main:app --reload
```
