class InvoiceLine:
    def __init__(self, invoice_number, invoice_date, invoice_line_number, product):
        self.invoice_number = invoice_number
        self.invoice_date = invoice_date
        self.invoice_line_number = invoice_line_number
        self.product = product
        self.invoice_line_dollar_margin = self.product.from_price - self.product.cost_price
        self.invoice_line_percent_margin = round((self.invoice_line_dollar_margin / self.product.from_price) * 100, 2)

    def __str__(self):
        return f'invoice_number={self.invoice_number}:' \
        + f'self.invoice_date={self.invoice_date}:' \
        + f'self.invoice_line_number={self.invoice_line_number}:' \
        + f'self.product.search_term={self.product.search_term}:' \
        + f'self.product.description={self.product.description}:' \
        + f'self.product.from_price={self.product.from_price}:' \
        + f'self.product.cost_price={self.product.cost_price}' \
        + f'self.invoice_line_dollar_margin={self.invoice_line_dollar_margin}' \
        + f'self.invoice_line_percent_margin={self.invoice_line_percent_margin}'
    
    def to_dict(self):
        return {
            'INVOICE_NUMBER': self.invoice_number
            ,'INVOICE_DATE': self.invoice_date
            ,'INVOICE_LINE_NUMBER': self.invoice_line_number
            ,'INVOICE_LINE_PRODUCT_NAME': self.product.search_term
            ,'INVOICE_LINE_PRODUCT_DESCRIPTION': self.product.description
            ,'INVOICE_LINE_PRODUCT_WEB_SELLING_PRICE': self.product.from_price
            ,'INVOICE_LINE_PRODUCT_CALCULATED_COST_PRICE': self.product.cost_price
            ,'INVOICE_LINE_DOLLAR_MARGIN': self.invoice_line_dollar_margin
            ,'INVOICE_LINE_PERCENT_MARGIN': self.invoice_line_percent_margin
        }