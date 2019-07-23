class Stock:
  def __init__(self, raw_data):
    self.sku = raw_data['SKU']
    self.agent_stock = self._get_agent_stock(raw_data)

  def agent_is_valid(self, agent, quanlity):
    return True if self.agent_stock[agent] >= quanlity else False

  def update(self, agent, quanlity):
    self.agent_stock[agent] = self.agent_stock[agent] - quanlity

  def _get_agent_stock(self, raw_data):
    agent_stock = {}

    for key in raw_data.keys():
      if 'Agent' in key:
        try:
          quanlity = int(raw_data[key])
          agent_stock[key] = quanlity
        except ValueError as e:
          continue

    return agent_stock

