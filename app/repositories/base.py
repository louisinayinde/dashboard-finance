"""
Base repository with common CRUD operations
"""

from typing import Generic, TypeVar, Type, Optional, List, Any, Dict
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from pydantic import BaseModel
import structlog

from app.core.database import Base

logger = structlog.get_logger()

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Base repository with common CRUD operations"""
    
    def __init__(self, model: Type[ModelType]):
        self.model = model
    
    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """Get a single record by ID"""
        try:
            stmt = select(self.model).where(self.model.id == id)
            result = db.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error("Error getting record by ID", model=self.model.__name__, id=id, error=str(e))
            raise
    
    def get_multi(
        self, 
        db: Session, 
        *, 
        skip: int = 0, 
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[ModelType]:
        """Get multiple records with pagination and filters"""
        try:
            stmt = select(self.model)
            
            # Apply filters if provided
            if filters:
                for field, value in filters.items():
                    if hasattr(self.model, field):
                        stmt = stmt.where(getattr(self.model, field) == value)
            
            stmt = stmt.offset(skip).limit(limit)
            result = db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            logger.error("Error getting multiple records", model=self.model.__name__, error=str(e))
            raise
    
    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        """Create a new record"""
        try:
            # Convert Pydantic model to dict or use as-is if already a dict
            if hasattr(obj_in, 'model_dump'):
                obj_data = obj_in.model_dump()
            elif hasattr(obj_in, 'dict'):
                obj_data = obj_in.dict()
            else:
                obj_data = obj_in
            
            # Create SQLAlchemy model instance
            db_obj = self.model(**obj_data)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            
            logger.info("Record created successfully", model=self.model.__name__, id=db_obj.id)
            return db_obj
        except Exception as e:
            db.rollback()
            logger.error("Error creating record", model=self.model.__name__, error=str(e))
            raise
    
    def update(
        self, 
        db: Session, 
        *, 
        db_obj: ModelType, 
        obj_in: UpdateSchemaType | Dict[str, Any]
    ) -> ModelType:
        """Update an existing record"""
        try:
            # Convert Pydantic model to dict if needed
            if hasattr(obj_in, 'model_dump'):
                update_data = obj_in.model_dump(exclude_unset=True)
            elif isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.dict(exclude_unset=True)
            
            # Update the object
            for field, value in update_data.items():
                if hasattr(db_obj, field):
                    setattr(db_obj, field, value)
            
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            
            logger.info("Record updated successfully", model=self.model.__name__, id=db_obj.id)
            return db_obj
        except Exception as e:
            db.rollback()
            logger.error("Error updating record", model=self.model.__name__, id=db_obj.id, error=str(e))
            raise
    
    def remove(self, db: Session, *, id: int) -> ModelType:
        """Delete a record by ID"""
        try:
            obj = db.get(self.model, id)
            if obj:
                db.delete(obj)
                db.commit()
                logger.info("Record deleted successfully", model=self.model.__name__, id=id)
                return obj
            else:
                logger.warning("Record not found for deletion", model=self.model.__name__, id=id)
                return None
        except Exception as e:
            db.rollback()
            logger.error("Error deleting record", model=self.model.__name__, id=id, error=str(e))
            raise
    
    def exists(self, db: Session, id: Any) -> bool:
        """Check if a record exists by ID"""
        try:
            stmt = select(self.model.id).where(self.model.id == id)
            result = db.execute(stmt)
            return result.scalar_one_or_none() is not None
        except Exception as e:
            logger.error("Error checking record existence", model=self.model.__name__, id=id, error=str(e))
            raise
    
    def count(self, db: Session, filters: Optional[Dict[str, Any]] = None) -> int:
        """Count total records with optional filters"""
        try:
            stmt = select(self.model)
            
            if filters:
                for field, value in filters.items():
                    if hasattr(self.model, field):
                        stmt = stmt.where(getattr(self.model, field) == value)
            
            result = db.execute(stmt)
            return len(result.scalars().all())
        except Exception as e:
            logger.error("Error counting records", model=self.model.__name__, error=str(e))
            raise
