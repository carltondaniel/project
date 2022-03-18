import pandas as pd
import numpy as np
from datetime import date, datetime, time, timedelta
import os
os.chdir('D:\\longtail_Dimaag\\beam_code')

df=pd.read_csv('data_prep_60mins.csv')

##look forward into future 
target_slide=60
## the size of data defined by abhishek data
data_step_size=60
## window size defined to roll over 
window_size=180
## the window size  
slide_over=int(window_size/data_step_size)
#target sliding window size 
target_index=int((window_size+target_slide)/data_step_size)
## target colum
target_label=[]

target=df[target_label]
target = target.iloc[target_index-1:,:].reset_index(drop=True)

df.drop(target_label,axis=1,inplace=True)

for i in list(df.columns):
    if 'TIME' in i:
        df.drop(i,axis=1,inplace=True)

def window_stack(a, stepsize, width):
    n = a.shape[0]
    return np.hstack(a[i:1+n+i-width:stepsize] for i in range(0,width))

## column_names
columns_list=df.columns
if target_slide % data_step_size == 0:
    concatinated_list_names=[]
    all_names_list = [[] for i in range(0,slide_over)]

    for i in all_names_list:
        all_names_list.index(i)
        for j in columns_list:
            i.append(j+"_"+str(all_names_list.index(i)))

    for i in all_names_list:
        concatinated_list_names=concatinated_list_names+i
    
    ## creating the sliding data_frame
    windowed=window_stack(np.array(df),1,slide_over)
    
    ##target_colum
    # target_colum = []
    # target_df=pd.DataFrame(columns=target_label)
    # end=target_index-1
    # for j in target_label:
    #     for i in range(end,len(df)):
    #         try:
    #             print(i)
    #             target_colum.append(target[j][i])
    #         except:
    #             pass
    #     target_df[j] = target_colum
               
    
    final_df=pd.DataFrame(windowed,columns=concatinated_list_names)
    final_df = final_df.iloc[0:len(final_df)-1,:]
    shape=list(final_df.shape)
    final_df = pd.concat([final_df,target],axis=1)
    #final_df['target_column']=target_colum
    #final_df.target_colum[final_df.target_colum>=1]=1
    
    df_len=len(final_df)

# caliculate start end time 

    start_time_list=[]
    end_time_list=[]
    for i in range(0,len(final_df)):
        start=datetime.combine(date.today(), time(00,00, 00)) + timedelta(hours=i)
        start_time_list.append(str(start.time()))
        end=datetime.combine(date.today(), time(int(window_size/60),00, 00)) + timedelta(hours=i)
        end_time_list.append(str(end.time()))
    
        
    final_df.insert(loc=0, column='start_time', value=start_time_list)
       
    final_df.insert(loc=1, column='end_time', value=end_time_list)
    final_df.to_csv('windowed_data_P_W_'+str(window_size)+"_T_W_"+str(target_slide)+"_input_step_"+str(data_step_size)+'.csv',index=False)
   
else:
    print("the target window is not a multiple of target data step size ")