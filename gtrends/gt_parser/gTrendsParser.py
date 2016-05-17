import pandas as pd
import requests
import ast

class gTrends_Parser(object):
    def __init__(self,google_terms):
        self.terms_tuple = (google_terms.split(','))
        self.actual_terms = [x.lstrip(' ') for x in self.terms_tuple]
        self.column_count = len(self.actual_terms)
        self.full_blob_dict = None
        self.table_data_dict = None
        self.column_name_dict = None
        self.row_value_dict = None
        self.raw_frame = None
        self.final_frame = None
        self.dummy_frame = None
        return

    def _get_gtrends_blob(self,actual_terms):
        """the function returns a dictionary that contains the returned js blob and
        another parsed dictionary that contains just the table results after
        collecting the data from google trends
        Ex:- resp_blob, table_dict = get_gtrends_blob(actual_terms)
        """
        content_resource = """http://www.google.com/trends/fetchComponent?q={0}&cid=TIMESERIES_GRAPH_0&export=3""".format(self.actual_terms)
        r = requests.get(content_resource)   #get request to the identified resource
        response = r.content   # push content into a seperate variable
        blob_dict = ast.literal_eval(response.decode().split('setResponse(')[1].rstrip()[:-2].replace('new Date', ''))   #returns parsed js blob
        table_dict = blob_dict['table']['rows']   #subset the blob to just collect the actual data
        return blob_dict,table_dict

    def get_raw_data_blobs(self):
        self.full_blob_dict, self.table_data_dict = self._get_gtrends_blob(self.actual_terms)
        return self.full_blob_dict, self.table_data_dict

    @staticmethod
    def _read_column_names(whole_blob_obj,column_count):
        """the function takes the whole blob obj and the column count variable
        and returns a dictionary of column names as captured on google trends
        Ex:- column_name_dict = _read_column_names(resp_blob,column_count)
        """
        columns={}
        for i in range(column_count+1):
            columns[i]=whole_blob_obj['table']['cols'][i]['label']
        return columns

    def get_column_names(self):
        self.column_name_dict = self._read_column_names(self.full_blob_dict,self.column_count)
        return self.column_name_dict

    @staticmethod
    def _read_rows(tbl_obj,column_count):
        """the function takes the table dictonary object and the column count variable
        to return a row data on the table in a dictonary format
        Ex:- my_rows = _read_row_values(table_dict,column_count)
        """
        rows={}
        for row_ix in range(len(tbl_obj)):
            columns ={}
            for i in range(column_count+1):
                columns[i]=tbl_obj[row_ix]['c'][i]['v']
            rows[row_ix]=columns
        return rows

    def get_row_values(self):
        self.row_value_dict = self._read_rows(self.table_data_dict,self.column_count)
        return self.row_value_dict

    @staticmethod
    def _generate_dataframe_obj(col_names_obj,row_values_obj):
        """func takes in column names dict and row value dict to mash up
        a pandas dataframe
        Ex:- my_frame= generate_dataframe_obj(column_name_dict,my_rows)
        """
        df = pd.DataFrame.from_dict(row_values_obj,orient='index')
        if not(len(col_names_obj)==len(df.columns)):
            assert('Too many column names or data frame columns. verify!')
        else:
            df.columns = col_names_obj.values()
        return df

    def get_data_frame_raw(self):
        self.raw_frame = self._generate_dataframe_obj(self.column_name_dict,self.row_value_dict)
        return self.raw_frame

    @staticmethod
    def _get_dates(dataframe):

        """
        Takes a raw gTrends Dframe - the output of the generate_dataframe_obj method and
        returns a usable dictionary of date strings.
        Note this func typically invoked via the gdate_to_pydate function. Check docstring
        for gdate_to_pydate function
        """
        pdate ={}
        for i in range(len(dataframe.Date)):
            year = str(dataframe.Date[i][0])
            month = str(dataframe.Date[i][1]+1)
            cal_date = str(dataframe.Date[i][2])
            pdate[i]= year+'-'+month+'-'+cal_date
        return pdate


    def _gdate_to_pydate(self,dframe):

        """
        Takes a raw gTrends Dframe - and returns a processed Data Frame with dates in
        string and manipulatable python date format. Uses get_dates method to process
        raw dates
        Ex:- my_processed_frame = gdate_to_pydate(my_frame)
        """
        dframe['str_date'] = pd.Series(self._get_dates(dframe), index = dframe.index)
        dframe['cal_date'] = pd.to_datetime(dframe['str_date'])
        return dframe

    def get_data_frame_processed(self):
        self.final_frame = self._gdate_to_pydate(self.raw_frame)
        return self.final_frame

