from fastapi import FastAPI
import models
from database import engine
from sqlalchemy import or_
from routers import todo
from fastapi.responses import HTMLResponse

app = FastAPI(title="To-Do App")
models.Base.metadata.create_all(engine)

app.include_router(todo.router)

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>To-Do API</title>
        <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>✅</text></svg>">

        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #0f172a, #1e293b);
                color: white;
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
            }

            .container {
                text-align: center;
                background: rgba(255,255,255,0.08);
                backdrop-filter: blur(10px);
                padding: 50px;
                border-radius: 20px;
                width: 90%;
                max-width: 700px;
                box-shadow: 0 15px 40px rgba(0,0,0,0.3);
            }

            .logo {
                font-size: 60px;
                margin-bottom: 15px;
            }

            h1 {
                font-size: 42px;
                margin-bottom: 15px;
            }

            p {
                color: #cbd5e1;
                font-size: 18px;
                line-height: 1.6;
                margin-bottom: 30px;
            }

            .badge {
                display: inline-block;
                padding: 8px 16px;
                background: rgba(59,130,246,0.2);
                border: 1px solid #3b82f6;
                border-radius: 50px;
                margin-bottom: 25px;
                color: #93c5fd;
                font-size: 14px;
            }

            .btn {
                display: inline-block;
                padding: 14px 28px;
                background: #2563eb;
                color: white;
                text-decoration: none;
                border-radius: 10px;
                font-weight: 600;
                transition: 0.3s;
            }

            .btn:hover {
                background: #1d4ed8;
                transform: translateY(-2px);
            }

            .footer {
                margin-top: 30px;
                color: #94a3b8;
                font-size: 14px;
            }
        </style>
    </head>

    <body>
        <div class="container">
            <div class="logo">✅</div>

            <div class="badge">
                FastAPI • SQLAlchemy • PostgreSQL
            </div>

            <h1>To-Do Management API</h1>

            <p>
                A RESTful To-Do application built with FastAPI,
                featuring CRUD operations, filtering,
                validation, and database persistence.
            </p>

            <a class="btn" href="/docs">
                View API Documentation
            </a>

            <div class="footer">
                Built with FastAPI 🚀
            </div>
        </div>
    </body>
    </html>
    """


# @app.get('/todos/search/',response_model = List[schemas.ToDo])
# def search_todos(q: str, db: Session = Depends(get_db)):
#     return db.query(models.ToDo).filter(
#         or_(
#             models.ToDo.title.ilike(f"%{q}%"),
#             models.ToDo.description.ilike(f"%{q}%")
#         )
#     ).all()

# @app.get("/todos/paginated")
# def get_paginated_todos(skip:int =0, limit: int = 10, db: Session = Depends(get_db)):
#     total = db.query(models.ToDo).count()
#     todos = db.query(models.ToDo).offset(skip).limit(limit).all()
#     return {"total": total, "skip": skip, "limit": limit,"data": todos}