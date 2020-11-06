def recordlink(df_products, df_invoice_lines):
    main_log.log.debug(f'recordlink: starting')
    # Prep data for Record Linkage - df's need to have samne number of rows and have index set
    # df_products.set_index('RESULT_PAGE_NUMBER', 'RESULT_PAGE_INDEX_POSITION')
    df_products.set_index('RESULT_PAGE_NUMBER')
    df_invoice_lines_rl = df_invoice_lines.copy()
    # df_invoice_lines_rl.set_index('INVOICE_NUMBER', 'INVOICE_LINE_NUMBER')
    df_invoice_lines_rl.set_index('INVOICE_NUMBER')
    # Get distinct list of products held in invoice lines
    main_log.log.debug(f'recordlink:len df_invoice_lines_rl before dedupe={len(df_invoice_lines_rl)}')
    df_invoice_lines_rl.drop_duplicates(subset=['INVOICE_LINE_PRODUCT_NAME', 'INVOICE_LINE_PRODUCT_DESCRIPTION'], keep='first', inplace=True)
    main_log.log.debug(f'recordlink:len df_invoice_lines_rl after dedupe={len(df_invoice_lines_rl)}')
    save_df_as_csv(df_invoice_lines_rl, term='rl_deduped')
    # number_additional_rows = len(df_products) - len(df_invoice_lines_rl)
    # main_log.log.debug(f'recordlink: before append rows:number of addtl rows={number_additional_rows}:len of df_invoice_lines_rl={len(df_invoice_lines_rl)}:'
    #     + f'len of df_products={len(df_products)}')
    # for i in range(number_additional_rows):
    #     dummy_value = 'dummy' + str(i)
    #     new_row = pd.Series({'INVOICE_NUMBER': dummy_value, 'INVOICE_DATE': dummy_value, 'INVOICE_LINE_NUMBER': dummy_value, 'INVOICE_LINE_PRODUCT_NAME': dummy_value,                          'INVOICE_LINE_PRODUCT_DESCRIPTION': dummy_value, 'INVOICE_LINE_PRODUCT_WEB_SELLING_PRICE': dummy_value, 'INVOICE_LINE_PRODUCT_CALCULATED_COST_PRICE': dummy_value,          })
    #     df_invoice_lines_rl = df_invoice_lines_rl.append(new_row, ignore_index=True)
    # save_df_as_csv(df_invoice_lines_rl, term='deduped_in_line_dummies')
    # main_log.log.debug(f'recordlink: after append rows:number of addtl rows={number_additional_rows}:len of df_invoice_lines_rl={len(df_invoice_lines_rl)}:'
    #     + f'len of df_products={len(df_products)}')
    
    # Fuzzy match invoice descriptions stetching back x days to those on the 'product file' and rank each match
    indexer = recordlinkage.Index()
    indexer.full()
    # indexer.block(left_on=['NAME'], right_on=['INVOICE_LINE_PRODUCT_NAME'])
    candidate_links = indexer.index(df_products, df_invoice_lines_rl)
    main_log.log.debug(f'recordlink: len candidate_links={len(candidate_links)}')
    compare = recordlinkage.Compare()
    compare.exact('PRODUCT_NAME', 'INVOICE_LINE_PRODUCT_NAME', label='PRODUCT_NAME')
    compare.string('PRODUCT_DESCRIPTION', 'INVOICE_LINE_PRODUCT_DESCRIPTION', method='jarowinkler', threshold=0.7, label='PRODUCT_DESCRIPTION')
    feature_vectors = compare.compute(candidate_links, df_products, df_invoice_lines_rl)
    return feature_vectors