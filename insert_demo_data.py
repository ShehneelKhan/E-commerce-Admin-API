from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from models import Product, Inventory, Sale
from random import randint


DATABASE_URL = 'mysql+pymysql://root:admin@localhost:3306/ecommerce'
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def populate_database():
    db = SessionLocal()
    products = [
        Product(product_name=f"Product_{i}", price=randint(50, 500))
        for i in range(1, 101) 
    ]

    db.add_all(products)
    db.commit()


    inventory_items = [
        Inventory(product_id=product.product_id, quantity=randint(10, 100))
        for product in products
    ]

    db.add_all(inventory_items)
    db.commit()


    sales = [
        Sale(
            product_id=product.product_id,
            quantity_sold=randint(1, 20),
            total_amount=product.price * randint(1, 20),
            sale_date=datetime.now() - timedelta(days=randint(1, 365)),
        )
        for product in products
    ]

    db.add_all(sales)
    db.commit()


    db.close()

if __name__ == "__main__":
    populate_database()
