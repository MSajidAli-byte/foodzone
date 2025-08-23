# Generate unique transaction ID
txn_id = f'T{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}{order.id}'
request.session['order_id'] = order.id
