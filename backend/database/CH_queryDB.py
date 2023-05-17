def queryDB(Table):
    rows = Table.query.order_by(Table.idx).all()
    return rows