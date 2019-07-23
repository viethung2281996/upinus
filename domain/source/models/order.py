class Order:
  def __init__(self, raw_data):
    self.id = raw_data['Order ID']
    self.name = raw_data['Order Name']
    self.status = raw_data['Order Status']
    self.quanlity = raw_data['Quantity']
    self.sku = raw_data['Lineitem SKU']
    self.raw_data = raw_data
