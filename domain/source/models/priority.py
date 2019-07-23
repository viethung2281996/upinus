class Priority:
  def __init__(self, raw_data):
    self.sku = raw_data['SKU']
    self.short_cut = raw_data['Tên viết tắt']
    self.agent_priority = self._get_agent_priority(raw_data)

  def _get_agent_priority(self, raw_data):
    agent_priority = {}

    for key in raw_data.keys():
      if 'Agent' in key:
        try:
          priority = int(raw_data[key])
          agent_priority[priority] = key
        except ValueError as e:
          continue

    return agent_priority