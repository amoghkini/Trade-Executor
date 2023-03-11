from datetime import datetime
import time
import heapq
import threading
from concurrent.futures import ThreadPoolExecutor


class TradeExecutor:
    def __init__(self):
        self.trade_queue = []
        self.immediate_queue = []
        self.pool = ThreadPoolExecutor(max_workers=10)
        self.lock = threading.Lock()
        self.done = threading.Event()
        self.done.clear()

        # start the thread that monitors the trade queue
        t = threading.Thread(target=self._process_trades)
        t.daemon = True
        t.start()

    def submit_trade(self, trade, execute_time=None):
        if execute_time is None:
            # if no execute_time is specified, add it to the immediate queue
            self.immediate_queue.append(trade)
        else:
            # otherwise, add it to the priority queue based on its execution time
            with self.lock:
                heapq.heappush(self.trade_queue, (execute_time, trade))

    def _process_trades(self):
        while not self.done.is_set():
            # check if there are any immediate trades to execute
            while len(self.immediate_queue) > 0:
                trade = self.immediate_queue.pop(0)
                self.pool.submit(self._execute_trade, trade)

            # check if there are any trades to execute based on their scheduled time
            print("Current time",datetime.now(),"trade queue", self.trade_queue)
            #if len(self.trade_queue) > 0:
            #    print(self.trade_queue[0][0])  

            with self.lock:
                #while len(self.trade_queue) > 0 and self.trade_queue[0][0] <= time.time():
                while len(self.trade_queue) > 0 and int(time.mktime(datetime.strptime(self.trade_queue[0][0], "%Y-%m-%d-%H:%M:%S").timetuple())) <= time.time():
                    _, trade = heapq.heappop(self.trade_queue)
                    self.pool.submit(self._execute_trade, trade)

            # sleep for a short interval to avoid busy waiting
            time.sleep(0.1)

    def _execute_trade(self, trade):
        # Write the broker specific trade execution logic here.
        print(f"Executing trade: {trade} at {datetime.now()}")
        time.sleep(0.1)  # simulate trade execution time

    def shutdown(self):
        self.done.set()
        self.pool.shutdown(wait=False)
