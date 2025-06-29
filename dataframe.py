import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# read
df = pd.read_excel('dataframe.xlsx')
# df=pd.read_csv('dataframe.csv') 

# write df to excel
# df.to_excel('file.xlsx')

# For read/write individual sheets 
'''
xlsx = pd.ExcelFile('your_file.xlsx')
df_dict = pd.read_excel(xlsx, sheet_name=None)
# Access DataFrames by sheet name:
df1 = df_dict['Sheet1']
df2 = df_dict['Sheet2']

# write individual sheets
writer = pd.ExcelWriter('filename.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Sheet1')
# Apply formatting using xlsxwriter methods
writer.save()
'''

# take subset of the df

# .loc uses names   
# iloc uses integer index
col_names=df.columns.tolist()  # names of columns
two_rows=df.iloc[[0,2]]   # first and third data rows as a dataframe
first_two_rows=df.iloc[0:2]  # rows 0 through row 1
# pick out some columns
df_cols=df.loc[:, 'service':'provider']  # df of columns service through died
# if just one column, repeat the name twice to get the df and not a series
row4_value=df['MRN'][4] # returns value in col MRN, row labelled 4

col_died=df['died']  # returns a died "column" (type is a .Series)

# Create the histogram
plt.figure(figsize=(8, 6))  # Adjust figure size as needed
plt.hist(df['died'], bins=10, edgecolor='black')  # Customize bins and edge color
plt.xlabel('Died')
plt.ylabel('Frequency')
plt.title('Histogram of "died" Column')
plt.grid(True)
plt.show()

# Calculate histogram statistics using numpy if the column is NUMERIC. will not work if text.
counts, bins = np.histogram(df['MRN'])

# Create a new DataFrame
histogram_df = pd.DataFrame({'bin_edges': bins, 'counts': counts})

# Optional: Add descriptive column names
histogram_df = histogram_df.rename(columns={'bin_edges': 'Died Values', 'counts': 'Frequency'})

print(histogram_df)

# if the histogram is on dates, then use pandas hist()

# datatype check (attribute dypes of a dataframe)
# can use with df.dtypes: returns datatypes of each column

hist=df['died'].hist()  # Create a histogram directly and add this to the plot so can use plt.show()

df_day_series=df['died'].dt.day   # day of month died series. can use month or year as well.
df['new col']=df_day_series         # add a new column created from series
histogram_df = df['died'].value_counts().reset_index(name='counts') # create histogram based on values (date string)

# filter a DF with AND or OR (OR uses |)
filtered_df= df[df['MRN']>6]
filtered_df2 = df[(df['MRN'] > 10) & (df['MRN'] < 20)]
filtered_df3 = df[(df['MRN'] > 10) & (df['MRN'] < 20) & (df['died'] > pd.Timestamp('2022-01-01'))]
filtered_df4 = df[(df['died'] > df['died'][1]    )]  # df of those who died after value in row 1

# note the filtering has the original row number in the result
# so that if s1 is series (from a column), s1[3] will return the row named "3" but s1.iloc[0] will return the first row

# count records where MRN>2
count = df[df['MRN'] > 2].shape[0]  # Combine filtering and counting in one step

# groupby
# calculate the average MRN for each provider by using groupby. Can use this for histograms as well.
# so can groupby and then do a count
grouped_df=df.groupby('provider')   # returns a groupedby object!!!
# so here we can find the avg number of people who died by provider
average_mrn_df = grouped_df['died'].mean().reset_index()   # get mean, sum, count, std, max, min, etc.

# multiple field groups

grouped_data = df.groupby(["provider", "age"])
counts = grouped_data.size()   # counts is a series, so counts[3] will give the number of records for provider 3
# if using multiple groupby, then series has two indices, e.g., counts[2,3] will give number of records
# where provider is 2 and age is 3. 

print(counts)   # count records for each group

means = grouped_data["revenue"].mean()
print(means)

def custom_function(group):
    # Do something with the group
    result=group.size()
    # ....
    return result

results = grouped_data.apply(custom_function)
print(results)



# subset a dataframe
# can use df.head(3) or df.tail(3) to get the first 3 or last 3 rows
df.head(3)
df.tail(3)
new_df=df.iloc[0:3]   # first 3 rows (0 to 2)
new_df=df.iloc[-3:-1]   # last 2 rows

# concatenate dataframes with same columns so more rows (vertical concat)
combined_df = pd.concat([df, df], ignore_index=True)  # will reindex so that all indexes unique

# join or merge so add more columns. 
# Join joins on the index column. Merge uses a named column. 
# there should be no overlap in column names.
# inner = only if both indexes match... intersection (normal case)
# outer = don't drop any records... union
# left = first one determines the rows
# right = second one determines the rows

# if some columns have the same names, join needs to rename them. 
df1=df.tail(3)
df2=df.head(3)
joined_df = df1.join(df2, how='inner', lsuffix="_a")
# so inner join will return no rows since none match
# out join returns all elements in both with n/a in missing columns

# merge (is like join but you specify the column name to join on)
pd.merge(df1, df2, on='MRN', suffixes=('_a', '_b'))