# def create_products(df_product_csv):
#     main_log.log.info('create_products: starting')
#     # Start with the webscraped products dataframe and delete all range priced products
#     df_non_range_products = df_product_csv.drop(df_product_csv[df_product_csv['FROM_PRICE'] != df_product_csv['TO_PRICE']].index)
#      # Select and rename required columns from web product data
#     df_products = df_non_range_products[['RESULT_PAGE_NUMBER', 'RESULT_PAGE_INDEX_POSITION', 'SEARCH_TERM', 'DESCRIPTION', 'FROM_PRICE']].copy()
#     df_products = df_products.rename(columns={'SEARCH_TERM': 'PRODUCT_NAME', 'DESCRIPTION': 'PRODUCT_DESCRIPTION', 'FROM_PRICE': 'WEB_SELLING_PRICE'})
#     # Create / mimic cost price by discounting selling price
#     df_products['CALCULATED_COST_PRICE'] = round(df_products['WEB_SELLING_PRICE'] * np.random.randint(85, 95, len(df_products))/100, 2)
#     list_of_products = [
#         Product(
#             str(row['RESULT_PAGE_NUMBER']) + '-' + str(row['RESULT_PAGE_INDEX_POSITION'])
#             ,row['RESULT_PAGE_NUMBER']
#             ,row['RESULT_PAGE_INDEX_POSITION']
#             ,row['PRODUCT_NAME']
#             ,row['PRODUCT_DESCRIPTION']
#             ,row['WEB_SELLING_PRICE']
#             ,row['CALCULATED_COST_PRICE']
#         )
#         for index, row in df_products.iterrows()
#     ]
#     main_log.log.info(f'create_products: ending: {len(list_of_products)} products created')
#     return list_of_products