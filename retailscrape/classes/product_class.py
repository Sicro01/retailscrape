class Product:
    def __init__(self, result_page_number, result_page_index_position, search_term, url, description, from_price, to_price, cost_price, fulfillment, availability,
        rating, duplicate_indicator='N'):
        self.result_page_number = result_page_number
        self.result_page_index_position = result_page_index_position
        self.search_term = search_term
        self.url = url
        self.description = description
        self.from_price = from_price
        self.to_price = to_price
        self.cost_price = cost_price
        self.fulfillment = fulfillment
        self.availability = availability
        self.rating = rating
        self.duplicate_indicator = duplicate_indicator
    
    def __str__(self):
        all_attributes = [''.join(f'{attribute}:{value}') for attribute, value in self.__dict__.items()]
        return ' ::: '.join(all_attributes)
    
    def __repr__(self):
        all_attributes = [''.join(f'{attribute}:{value}') for attribute, value in self.__dict__.items()]
        return ' ::: '.join(all_attributes)
    
    def set_duplicate(self):
        self.duplicate_indicator = 'Y'
    
    def to_dict(self):
        return {
            'RESULT_PAGE_NUMBER': self.result_page_number
            ,'RESULT_PAGE_INDEX_POSITION': self.result_page_index_position
            ,'SEARCH_TERM': self.search_term
            ,'URL': self.url
            ,'DESCRIPTION': self.description
            ,'FROM_PRICE': self.from_price
            ,'TO_PRICE': self.to_price
            ,'COST_PRICE': self.cost_price
            ,'FULFILLMENT': self.fulfillment
            ,'AVAILABILITY': self.availability
            ,'RATING': self.rating
            ,'DUPLICATE_INDICATOR': self.duplicate_indicator
        }
    
    def print_product(self):
        attrs = vars(self)
        return (', '.join('%s: %s' % item for item in attrs.items()))

    def df_to_class_list(self, df):
        return [(
            Product(
                row.result_page_number
                ,row.result_page_index_position
                ,row.search_term
                ,row.url
                ,row.description
                ,row.from_price
                ,row.to_price
                ,row.cost_price
                ,row.fulfillment
                ,row.availability
                ,row.rating
                ,row.duplicate_indicator
                )) for i, row in df.iterrows()]

    
