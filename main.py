from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
import models
from database import engine, SessionLocal
from sqlalchemy import func
import models
from datetime import datetime, timedelta, date

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class SaleCreate(BaseModel):
    product_id: int
    quantity_sold: int
    total_amount: float
    sale_date: date

class Sale(BaseModel):
    product_id: int
    quantity_sold: int
    total_amount: float
    sale_date: date 

class ProductCreate(BaseModel):
    product_name: str
    price: float

class Product(BaseModel):
    product_id: int
    product_name: str
    price: float

class InventoryUpdate(BaseModel):
    product_id: int
    quantity: int



@app.post("/sales/create", response_model=Sale)
def create_sale(sale: SaleCreate, db: Session = Depends(get_db)):
    # Create a new sale record in the database
    db_sale = models.Sale(**sale.model_dump())
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)

    # Update the inventory
    inventory_update = InventoryUpdate(product_id=sale.product_id, quantity=-sale.quantity_sold)
    update_inventory(inventory_update, db)

    return db_sale


@app.get("/sales/revenue")
def get_revenue(start_date: str, end_date: str, db: Session = Depends(get_db)):
    # Retrieve revenue data within the specified date range
    revenue = db.query(func.sum(models.Sale.total_amount)).filter(models.Sale.sale_date.between(start_date, end_date)).scalar()
    return {"revenue": revenue}



@app.get("/inventory")
def get_inventory(low_stock_threshold: int = Query(default=10, description="Low stock threshold"), db: Session = Depends(get_db)):
    # Retrieve current inventory status
    inventory = db.query(models.Inventory).all()

    # Check for low stock and include in response
    low_stock_alerts = [item for item in inventory if item.quantity < low_stock_threshold]

    if low_stock_alerts:
        response_data = {"inventory": inventory, "low_stock_alerts": low_stock_alerts}
    else:
        response_data = {"inventory": inventory}

    return response_data


@app.put("/inventory/update")
def update_inventory(inventory_update: InventoryUpdate, db: Session = Depends(get_db)):
    # Update inventory levels and track changes
    product_id = inventory_update.product_id
    quantity = inventory_update.quantity

    # Check if the product exists
    product = db.query(models.Product).filter(models.Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Update inventory
    existing_inventory = db.query(models.Inventory).filter(models.Inventory.product_id == product_id).first()

    if existing_inventory:
        existing_inventory.quantity += quantity
    else:
        new_inventory = models.Inventory(product_id=product_id, quantity=quantity)
        db.add(new_inventory)

    db.commit()

    return {"message": "Inventory updated successfully"}



@app.post("/products/register", response_model=Product)
def register_product(product: ProductCreate, db: Session = Depends(get_db)):
    # Register a new product
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product




@app.get("/sales")
def get_all_sales(db: Session = Depends(get_db)):
    # Retrieve all sales data
    all_sales = db.query(models.Sale).all()
    return all_sales


@app.get("/sales/daily")
def get_daily_sales(db: Session = Depends(get_db)):
    # Retrieve daily sales data
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    daily_sales = db.query(models.Sale).filter(models.Sale.sale_date.between(today, tomorrow)).all()
    return daily_sales

@app.get("/sales/weekly")
def get_weekly_sales(db: Session = Depends(get_db)):
    # Retrieve weekly sales data
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=7)
    weekly_sales = db.query(models.Sale).filter(models.Sale.sale_date.between(start_of_week, end_of_week)).all()
    return weekly_sales

@app.get("/sales/monthly")
def get_monthly_sales(db: Session = Depends(get_db)):
    # Retrieve monthly sales data
    today = datetime.now().date()
    start_of_month = today.replace(day=1)
    end_of_month = (start_of_month + timedelta(days=32)).replace(day=1)
    monthly_sales = db.query(models.Sale).filter(models.Sale.sale_date.between(start_of_month, end_of_month)).all()
    return monthly_sales

@app.get("/sales/annual")
def get_annual_sales(db: Session = Depends(get_db)):
    # Retrieve annual sales data
    today = datetime.now().date()
    start_of_year = today.replace(month=1, day=1)
    end_of_year = today.replace(month=12, day=31)
    annual_sales = db.query(models.Sale).filter(models.Sale.sale_date.between(start_of_year, end_of_year)).all()
    return annual_sales
    

@app.get("/sales/filter")
def filter_sales(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    product_id: Optional[int] = None,
    category: Optional[str] = None,
    quantity_sold_min: Optional[int] = None,
    quantity_sold_max: Optional[int] = None,
    total_amount_min: Optional[float] = None,
    total_amount_max: Optional[float] = None,
    db: Session = Depends(get_db)
):
    
    query = db.query(models.Sale)

    if start_date and end_date:
        query = query.filter(models.Sale.sale_date.between(start_date, end_date))

    if product_id:
        query = query.filter(models.Sale.product_id == product_id)

    if category:
        query = query.join(models.Product).filter(models.Product.product_category == category)

    if quantity_sold_min is not None:
        query = query.filter(models.Sale.quantity_sold >= quantity_sold_min)

    if quantity_sold_max is not None:
        query = query.filter(models.Sale.quantity_sold <= quantity_sold_max)

    if total_amount_min is not None:
        query = query.filter(models.Sale.total_amount >= total_amount_min)

    if total_amount_max is not None:
        query = query.filter(models.Sale.total_amount <= total_amount_max)

    filtered_sales = query.all()
    return filtered_sales


@app.get("/sales/analysis")
def analyze_sales(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    product_id: Optional[int] = None,
    category: Optional[str] = None,
    quantity_sold_min: Optional[int] = None,
    quantity_sold_max: Optional[int] = None,
    total_amount_min: Optional[float] = None,
    total_amount_max: Optional[float] = None,
    db: Session = Depends(get_db)
):
    
    query = db.query(models.Sale)

    if start_date and end_date:
        query = query.filter(models.Sale.sale_date.between(start_date, end_date))

    if product_id:
        query = query.filter(models.Sale.product_id == product_id)

    if category:
        query = query.join(models.Product).filter(models.Product.product_category == category)

    if quantity_sold_min is not None:
        query = query.filter(models.Sale.quantity_sold >= quantity_sold_min)

    if quantity_sold_max is not None:
        query = query.filter(models.Sale.quantity_sold <= quantity_sold_max)

    if total_amount_min is not None:
        query = query.filter(models.Sale.total_amount >= total_amount_min)

    if total_amount_max is not None:
        query = query.filter(models.Sale.total_amount <= total_amount_max)

    total_quantity_sold = query.with_entities(func.sum(models.Sale.quantity_sold)).scalar()
    total_revenue = query.with_entities(func.sum(models.Sale.total_amount)).scalar()

    return {"total_quantity_sold": total_quantity_sold, "total_revenue": total_revenue}


@app.get("/sales/compare")
def compare_sales(
    start_date_1: str,
    end_date_1: str,
    start_date_2: str,
    end_date_2: str,
    db: Session = Depends(get_db)
):
    # Compare sales data between two date ranges
    revenue_1 = db.query(func.sum(models.Sale.total_amount)).filter(models.Sale.sale_date.between(start_date_1, end_date_1)).scalar()
    revenue_2 = db.query(func.sum(models.Sale.total_amount)).filter(models.Sale.sale_date.between(start_date_2, end_date_2)).scalar()

    return {"revenue_comparison": {"date_range_1": {"start_date": start_date_1, "end_date": end_date_1, "revenue": revenue_1},
                                   "date_range_2": {"start_date": start_date_2, "end_date": end_date_2, "revenue": revenue_2}}}


@app.get("/sales/bydate")
def sales_by_date(
    start_date: str,
    end_date: str,
    db: Session = Depends(get_db)
):
    # Retrieve sales data by date range
    sales_by_date_range = db.query(models.Sale).filter(models.Sale.sale_date.between(start_date, end_date)).all()
    return sales_by_date_range


@app.get("/sales/byproduct")
def sales_by_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    # Retrieve sales data for a specific product
    sales_by_product = db.query(models.Sale).filter(models.Sale.product_id == product_id).all()
    return sales_by_product

@app.get("/sales/bycategory")
def sales_by_category(
    category: str,
    db: Session = Depends(get_db)
):
    # Retrieve sales data for a specific product category
    sales_by_category = db.query(models.Sale).join(models.Product).filter(models.Product.product_category == category).all()
    return sales_by_category