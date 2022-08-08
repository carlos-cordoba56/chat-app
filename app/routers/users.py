from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app.database.database import get_db
from app import utils
from app.routers.schemas import UserResponce, User
from app.database import models

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserResponce)
def create_user(user: User, db: Session = Depends(get_db)):
    
    user.password = utils.hash(user.password)

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get( '/{id}', response_model=UserResponce )
def get_user( id: int, db: Session = Depends(get_db) ):
    user = db.query(models.User).filter(models.User.id == id).first()
    return user
    if not user:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, 
                             detail=f'user with id={id} does not exist' )
