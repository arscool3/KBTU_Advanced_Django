# Ensure this function can be imported and used in the Kafka consumer
from sqlalchemy import text
from datetime import datetime
from database import get_db
from analys_product.models import AnalysProduct

def process_and_store_most_popular_product():
    db_gen = get_db()
    db = next(db_gen)
    try:
        sql = """
        SELECT ci.product_id, SUM(ci.amount) AS total_amount, p.name AS product_name
        FROM cart_item ci
        JOIN product p ON p.id = ci.product_id
        GROUP BY ci.product_id, p.name
        ORDER BY total_amount DESC
        LIMIT 1;
        """
        result = db.execute(text(sql)).first()
        if result:
            new_popular_product = AnalysProduct(
                product_id=result.product_id,
                product_name=result.product_name,
                count=result.total_amount,
                calculated_at=datetime.utcnow()
            )
            db.add(new_popular_product)
            db.commit()
            print("Popular product data has been stored successfully.")
            return new_popular_product
        else:
            print("No products found in cart items.")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
        return None
    finally:
        try:
            next(db_gen)
        except StopIteration:
            pass


# from sqlalchemy import text
# from sqlalchemy.orm import Session
# from datetime import datetime
# from database import session as db_session, session  # Assuming db_session is a scoped session
# from analys_product.models import AnalysProduct  # Ensure you have imported your ORM model
#
#
# def process_and_store_most_popular_product():
#     # SQL query that sums the amounts for each product
#     sql = """
#     SELECT ci.product_id, SUM(ci.amount) AS total_amount, p.name AS product_name
#     FROM cart_item ci
#     JOIN product p ON p.id = ci.product_id
#     GROUP BY ci.product_id, p.name
#     ORDER BY total_amount DESC
#     LIMIT 1;
#     """
#
#     # Execute the SQL using the `text()` function to safely execute raw SQL
#     result = db_session.execute(text(sql)).first()
#
#     if result:
#         # Create and store the PopularProduct entry
#         with session as sess:
#             new_popular_product = AnalysProduct(
#                 product_id=result.product_id,
#                 product_name=result.product_name,
#                 count=result.total_amount,  # Assuming 'count' represents the total amount
#                 calculated_at=datetime.utcnow()
#             )
#             sess.add(new_popular_product)
#             sess.commit()
#             print("Popular product data has been stored successfully.")
#     else:
#         print("No products found in cart items.")



# from sqlalchemy import text
# from database import session  # Ensure this is a properly scoped session for your application
#
# def get_most_popular_product_by_amount():
#     # SQL query that sums the amounts for each product
#     sql = """
#     SELECT ci.product_id, SUM(ci.amount) AS total_amount, p.name AS product_name
#     FROM cart_item ci
#     JOIN product p ON p.id = ci.product_id
#     GROUP BY ci.product_id, p.name
#     ORDER BY total_amount DESC
#     LIMIT 1;
#     """
#     # Execute the SQL using the `text()` function to safely execute raw SQL
#     result = session.execute(text(sql)).first()
#     if result:
#         return {
#             "product_id": result.product_id,
#             "product_name": result.product_name,
#             "total_amount": result.total_amount  # The total amount of products added to carts
#         }
#     else:
#         return {"message": "No products found in cart items."}
