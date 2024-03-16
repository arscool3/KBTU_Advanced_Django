import requests

BASE_URL = "http://localhost:8000"

def test_create_product():
    product_data = {
        "name": "Test Product",
        "supplier_id": 1,  
        "category_id": 1  
    }
    response = requests.post(f"{BASE_URL}/product", json=product_data)
    print(response.json())


def test_get_products():
    response = requests.get(f"{BASE_URL}/products")
    print(response.json())


def test_delete_product(product_id):
    response = requests.delete(f"{BASE_URL}/product/{product_id}")
    print(response.json())


def test_create_supplier():
    supplier_data = {
        "supplier_name": "Test Supplier"
    }
    response = requests.post(f"{BASE_URL}/supplier", json=supplier_data)
    print(response.json())


def test_get_suppliers():
    response = requests.get(f"{BASE_URL}/suppliers")
    print(response.json())


def test_delete_supplier(supplier_id):
    response = requests.delete(f"{BASE_URL}/supplier/{supplier_id}")
    print(response.json())  


def test_create_category():
    category_data = {
        "category_name": "Test Category"
    }
    response = requests.post(f"{BASE_URL}/category", json=category_data)
    print(response.json())


def test_get_categories():
    response = requests.get(f"{BASE_URL}/categories")
    print(response.json())


def test_delete_category(category_id):
    response = requests.delete(f"{BASE_URL}/category/{category_id}")
    print(response.json())


if __name__ == "__main__":
    test_create_product()
    test_get_products()


def test_update_product(product_id):
    product_data = {
        "name": "Updated Product",
        "supplier_id": 2,  
        "category_id": 2  
    }
    response = requests.put(f"{BASE_URL}/product/{product_id}", json=product_data)
    print(response.json())


def test_update_supplier(supplier_id):
    supplier_data = {
        "supplier_name": "Updated Supplier"
    }
    response = requests.put(f"{BASE_URL}/supplier/{supplier_id}", json=supplier_data)
    print(response.json())


def test_update_category(category_id):
    category_data = {
        "category_name": "Updated Category"
    }
    response = requests.put(f"{BASE_URL}/category/{category_id}", json=category_data)
    print(response.json())


def test_create_order():
    order_data = {
        "product_id": 1,
        "quantity": 10
    }
    response = requests.post(f"{BASE_URL}/order", json=order_data)
    print(response.json())


def test_create_customer():
    customer_data = {
        "name": "Test Customer"
    }
    response = requests.post(f"{BASE_URL}/customer", json=customer_data)
    print(response.json())
