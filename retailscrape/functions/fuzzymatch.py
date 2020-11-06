def fuzzymatch(df_products, df_invoice_lines):
    main_log.log.debug(f'fuzzymatch: starting')
    # Dedupe invoice line products
    df_invoice_lines_fm = df_invoice_lines.copy()
    main_log.log.debug(f'fuzzymatch:len df_invoice_lines_fm before dedupe={len(df_invoice_lines_fm)}')
    df_invoice_lines_fm.drop_duplicates(subset=['INVOICE_LINE_PRODUCT_NAME', 'INVOICE_LINE_PRODUCT_DESCRIPTION'], keep='first', inplace=True)
    save_df_as_csv(df_invoice_lines_fm, term='fm_deduped')
    main_log.log.debug(f'fuzzymatch:len df_invoice_lines_fm after dedupe={len(df_invoice_lines_fm)}')
    left_on = ['PRODUCT_NAME', 'PRODUCT_DESCRIPTION']
    right_on = ['INVOICE_LINE_PRODUCT_NAME', 'INVOICE_LINE_PRODUCT_DESCRIPTION'] 
    matched_results = fuzzymatcher.fuzzy_left_join(df_products, df_invoice_lines_fm, left_on, right_on, left_id_col='PRODUCT_NUMBER', right_id_col = 'INVOICE_NUMBER')
    main_log.log.debug(f'fuzzymatch: len matched_results={len(matched_results)}')
    main_log.log.debug(f'fuzzymatch: ending')
    return matched_results