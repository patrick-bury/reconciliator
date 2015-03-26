#!/usr/bin/python
import xlrd
import os
import datetime
#param_column=dict_to_list(loads(urllib.unquote_plus(params['column'])))

def xls(plugin_params):
    path=plugin_params['folder']
    file=plugin_params['file']
    sheet=int(plugin_params['sheet'])
    selected_columns=plugin_params['cols_to_import']
    output_format=plugin_params['output_format']
    rename=plugin_params['rename']
    format_date=plugin_params['format_date']
        
    param_column=process_param_columns(selected_columns)
    workbook=xlrd.open_workbook(path+file,logfile=open(os.devnull,'w'))
    worksheet=workbook.sheet_by_index(sheet)
    data=[]
    to_import_column=[]
    is_header=0
    num_rows= worksheet.nrows-1
    num_cells=worksheet.ncols-1
    curr_row = -1
    col_in_param=-1
    while curr_row < num_rows:
        curr_row += 1
        if(is_header==0):
            is_header=1
            xls_column=[]
            xls_column_name=[]
            curr_cell = -1
            while curr_cell < num_cells:
                curr_cell += 1
                cell_type = worksheet.cell_type(curr_row, curr_cell)
                cell_value = worksheet.cell_value(curr_row, curr_cell)
                cell_value=filter_cell(cell_type,cell_value)
                if cell_value in param_column:
                    col_in_param=param_column.index(cell_value)
                    to_import_column.append(curr_cell)
                    xls_column_name.append(cell_value)
                    xls_column.append(rename_cell(rename,curr_cell,col_in_param))
                    if rename==0:
                        xls_column.append(curr_cell)
                    else:
                        xls_column.append("data"+str(col_in_param))
        else:
            curr_cell=-1
            while(curr_cell<num_cells):
                curr_cell+=1
                if curr_cell in to_import_column:
                    cell_type = worksheet.cell_type(curr_row, curr_cell)
                    cell_value = worksheet.cell_value(curr_row, curr_cell)
                    cell_value=filter_cell(cell_type,cell_value)
                    cell_value=transcode_cell(cell_type,cell_value,format_date,workbook.datemode)
                    data.append(cell_value.encode('utf-8'))
    result=format_output(xls_column,xls_column_name,data,output_format)
    print ("Import of %s completed" % file)
    return(result)
    


def rename_cell(rename,curr_cell,col_in_param):
    if rename==0:
        value=curr_cell
    else:
        value="data"+str(col_in_param)
    return(value)
            
def process_param_columns(selected_columns):
    columns=selected_columns.split(',')
    param_column=[]
    for column in columns:
        column=column.replace('"',"")
        param_column.append(column)
    return(param_column)
        
def filter_cell(cell_type,cell_value):
    if cell_type==xlrd.XL_CELL_TEXT:
        cell_value=cell_value.replace('"',"'")
        cell_value=cell_value.replace('\r','@@@')
        cell_value=cell_value.replace('\n','@@@')
        cell_value=cell_value.replace('\t',' ')
    return(cell_value)
    
def transcode_cell(cell_type,cell_value,format_date,datemode):
    if cell_type==xlrd.XL_CELL_DATE and format_date==1:
        cell_value=datetime.datetime(*xlrd.xldate_as_tuple(cell_value,datemode))
        cell_value=cell_value.strftime('%m/%d/%Y %H:%M:%S')
    cell_value=str(cell_value)
    return(cell_value)

def format_output(xls_column,xls_column_name,data,output_format):
    if (output_format=='dict'):
        result=result_to_dict(xls_column_name,data)
    if (output_format=='serial'):
        result=php_serial(xls_column,data)
    return(result)

def result_to_dict(header,corpus):
    out={}
    for col in range(0,int(len(corpus)/len(header))):
        tmp={}
        i=0
        for line in range(0,len(header)):
            cell=corpus[line+col*len(header)]
            tmp[header[line]]=cell
        i=i+1                 
        out[col]=tmp
    return(out)
    
def php_serial(header,corpus):
    index=0
    out=dict()
    for col in range(0,len(header)):
        tmp=dict()
        i=0
        tmp.update({"title":header[col]})
        for line in range(0,len(corpus)/len(header)):
            cell=corpus[col+line*len(header)]
            tmp.update({i:cell})
            i=i+1
        out.update({header[col]:tmp}) 
        index+=1    
    return(out)
