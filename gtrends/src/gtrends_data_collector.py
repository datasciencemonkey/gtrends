"""
Created on Sat May 14 20:48:40 2016
@author: sagang
"""

from gt_parser.gTrendsParser import gTrends_Parser
google_terms = 'amazon, ebay'

"""str(raw_input("List terms that are of interest to you "
                             "(seperated by a comma - no whitespaces between commas)?"))"""

#Instantiate Parser Object

myParserObject = gTrends_Parser(google_terms)

# To make the parser collect raw data simply run
# This would produce two sets of dictionaries - one the entire blob & another one with just the data
# You have the option of collecting the results in two seperate dicts or just letting the data pass.
# The Parser Object stores the data in its internals
myParserObject.get_raw_data_blobs()

myParserObject.full_blob_dict  # has the entire data blob as a raw un-processed object

myParserObject.table_data_dict  # has just the raw data

myParserObject.get_column_names()  # parses and displays the column names

myParserObject.get_row_values()  # parses and displays row values

myParserObject.get_data_frame_raw()  # reads and converts data into a raw data frame - Dates still need to be processed

myParserObject.get_data_frame_processed()  # provides the fully converted data frame object for further processing







