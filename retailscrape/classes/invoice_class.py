import random # type: ignore
import pandas as pd # type:ignore
from classes.invoice_line_class import InvoiceLine # type: ignore

class Invoice:
    def __init__(self, invoice_date):
        self.invoice_number = random.sample(range(1000000),1)[0]
        self.invoice_date = invoice_date
        self.invoice_number_of_lines = random.randint(5,15)
        self.invoice_lines = []
        
    def add_invoice_line(self, product, line_number):
        invoice_line = InvoiceLine(self.invoice_number, self.invoice_date, line_number, product)
        self.invoice_lines.append(invoice_line)
    
    def __str__(self):
        return f'invoice_number={self.invoice_number}:invoice_date={self.invoice_date}:number_invoice_lines={len(self.invoice_lines)}'
    
    def to_dict(self):
        return {
            'INVOICE_NUMBER': self.invoice_number
            ,'INVOICE_DATE': self.invoice_date
            ,'NUMBER_INVOICE_LINES': len(self.invoice_lines)
        }
    
    def df(self, list_of_items):
        return pd.DataFrame.from_records([i.to_dict for i in list_of_items])
