import camelot

def extract_pdf_tables(filepath):
    tables = camelot.read_pdf(filepath, flavor="stream", pages="all")
    dfs = [table.df for table in tables]
    return dfs
