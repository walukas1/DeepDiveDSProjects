import pandas as pd
def IDA(df, target,null_upper_lim, null_lower_lim):
  ''' This function returns the following information after inputting the data frame and identifying the target column where df must be a data frame and target must be a string name of column
null_upper_lim in decimal percent (0.4 = 40%) defines the threshhold of null data in feature in which more than will suggest to delete the column (think of better wording later)
null_lower_lim in decimal percent (0.02 = 2%) defines the threshhold of null data in a fueature in which less than it will suggest columns to delete rows in it that has nulls

Returns dict_keys(['DF rows', 'DF Columns', 'Total Nulls', 'Duplicate rows', 'meta_df', 'Target Name', 'Target count', 'Target Nulls', 'Target type', 'Drop columns', 'Drop rows'])
'''


#Check dataframe for size, shape, nulls and duplicates
  rows, columns = df.shape
  df_nulls = df.isnull().sum().sum()
  duplicates = df.duplicated().sum()
  meta_dict = {'DF rows' : rows, 'DF Columns' : columns, 'Total Nulls': df_nulls, 'Duplicate rows':duplicates}
  # print('--- Features Type, Uniques and Null Counts ---')
  meta_dict['meta_df'] = pd.concat([df.dtypes, df.nunique(), df.isnull().sum()], keys = ['Dtype', 'Uniques','Null Sum'], axis = 1)

# # Check target data
  target_nulls = df[target].isnull().sum()
  target_count = df[target].count()
  target_type = type(df[target][1])
  meta_dict.update([('Target Name',target),('Target count', target_count),('Target Nulls',target_nulls), ('Target type',target_type)])

  # print('--- Target Describe and Histogram ---')
  # print(df[target].describe().transpose())
  # target_plt = plt.hist(df[target], bins=20, label = target)
  # plt.title(target)
  # meta_dict['Target plt'] = target_plt

#Suggest columns and rows to drop based on nulls
  #Find location of nulls missing {null_upper_lim}% of data set
  filter_c = df.isnull().sum() > rows * null_upper_lim
  df_nulls = df.isnull().sum()
  drop_columns = df_nulls[filter_c]
  #Categories with only a few nulls ({null_lower_lim} % mising threshhold)
  filter_r = (df.isnull().sum() > 0) & (df.isnull().sum() < rows * null_lower_lim)
  drop_rows = df_nulls[filter_r]
  meta_dict.update([('Drop columns',drop_columns),('Drop rows',drop_rows)])
  return(meta_dict)
