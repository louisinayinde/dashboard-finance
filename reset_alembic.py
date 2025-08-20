#!/usr/bin/env python3
"""
Reset Alembic and recreate tables
"""

from app.core.database import engine, drop_tables, create_tables
from sqlalchemy import text

def main():
    print("Resetting Alembic and database...")
    
    # Drop alembic version table
    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS alembic_version CASCADE"))
        conn.commit()
        print("✅ Alembic version table dropped")
    
    # Drop all tables
    drop_tables()
    print("✅ All tables dropped")
    
    # Recreate all tables
    create_tables()
    print("✅ All tables recreated")
    
    print("🎉 Database reset completed!")

if __name__ == "__main__":
    main()
