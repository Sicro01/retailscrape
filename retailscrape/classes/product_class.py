class Product:
    def __init__(self, result_page_number, result_page_index_position, search_term, url, description, from_price, to_price, fulfillment, availability, rating, duplicate_indicator='N'):
        self.result_page_number = result_page_number
        self.result_page_index_position = result_page_index_position
        self.search_term = search_term
        self.url = url
        self.description = description
        self.from_price = from_price
        self.to_price = to_price
        self.fulfillment = fulfillment
        self.availability = availability
        self.rating = rating
        self.duplicate_indicator = duplicate_indicator
    
    def __str__(self):
        all_attributes = [''.join(f'{attribute}:{value}') for attribute, value in self.__dict__.items()]
        return ' :: '.join(all_attributes)
    
    def __repr__(self):
        all_attributes = [''.join(f'{attribute}:{value}') for attribute, value in self.__dict__.items()]
        return ' :: '.join(all_attributes)
    
    def set_duplicate(self):
        self.duplicate_indicator = 'Y'
    
    def to_dict(self):
        return {
            'result_page_number': self.result_page_number
            ,'result_page_index_position': self.result_page_index_position
            ,'search_term': self.search_term
            ,'url': self.url
            ,'description': self.description
            ,'from_price': self.from_price
            ,'to_price': self.to_price
            ,'fulfillment': self.fulfillment
            ,'availability': self.availability
            ,'rating': self.rating
            ,'duplicate_indicator': self.duplicate_indicator
        }
    
    def print_product(self):
        attrs = vars(self)
        return (', '.join('%s: %s' % item for item in attrs.items()))
