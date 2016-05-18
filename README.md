This package allows users to specify terms to the gtrends parser object to download, process google trends data.

*Note - There isn't an official Google trends API (at the moment)- this is just another way to get the data - please play nice when you use the code.*

The methods within the code give access to the data objects that may be of interest to you

An example of how the package can be used -

* Instantiate Parser Object & run all the methods below (copy paste to make it easy) & then select the object that is of interest to you

-- just pass in the actual terms you want to query seperated by a comma-- for example: google_terms = coffee, chocolate

myParserObject = gTrends_Parser(google_terms)  


-- To make the parser collect raw data simply run

myParserObject.get_raw_data_blobs()
-- This would produce two sets of dictionaries - one the entire blob & another one with just the data
-- You have the option of collecting the results in two seperate dicts or just letting the data pass.
-- The Parser Object stores the data in its internals

myParserObject.full_blob_dict   - *has the entire data blob as a raw un-processed object*

myParserObject.table_data_dict  - *has just the raw data*

myParserObject.get_column_names()  - *to process and display column names*

myParserObject.get_row_values()  - *to process and displays row values*

myParserObject.get_data_frame_raw()  - *reads and converts data into a raw data frame - Dates still need to be processed*

myParserObject.get_data_frame_processed()  - *provides the fully converted data frame object for further processing*


