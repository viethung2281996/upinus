import csv

class CSV:
  def __init__(self):
    pass

  @staticmethod
  def get_data_raw_file(file):
    data = []
    csvfile = (line.decode('utf8') for line in file)
    reader = csv.DictReader(csvfile, delimiter=',', quotechar='|')
    headers = reader.fieldnames

    for row in reader:
      item = {}
      for header in headers:
        item[header] = row[header] 

      data.append(item)

    return data