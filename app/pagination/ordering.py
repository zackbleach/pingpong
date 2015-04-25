class Ordering():

    def __init__(self, order_by=None, direction=None):
        if order_by is None:
            self.order_by = 'id'
        else:
            self.order_by = order_by

        if direction is None:
            self.direction = 'desc'
        else:
            self.direction = direction

    def __repr__(self):
        return '<Ordering : order_by = %r, direction = %r >' % (self.order_by,
                                                                self.direction)
