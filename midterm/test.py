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
