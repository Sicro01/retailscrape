from collections import namedtuple # type: ignore
from classes.product_class import Product # type: ignore
from functions.helper_functions import create_log  # type: ignore

class Webpage():
    def __init__(self, soup, url, result_page_number):
        self.soup = soup
        self.result_page_number = result_page_number
        self.url = url
        self.products = []
        self.webpage_log = create_log('retail_live.webpage_log')
        self.price_tuple = namedtuple('Price', ['from_price', 'to_price'])
        self.fulfillment_tuple = namedtuple('Fulfillment', ['fulfillment'])
        self.availability_tuple = namedtuple('Availability', ['availability'])
        self.description_tuple = namedtuple('Description', ['description'])
        self.rating_tuple = namedtuple('Rating', ['rating'])
    
    def get_product_data(self, search_term):
        self.webpage_log.info('get_product_data: Capturing product data for current webpage')
        grid_ul_tags = self.soup.find_all('ul', class_='search-result-gridview-items four-items')
        for grid_ul_tag in grid_ul_tags:
            grid_item_div_tags = grid_ul_tag.find_all('div', class_='search-result-gridview-item clearfix arrange-fill') # All items are li html elements within the ul with the above classes
            for result_page_item_position_index, grid_item_div_tag in enumerate(grid_item_div_tags):
                description_tuple = self.get_description(grid_item_div_tag) # Get description
                rating_tuple = self.get_rating(grid_item_div_tag) # Get rating
                prices_tuple = self.get_prices(grid_item_div_tag) # Get prices
                fulfillment_tuple = self.get_fulfillment(grid_item_div_tag) # Get fulfillment
                availability_tuple = self.get_availability(grid_item_div_tag) # Get Availability
                
                # Create a product entity
                this_product = Product(result_page_item_position_index, search_term, self.url, self.result_page_number, description_tuple.description, prices_tuple.from_price, prices_tuple.to_price                                         ,fulfillment_tuple.fulfillment, availability_tuple.availability, rating_tuple.rating)
                
                self.webpage_log.debug(f'get_product_data:this_product:'+ '\n' + f'{this_product}')
                self.products.append(this_product)
        self.webpage_log.debug(f'get_product_data: len(self.products): {len(self.products)}')    
            
    def get_description(self, grid_item_div_tag):
        description_tag = grid_item_div_tag.find('a', class_='product-title-link')
        description_tuple = self.description_tuple(description_tag.span.text)
        self.webpage_log.debug(f'get_product_data:description_tuple:{description_tuple}')
        return description_tuple
    
    def get_rating(self, grid_item_div_tag):
        stars = [star for star in grid_item_div_tag.find_all('span', class_="star-rated")]
        half_stars = [half_star for half_star in grid_item_div_tag.find_all('span', class_="star-partial")]
        rating_tuple = self.rating_tuple(len(stars) + len(half_stars)/2)
        self.webpage_log.debug(f'get_product_data:rating_tuple:{rating_tuple}')
        return rating_tuple
    
    def get_prices(self, grid_item_div_tag):
        price_tags = [price for price in grid_item_div_tag.find_all('span', class_="price-main")]
        these_prices = [price_tag.span.text for price_tag in price_tags]
        these_prices.append(these_prices[0]) if len(these_prices) == 1 else None
        these_prices.extend(['', '']) if len(these_prices) == 0 else None # Set empty prices if product has fulfillment of 'In-store Only' thenno prices will be displayed on webpage
        prices_tuple = self.price_tuple(these_prices[0], these_prices[1])
        self.webpage_log.debug(f'get_product_data:prices_tuple:{prices_tuple}')
        return prices_tuple
    
    def get_fulfillment(self, grid_item_div_tag):
        fulfillment_tag = grid_item_div_tag.find('div', class_="search-result-product-shipping-details gridview")
        fulfillment = f'{fulfillment_tag.text}' if fulfillment_tag != None else ''
        replace_dict = {'\a0': ' ', 'Free delivery': ' Free delivery', 'deliveryon': 'delivery on', 'Â': ' '} # Some fulfillment text needs tidying up - so execute some string replacements
        fulfillment = self.fulfillment_replace_all(fulfillment, replace_dict)
        fulfillment_tuple = self.fulfillment_tuple(fulfillment)
        self.webpage_log.debug(f'get_product_data:fulfillment_tuple:{fulfillment_tuple}')
        return fulfillment_tuple
    
    def get_availability(self, li_tag):
        availability_tag = li_tag.find('div', class_="product-sub-title-block")
        availability = availability_tag.span.text if availability_tag != None else ''
        availability_tuple = self.availability_tuple(availability)
        self.webpage_log.debug(f'get_product_data:availability_tuple:{availability_tuple}')
        return availability_tuple
    
    def fulfillment_replace_all(self, text, dic):
        for bad_text, good_text in dic.items():
            text = text.replace(bad_text, good_text)
        return text