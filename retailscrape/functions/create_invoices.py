from datetime import datetime, timedelta # type: ignore
import random # type: ignore
from copy import deepcopy # type: ignore
from classes.invoice_class import Invoice # type: ignore
from classes.invoice_line_class import InvoiceLine # type: ignore
from classes.log_class import Log # type: ignore

def create_invoices(list_of_products=[], number_of_invoices=20, scrape_log=''):
    module_log = Log(module_name=scrape_log.module_name + f'.create_invoices')
    module_log.log.info(f'starting creating invoices')
    # main_log.log.info('create_invoices: starting')
    # Create empty lists to hold outputs
    list_of_invoices = []
    list_of_invoice_lines = []
    # Iterate for number of invoices
    for i in range(number_of_invoices):
        invoice_date = datetime.now() - timedelta(days=i)
        invoice = Invoice(invoice_date.date())
        invoice.invoice_number_of_lines = len(list_of_products) if invoice.invoice_number_of_lines > len(list_of_products) else invoice.invoice_number_of_lines
        # main_log.log.debug(f'create_invoices: invoice for date {invoice.invoice_date} created')
        product_indexes = random.sample(range(len(list_of_products)), invoice.invoice_number_of_lines)
        # Iterate for number of invoice lines (a random number created on invoice instantiation)
        for line_number in range(invoice.invoice_number_of_lines):
            this_product = deepcopy(list_of_products[product_indexes[line_number]]) # Copy product entity using random index number ref to list of product entities
            invoice_line = InvoiceLine(invoice.invoice_number, invoice.invoice_date, line_number, this_product)
            invoice.invoice_lines.append(invoice_line)
            list_of_invoice_lines.append(invoice_line)
            # main_log.log.debug(f'create_invoices: invoice line for product {invoice_line.product.product_description} created')
        list_of_invoices.append(invoice)
    # main_log.log.info(f'create_invoices: ending: {len(list_of_invoices)} invoices created')
    return list_of_invoice_lines

def modify_invoice_line_product_descriptions(list_of_invoices):
    for invoice in list_of_invoices:
        for invoice_line in invoice.invoice_lines:
            split_description = invoice_line.product.product_description.split(',')
            if len(split_description) == 3:
                invoice_line.product.product_description = split_description[1] + split_description[2]