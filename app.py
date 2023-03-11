from flask import Flask, request, jsonify
from trade_executor import TradeExecutor

app = Flask(__name__)
executor = TradeExecutor()


@app.route('/submit_trade', methods=['POST'])
def submit_trade():
    trade = request.json
    execute_time = trade.get('execute_time')
    executor.submit_trade(trade, execute_time)
    return jsonify({'status': 'success'})


@app.route('/shutdown', methods=['POST'])
def shutdown():
    executor.shutdown()
    return jsonify({'status': 'success'})


if __name__ == '__main__':
    app.run(debug=True)

# curl to place the new trade: curl -X POST -H "Content-Type: application/json" -d '{"symbol": "AAPL", "quantity": 100, "price": 150.0, "action": "BUY", "execute_time": "2023-03-12T10:00:00"}' http://localhost:5000/submit_trade
# curl to shut down the trade manager: curl -X POST http://localhost:5000/shutdown
