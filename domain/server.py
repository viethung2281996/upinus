from flask import Flask, render_template, request, send_file, redirect, abort
from source.helpers.csv import CSV
from order_handler import OrderHandler
app = Flask(__name__)

@app.route("/", methods=('GET', 'POST'))
def hello():
  if request.method == 'GET':
    return render_template('index.html')
  elif request.method == 'POST':
    order_file = request.files['order']
    priotiry_file = request.files['priority']
    stock_file = request.files['stock']

    if order_file.filename == '' or priotiry_file.filename == '' or stock_file.filename == '':
      return abort(400)

    try:
      orders = CSV.get_data_raw_file(order_file)
      priorities = CSV.get_data_raw_file(priotiry_file)
      stocks = CSV.get_data_raw_file(stock_file)
    except Exception as e:
      return abort(400)

    try:
      order_handler = OrderHandler(orders, priorities, stocks)
      order_handler.process()
      order_handler.generate_result()
    except Exception as e:
      return abort(500)
      
    return redirect('result') 
  else:
    return abort(400)

@app.route("/result", methods=('GET',))
def result():
  return render_template('result.html')

@app.route("/download")
def download():
  path = './result.zip'
  return send_file(path, as_attachment=True)
if __name__ == '__main__':
  app.run()