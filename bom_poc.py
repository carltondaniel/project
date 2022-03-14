import pandas as pd
pd.options.mode.chained_assignment = None 
import numpy as np
import json
import copy


file1='/home/carlton/Downloads/bomsample1.xlsx'
file2='/home/carlton/Downloads/bomsample1_modified.xlsx'
bom_1_df=pd.read_excel(file1, sheet_name='Sheet1',index_col='RowID',na_values='empty')
bom_2_df=pd.read_excel(file2, sheet_name='Sheet1',index_col='RowID',na_values='empty')
rows_missing_bom_2=set(bom_1_df.index)-set(bom_2_df.index)
rows_missing_bom_1=set(bom_2_df.index)-set(bom_1_df.index)
columns_missing_bom2=set(bom_1_df.columns)-set(bom_2_df.columns)
columns_missing_bom1=set(bom_2_df.columns)-set(bom_1_df.columns)
columns_in_order=list(bom_1_df.columns)
index_in_order=list(bom_1_df.index)
for column in columns_missing_bom1:
    columns_in_order.insert(bom_2_df.columns.get_loc(column),column)
for row in rows_missing_bom_1:
    index_in_order.insert(row,row)
new_df=pd.DataFrame(columns=columns_in_order,index=index_in_order)
new_df = new_df.fillna("empty")
bom_2_df=bom_2_df.fillna("empty")
bom_1_df=bom_1_df.fillna("empty")
bom_1_changed_dimention=copy.deepcopy(bom_1_df)
bom_2_changed_dimention=copy.deepcopy(bom_2_df)
bom_1_changed_dimention[list(columns_missing_bom1)]="empty"
bom_2_changed_dimention[list(columns_missing_bom2)]="empty"  
for i in rows_missing_bom_1:
    bom_1_changed_dimention.loc[int(i)]="empty"
for i in rows_missing_bom_2:
    bom_2_changed_dimention.loc[int(i)]="empty"   
b1=bom_1_changed_dimention[columns_in_order]
b2=bom_2_changed_dimention[columns_in_order]
common_columns=set(bom_1_df.columns).intersection(set(bom_2_df.columns))
common_index=set(bom_1_df.index).intersection(set(bom_2_df.index))
error_list=[]
for columns in common_columns:
    for index in common_index:
        if bom_1_changed_dimention[columns][index]==bom_2_changed_dimention[columns][index]:
            new_df[columns][index]=bom_1_changed_dimention[columns][index]
        elif bom_1_changed_dimention[columns][index]!=bom_2_changed_dimention[columns][index]:
            temp=str(bom_1_changed_dimention[columns][index])+"->"+str(bom_2_changed_dimention[columns][index])
            new_df[columns][index]=temp
            
            x = {
          "error_type": "5",
          "note": "Field_Change",
          "column": str(columns),
          "row": str(index),
          "previous_state":str(temp.split("->")[0]),
          "current_state": str(temp.split("->")[1])
                }  
            error_list.append(x)
            
for  i in columns_missing_bom1:

    x = {
      "error_type": "1",
      "note": "New_Column",
      "column": str(i),
      "row": "",
      "previous_state":"",
      "current_state": ""
    }
    error_list.append(x)
    
for  i in columns_missing_bom2:

    x = {
      "error_type": "2",
      "note": "Missing_Colum",
      "column": str(i),
      "row": "",
      "previous_state":"",
      "current_state": ""
    }
    error_list.append(x)
    
for  i in rows_missing_bom_1:

    x = {
      "error_type": "3",
      "note": "New_Row",
      "column": "",
      "row": str(i),
      "previous_state":"",
      "current_state": ""
    }
    error_list.append(x)
    
for  i in rows_missing_bom_2:

    x = {
      "error_type": "4",
      "note": "Missing_row",
      "column": "",
      "row": str(i),
      "previous_state":"",
      "current_state": ""
    }
    error_list.append(x)
final_json_object = json.dumps(error_list)
new_df[list(columns_missing_bom2)]=bom_1_df[list(columns_missing_bom2)]
new_df[list(columns_missing_bom1)]=bom_2_df[list(columns_missing_bom1)]
new_df = new_df.fillna("empty")
for column in bom_1_df.columns:
    for row in rows_missing_bom_2:
        new_df[column][row]=bom_1_df[column][row]
        
for column in bom_2_df.columns:
    for row in rows_missing_bom_1:
        new_df[column][row]=bom_2_df[column][row]
    
new_df.insert(loc=0, column='RowID', value=new_df.index)

print(new_df)
print(json.dumps(error_list))
