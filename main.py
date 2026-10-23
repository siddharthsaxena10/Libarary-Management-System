from fastapi import FastAPI

# Teacher router
from app.routes.teacher import router as teacher_router

# Employee router
from app.routes.employee import router as employee_router

# Shop router
from app.routes.shop import router as shop_router

# Author router
from app.routes.author import router as author_router

# Books router
from app.routes.books import router as books_router

# Department router
from app.routes.department import router as department_router

# Student router
from app.routes.student import router as student_router

# Admin router
from app.routes.admin import router as admin_router

# Book Copy router
from app.routes.book_copy import router as book_copy_router

from app.routes.book_issue import router as book_issue_router

from app.routes.fine_payment import router as fine_payment_router


# FastAPI application
app = FastAPI(
    title="Library Management System",
    description="API for managing books, authors, students, and book issues.",
    version="1.0.0"
)

# Register all required routers
app.include_router(teacher_router)
app.include_router(employee_router)
app.include_router(shop_router)
app.include_router(author_router)
app.include_router(books_router)
app.include_router(department_router)
app.include_router(student_router)
app.include_router(admin_router)
app.include_router(book_copy_router)
app.include_router(book_issue_router)
app.include_router(fine_payment_router)
