# filepath: /home/agustin/Escritorio/Escritorio/Documentos/challenges/pwc/burger_project/app/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.auth import (
    authenticate_user, create_access_token, get_current_active_user,
    ACCESS_TOKEN_EXPIRE_MINUTES, Token
)
from app.routers import burger, store, promotion, ingredient
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from app.middleware import correlation_id

app = FastAPI()

app.state.limiter = Limiter(key_func=get_remote_address)
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(correlation_id.CorrelationIdMiddleware)

app.include_router(burger.router,
                   prefix="/burger",
                   tags=["Burger"],
                   dependencies=[Depends(get_current_active_user)])

app.include_router(ingredient.router,
                   prefix="/ingredient",
                   tags=["Ingredient"],
                   dependencies=[Depends(get_current_active_user)])

app.include_router(promotion.router,
                   prefix="/promotion",
                   tags=["Promotion"],
                   dependencies=[Depends(get_current_active_user)])

app.include_router(store.router,
                   prefix="/store",
                   tags=["Store"],
                   dependencies=[Depends(get_current_active_user)])

@app.get("/", tags=["Root"])
def read_root():
    return {"Hello": "World!"}

@app.post("/token", response_model=Token, tags=["Root"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}

@app.get("/version", tags=["Version"])
def get_version():
    return {"version": "1.0.0"}
