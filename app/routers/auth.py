from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import utils
from app import oauth2
from app.database import models
from app.database.database import get_db


router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login( user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db) ):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException( status_code=status.HTTP_403_FORBIDDEN, detail=f'invalid credentials' )
    
    if utils.verify(user_credentials.password, user.password):
        # create an acces token
        access_token = oauth2.create_access_token(data={"user_id": user.id})
        return {'access_token': access_token,  'token_type': 'bearer'}
    else:
        raise HTTPException( status_code=status.HTTP_403_FORBIDDEN, detail=f'invalid credentials' )
    