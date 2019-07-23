from source.models.order import Order
from source.models.priority import Priority
from source.models.stock import Stock
import os, shutil, csv, zipfile
from datetime import date

class OrderHandler:
  def __init__(self, orders_data, priorities_data, stocks_data):
    self.orders = self.get_orders(orders_data)
    self.priorities = self.get_priorities(priorities_data)
    self.stocks = self.get_stocks(stocks_data)
    self.error_orders = []
    self.success_orders = {}

  def process(self):
    payed_orders = self._get_payed_orders()
    unpayed_orders = self._get_unpayed_orders()

    for order in payed_orders:
      self._process_order(order)

    for order in unpayed_orders:
      self._process_order(order)

  def generate_result(self):
    current_datetime = date.today().strftime("%d.%m.%Y")

    if os.path.exists('result'):
      shutil.rmtree('result')

    headers = self.orders[0].raw_data.keys()
    
    os.makedirs('result/error_orders')
    with open('./result/error_orders/{}.csv'.format(current_datetime), 'w') as csvfile:
      writer = csv.writer(csvfile, delimiter=',')
      writer.writerow(headers)
      for order in self.error_orders:
        values = order.raw_data.values()
        writer.writerow(values)

    os.makedirs('result/success_orders')
    for key in self.success_orders.keys():
      product_name = key.split('_')[0]
      supplier_name = key.split('_')[1]
      with open('./result/success_orders/{}_{}_{}_{}.csv'.format(product_name, self.success_orders[key]['quanlity'], current_datetime, supplier_name), 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(headers)
        for order in self.success_orders[key]['orders']:
          values = order.raw_data.values()
          writer.writerow(values)

    zf = zipfile.ZipFile("result.zip", "w")
    for dirname, subdirs, files in os.walk("result"):
      zf.write(dirname)
      for filename in files:
        zf.write(os.path.join(dirname, filename))
    zf.close()


  @staticmethod
  def get_orders(orders_data):
    orders = []
    for order_data in orders_data:
      orders.append(Order(order_data))
    return orders

  @staticmethod
  def get_priorities(priorities_data):
    priorities = []
    for priority_data in priorities_data:
      priorities.append(Priority(priority_data))
    return priorities

  @staticmethod
  def get_stocks(stocks_data):
    stocks = []
    for stock_data in stocks_data:
      stocks.append(Stock(stock_data))
    return stocks

  def _get_payed_orders(self):
    payed_orders = []
    for order in self.orders:
      if order.status == 'SHIPPING':
        payed_orders.append(order)
    return payed_orders

  def _get_unpayed_orders(self):
    unpayed_orders = []
    for order in self.orders:
      if order.status == 'TO_ORDER':
        unpayed_orders.append(order)
    return unpayed_orders

  def _process_order(self, order):
    sku = order.sku
    quanlity = int(order.quanlity)

    stock = self._get_stock(sku)
    if stock is None:
      self._add_error_order(order)
      return

    short_cut, agent_supply = self._get_agent_supply(sku)
    for agent in agent_supply:
      if self._check_valid_agent_supply(stock, agent, quanlity):
        self._update_stock(stock, agent, quanlity)
        self._add_success_order(short_cut, agent, order)
        return

    self._add_error_order(order)
    

  def _get_agent_supply(self, order_sku):
    agent_supply = []
    short_cut = None
    for priority in self.priorities:
      if priority.sku == order_sku:
        short_cut = priority.short_cut
        order_available = [*priority.agent_priority]
        order_available.sort()
        for order in order_available:
          agent_supply.append(priority.agent_priority[order])
    return short_cut, agent_supply

  def _get_stock(self, order_sku):
    for stock in self.stocks:
      if stock.sku == order_sku:
        return stock
    return None

  def _check_valid_agent_supply(self, stock, agent, quanlity):
    return stock.agent_is_valid(agent, quanlity)

  def _update_stock(self, stock, agent, quanlity):
    stock.update(agent, quanlity)

  def _add_success_order(self, short_cut, agent, order):
    key = short_cut + '_' +  agent.split(' ')[1]
    quanlity = int(order.quanlity)
    if key in self.success_orders.keys():
      self.success_orders[key]['orders'].append(order)
      self.success_orders[key]['quanlity'] = self.success_orders[key]['quanlity'] + quanlity
    else:
      self.success_orders[key] = {}
      self.success_orders[key]['orders'] = [order]
      self.success_orders[key]['quanlity'] = quanlity

  def _add_error_order(self, order):
    self.error_orders.append(order)
