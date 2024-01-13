# Hack for Sanuli.
# Read Kotus into dataframe to allow search based on letter locations.
import numpy as np
import pandas as pd

# Function to filter according to number of characters
def howManyLetters(df,num_letters):
   new_df = df[df[num_letters] =='']
   for i in range(num_letters-1,-1,-1):
      new_df = new_df[new_df[i] !='']
   return new_df

# Function to filter based on possible location of character
def charPossiblePlace(df,char,digits):
   new_df = df.copy(deep=True)
   total_df = None
   for digit in digits:
      sub_df = new_df[new_df[digit]==char]
      if total_df is None: total_df = sub_df
      else: total_df = pd.concat([total_df,sub_df],axis=0)
   total_df = total_df.drop_duplicates()
   return total_df
   

KOTUS_FILE_PATH = 'kotus-sanalista_v1.xml'

# Read
with open(KOTUS_FILE_PATH, 'r', encoding="utf-8") as f:
    data = f.readlines()

# Parse
row_list = data[12:-1]
parsed_row_list = []
max_letters = -1
for row in row_list:
   parsed_row = row.split('<s>')[-1].split('</s>')[0]
   parsed_row_list.append(parsed_row)
   if len(parsed_row) > max_letters:
      max_letters = len(parsed_row)

# Format to array
arr = np.empty((len(parsed_row_list),max_letters),dtype='str')
for i in range(0,len(parsed_row_list)):
   row = list(parsed_row_list[i])
   arr[i, :len(row)] = row

# Format to dataframe
df = pd.DataFrame(data=arr)

# Start filtering
vowels = ['a','e','i','o','u','y','ä','ö','å']

# Looking for a 6 letter word,
# with 'a' as 4th letter and
# 'u' as possibly 6th letter.
# No other vowels.
new_df = df[df[6] =='']
new_df = new_df[new_df[3] == 'a']
new_df = new_df[new_df[5] == 'u']
new_df = new_df[~new_df[0].isin(vowels)]
new_df = new_df[~new_df[1].isin(vowels)]
new_df = new_df[~new_df[2].isin(vowels)]
new_df = new_df[~new_df[4].isin(vowels)] 
print(new_df) # No entries, trying the second possibility

# Looking for a 6 letter word,
# with 'a' as 4th letter and
# 'u' as possibly 3rd letter.
# No other vowels.
new_df1 = df[df[6] =='']
new_df1 = new_df1[new_df1[3] == 'a']
new_df1 = new_df1[new_df1[2] == 'u']
new_df1 = new_df1[~new_df1[0].isin(vowels)]
new_df1 = new_df1[~new_df1[1].isin(vowels)]
new_df1 = new_df1[~new_df1[4].isin(vowels)]
new_df1 = new_df1[~new_df1[5].isin(vowels)]
print(new_df1) # One entry found: 'squash'. Hooray!


# Searching again, 13.1.2024
new_df2 = howManyLetters(df,6)

new_df2 = new_df2[new_df2[1]=='a']
new_df2 = charPossiblePlace(new_df2,'u',[0,2,4,5])
new_df2 = charPossiblePlace(new_df2,'i',[0,2,3])
new_df2 = charPossiblePlace(new_df2,'t',[0,3,4,5])
new_df2 = charPossiblePlace(new_df2,'n',[0,3,4,5])

print(new_df2) # One entry found: 'nainut'. Hooray!
