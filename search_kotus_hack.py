# Hack for Sanuli.
# Read Kotus into dataframe to allow search based on letter locations.
import numpy as np
import pandas as pd
import itertools
EMPTY_CHAR = '_'

# Function to filter according to number of characters
def howManyLetters(df,num_letters):
   new_df = df[df[num_letters] ==EMPTY_CHAR]
   for i in range(num_letters-1,-1,-1):
      new_df = new_df[new_df[i] !=EMPTY_CHAR]
   return new_df

# Function to filter based on possible location of character.
# Obsolete, since multiCharPossiblePlace can be run with
# num_instances=1, which performs the same function.
def charPossiblePlace(df,char,digits):
   new_df = df.copy(deep=True)
   total_df = None
   for digit in digits:
      sub_df = new_df[new_df[digit]==char]
      if total_df is None: total_df = sub_df
      else: total_df = pd.concat([total_df,sub_df],axis=0)
   total_df = total_df.drop_duplicates()
   return total_df


# Function to filter based on possible location of character,
# taking into account the possibility of two or more instances of it.
def multiCharPossiblePlace(df,char,digits,num_instances):
   new_df = df.copy(deep=True)
   total_df = None
   combinations = list(itertools.combinations(digits,num_instances))
   for combination in combinations:
      sub_df = None
      for location in digits:
         if location in combination:
            if sub_df is None: sub_df = new_df[new_df[location]==char]
            else: sub_df = sub_df[sub_df[location]==char]
         else:
            if sub_df is None: sub_df = new_df[new_df[location]!=char]
            else: sub_df = sub_df[sub_df[location]!=char]
      if total_df is None: total_df = sub_df
      else: total_df = pd.concat([total_df,sub_df],axis=0)
   # Digits tell the possible places, now get rid of impossible ones.
   for col in total_df:
      if col not in digits:
         total_df = total_df[total_df[col]!=char]
   return total_df


# Function to filter based on possible location of character,
# taking into account the possibility of two or more instances of it.
# In addition, take into account the possibility for a list of number of instances.
def multiCharMultiPossiblePlace(df,char,digits,num_instances_list):
   new_df = df.copy(deep=True)
   total_df = None
   combinations = []
   for num_instances in num_instances_list:
      combinations = combinations + list(itertools.combinations(digits,num_instances))
   for combination in combinations:
      sub_df = None
      for location in digits:
         if location in combination:
            if sub_df is None: sub_df = new_df[new_df[location]==char]
            else: sub_df = sub_df[sub_df[location]==char]
         else:
            if sub_df is None: sub_df = new_df[new_df[location]!=char]
            else: sub_df = sub_df[sub_df[location]!=char]
      if total_df is None: total_df = sub_df
      else: total_df = pd.concat([total_df,sub_df],axis=0)
   # Digits tell the possible places, now get rid of impossible ones.
   for col in total_df:
      if col not in digits:
         total_df = total_df[total_df[col]!=char]
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
arr = np.full((len(parsed_row_list),max_letters),EMPTY_CHAR,dtype='str')
for i in range(0,len(parsed_row_list)):
   #row = list(parsed_row_list[i])
   row = list(parsed_row_list[i].lower())
   arr[i, :len(row)] = row

# Format to dataframe
df = pd.DataFrame(data=arr)
df = df.drop_duplicates()

# Start filtering
vowels = ['a','e','i','o','u','y','ä','ö','å']

# Looking for a 6 letter word,
# with 'a' as 4th letter and
# 'u' as possibly 6th letter.
# No other vowels.
new_df = df[df[6] ==EMPTY_CHAR]
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
new_df1 = df[df[6] ==EMPTY_CHAR]
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


# Sanity check. Works as intended
new_df3 = howManyLetters(df,4)
new_df3 = charPossiblePlace(new_df3,'t',[0,2])
new_df3 = charPossiblePlace(new_df3,'o',[1,3])
# Returns many options

new_df4 = howManyLetters(df,4)
new_df4 = multiCharPossiblePlace(new_df4,'t',[0,2],2)
new_df4 = multiCharPossiblePlace(new_df4,'o',[1,3],2)
# Returns only "toto". Hooray!

new_df5 = howManyLetters(df,6)
new_df5 = multiCharPossiblePlace(new_df5,'t',[0,2,4],3)
new_df5 = multiCharPossiblePlace(new_df5,'o',[1,3],2)
# Returns only "totota". Hooray!

new_df6 = howManyLetters(df,6)
new_df6 = multiCharPossiblePlace(new_df6,'t',[0,2,4],2)
new_df6 = multiCharPossiblePlace(new_df6,'o',[1,3],2)
# Returns only "lotota". Hooray!


# Search again, 23.3.2024
new_dfa = howManyLetters(df,6)
new_dfa = new_dfa[new_dfa[1]=='e']
new_dfa = multiCharMultiPossiblePlace(new_dfa,'t',[0,2,3,5],[1,2,3])
new_dfa = multiCharMultiPossiblePlace(new_dfa,'o',[0,2,3,4],[1,2,3])
new_dfa = multiCharMultiPossiblePlace(new_dfa,'n',[0,3,4,5],[1,2,3])

new_dfb = howManyLetters(df,6)
new_dfb = multiCharMultiPossiblePlace(new_dfb,'i',[0,3,5],[1,2,3])
new_dfb = multiCharMultiPossiblePlace(new_dfb,'n',[1,2,3,4,5],[1,2,3,4,5])
new_dfb = multiCharMultiPossiblePlace(new_dfb,'m',[0,1,2,4,5],[1,2,3,4,5])
new_dfb = multiCharMultiPossiblePlace(new_dfb,'u',[0,2,3,4,5],[1,2,3,4,5])
new_dfb = multiCharMultiPossiblePlace(new_dfb,'d',[0,1,2,4,5],[1,2,3,4,5])
