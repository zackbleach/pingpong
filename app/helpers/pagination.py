from config import Config


class Pagination():

    def __init__(self, page=None, page_size=None):
        if page_size is None:
            self.page_size = Config.DEFAULT_PAGE_SIZE
        else:
            self.page_size = page_size

        if page is None:
            self.page = 1
        else:
            self.page = page

    def __repr__(self):
        return '<Pagination : page = %r, pageSize = %r >' % (self.page,
                                                             self.page_size)
