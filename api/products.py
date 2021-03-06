from google.cloud import datastore
import connexion

datastore_client = datastore.Client()

def search():
  query = datastore_client.query(kind='products')
  query_iter = query.fetch()
  products = []
  for entity in query_iter:
    products.append(entity)
  response = {
    "products": products
  }
  return response, 201
def post(user, product):
  print(user)
  # token = connexion.request.headers['Authorization']
  # print(token)
  kind = 'products'
  name = product['product_id']
  # The Cloud Datastore key for the new entity
  product_key = datastore_client.key(kind, name)
  # Prepares the new entity
  product_entry = datastore.Entity(key=product_key)
  product_entry['producer_id'] = product['producer_id']
  product_entry['product_name'] = product['product_name']
  product_entry['release_date'] = product['release_date']
  product_entry['product_id'] = product['product_id']
  
  # check if the user edits a product that does not belong to him !need to implement a check that he does not overwrite an existing one from someone else
  if user != product['producer_id']:
    return None, 401 

  # Saves the entity
  datastore_client.put(product_entry)
  return product, 200