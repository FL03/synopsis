from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from jose import JWTError, jwt

from synopsis.core.session import Session
from synopsis.data.models.tokens import Token, TokenData
from synopsis.data.models.users import User, Users

session: Session = Session()
constants = session.authorization
router: APIRouter = APIRouter(prefix="/oauth", tags=["oauth"])


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": form_data.username},
        expires_delta=timedelta(minutes=constants.expiration)
    )
    return Token(access_token=access_token, token_type="bearer")


def verify_password(plain_password, hashed_password):
    return constants.context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return constants.context.hash(password)


async def get_user(username: str):
    res = await User.from_queryset(Users.all())
    for user in res:
        if user["username"] == username:
            return await User.from_queryset_single(Users.get(username=username))
        else:
            return None


async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, session.settings.access_token, algorithm=constants.algorithm)
    return encoded_jwt


async def get_current_user(token: str = Depends(constants.scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, session.settings.access_token, algorithms=[constants.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if await current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return await get_user(username=current_user.username)
