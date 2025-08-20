"""
User repository for user management operations
"""

from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from passlib.context import CryptContext
import structlog

from .base import BaseRepository
from app.models.user import User, UserRole

logger = structlog.get_logger()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserRepository(BaseRepository[User, dict, dict]):
    """User repository with user-specific operations"""
    
    def __init__(self):
        super().__init__(User)
    
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        try:
            stmt = select(User).where(User.email == email)
            result = db.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error("Error getting user by email", email=email, error=str(e))
            raise
    
    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        """Get user by username"""
        try:
            stmt = select(User).where(User.username == username)
            result = db.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error("Error getting user by username", username=username, error=str(e))
            raise
    
    def get_active_users(self, db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all active users"""
        try:
            stmt = select(User).where(User.is_active == True).offset(skip).limit(limit)
            result = db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            logger.error("Error getting active users", error=str(e))
            raise
    
    def get_users_by_role(self, db: Session, role: UserRole, skip: int = 0, limit: int = 100) -> List[User]:
        """Get users by role"""
        try:
            stmt = select(User).where(User.role == role).offset(skip).limit(limit)
            result = db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            logger.error("Error getting users by role", role=role.value, error=str(e))
            raise
    
    def create_user(self, db: Session, user_data: dict) -> User:
        """Create a new user with hashed password"""
        try:
            # Hash the password if provided
            if 'password' in user_data:
                user_data['password_hash'] = pwd_context.hash(user_data.pop('password'))
            
            # Create user instance
            user = User(**user_data)
            db.add(user)
            db.commit()
            db.refresh(user)
            
            logger.info("User created successfully", user_id=user.id, email=user.email)
            return user
        except Exception as e:
            db.rollback()
            logger.error("Error creating user", error=str(e))
            raise
    
    def update_user(self, db: Session, user_id: int, update_data: dict) -> Optional[User]:
        """Update user with optional password hashing"""
        try:
            user = db.get(User, user_id)
            if not user:
                return None
            
            # Hash password if provided
            if 'password' in update_data:
                update_data['password_hash'] = pwd_context.hash(update_data.pop('password'))
            
            # Update fields
            for field, value in update_data.items():
                if hasattr(user, field):
                    setattr(user, field, value)
            
            db.add(user)
            db.commit()
            db.refresh(user)
            
            logger.info("User updated successfully", user_id=user.id)
            return user
        except Exception as e:
            db.rollback()
            logger.error("Error updating user", user_id=user_id, error=str(e))
            raise
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    def authenticate_user(self, db: Session, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password"""
        try:
            user = self.get_by_email(db, email)
            if not user:
                return None
            
            if not self.verify_password(password, user.password_hash):
                return None
            
            if not user.is_active:
                return None
            
            # Update last login
            user.last_login = User.updated_at.default.arg()
            db.add(user)
            db.commit()
            
            logger.info("User authenticated successfully", user_id=user.id, email=email)
            return user
        except Exception as e:
            logger.error("Error authenticating user", email=email, error=str(e))
            raise
    
    def deactivate_user(self, db: Session, user_id: int) -> bool:
        """Deactivate a user"""
        try:
            user = db.get(User, user_id)
            if not user:
                return False
            
            user.is_active = False
            db.add(user)
            db.commit()
            
            logger.info("User deactivated", user_id=user_id)
            return True
        except Exception as e:
            db.rollback()
            logger.error("Error deactivating user", user_id=user_id, error=str(e))
            raise
    
    def change_user_role(self, db: Session, user_id: int, new_role: UserRole) -> Optional[User]:
        """Change user role"""
        try:
            user = db.get(User, user_id)
            if not user:
                return None
            
            user.role = new_role
            db.add(user)
            db.commit()
            db.refresh(user)
            
            logger.info("User role changed", user_id=user_id, new_role=new_role.value)
            return user
        except Exception as e:
            db.rollback()
            logger.error("Error changing user role", user_id=user_id, new_role=new_role.value, error=str(e))
            raise
