# import the modules
import pandas as pd 
from sqlalchemy import create_engine
import pandas as pd
from sklearn.cluster import KMeans
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler

  
# SQLAlchemy connectable
#cnx = create_engine('sqlite:///database.db').connect()


# table named 'contacts' will be returned as a dataframe.
#df = pd.read_sql_table('user', cnx)
def encoding(enc_string, df):
  enc = OneHotEncoder(handle_unknown='ignore')
  enc_df = df[[enc_string]]
  X = enc_df.to_numpy()
  enc.fit(X)
  g = enc.transform(X).toarray()
  names = enc.get_feature_names_out([''])
  arr = pd.DataFrame(g, columns = names)
  return arr

def kmeans(df, k):
  #	aesthetic	Sports	Cooking/Baking	Singing	Video Games	TV Shows/Youtube	Reading/Self Learning	Outdoor Recreation	Arts and Crafts	Traveling	Music	religion	Acts of Service	Quality Time	Physical Touch	Gift Giving	Words of Affirmation
  kmeans_df = df.drop(columns = ['age', 'preferred_age','height', 'preferred_height','race', 'preferred_race', 'mbti'])
  X = kmeans_df.drop(columns = ['name', 'gender', 'email'])
  scaler = StandardScaler()
  X = scaler.fit_transform(X)

  kmeans = KMeans(n_clusters=k, random_state=0).fit(X)
  res = kmeans.labels_
  df['group'] = res
  return df

def sort_into_groups(df, k):
  d = {}
  for x in range(k):
      d["group_{0}".format(x)] = df[df['group'] == x]
  return d

def compatible_height_calc (group):
  compat_height = np.subtract.outer(group['height'].to_numpy(), group['preferred_height'].to_numpy())
  compat_height = np.absolute(compat_height)
  compat_height = compat_height/np.amax(compat_height)
  compat_height = 1- compat_height
  return compat_height

def compatible_race_calc (group):
  compat_race = np.equal.outer(group['race'].to_numpy(), group['preferred_race'].to_numpy())
  return compat_race

def compatible_age_calc (group):
  compat_age = np.subtract.outer(group['age'].to_numpy(), group['preferred_age'].to_numpy())
  compat_age = np.absolute(compat_age)
  compat_age = compat_age/np.amax(compat_age)
  compat_age = 1- compat_age
  return compat_age

def compatible_personality_chart():
  personality_chart = np.array([[.75, .75, .75, 1, .75, 1, .75, .75, 0, 0, 0, 0, 0, 0, 0, 0],
                             [.75, .75, 1, .75, 1, .75, .75, .75, 0, 0, 0, 0, 0, 0, 0, 0],
                             [.75, 1, .75, .75, .75, .75, .75, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                             [1, .75, .75, .75, .75, .75, .75, .75, 1, 0, 0, 0, 0, 0, 0, 0],
                             [.75, 1, .75, .75, .75, .75, .75, 1, .5, .5, .5, .5, .25, .25, .25, .25],
                             [1, .75, .75, .75, .75, .75, 1, .75, .5, .5, .5, .5, .5, .5, .5, .5],
                             [.75, .75, .75, .75, .75, 1, .75, .75, .5, .5, .5, .5, .25, .25, .25, 1],
                             [.75, .75, 1, .75, 1, .75, .75, .75, .5, .5, .5, .5, .25, .25, .25, .25],
                             [0, 0, 0, 1, .5, .5, .5, .5, .25, .25, .25, .25, .5, 1, .5, 1],
                             [0, 0, 0, 0, .5, .5, .5, .5, .25, .25, .25, .25, 1, .5, 1, .5],
                             [0, 0, 0, 0, .5, .5, .5, .5, .25, .25, .25, .25, .5, 1, .5, 1],
                             [0, 0, 0, 0, .5, .5, .5, .5, .25, .25, .25, .25, 1, .5, 1, .5],
                             [0, 0, 0, 0, .25, .5, .25, .25, .5, 1, .5, 1, .75, .75, .75, .75],
                             [0, 0, 0, 0, .25, .5, .25, .25, 1, .5, 1, .5, .75, .75, .75, .75],
                             [0, 0, 0, 0, .25, .5, .25, .25, .5, 1, .5, 1, .75, .75, .75, .75],
                             [0, 0, 0, 0, .25, .5, 1, .25, 1, .5, 1, .5, .75, .75, .75, .75]])

  personality_names = ['INFP', 'ENFP', 'INFJ', 'ENFJ', 'INTJ', 'ENTJ', 'INTP', 'ENTP',
                     'ISFP', 'ESFP', 'ISTP', 'ESTP', 'ISFJ', 'ESFJ', 'ISTJ', 'ESTJ']

  personality_df = pd.DataFrame(personality_chart, columns = personality_names, index = personality_names)
  return personality_df

def compatible_personality_calc (group, personality_chart):
  per = group['mbti'].to_numpy()
  compat_per = np.zeros((len(per),len(per)))
  for x in range(len(per)):
    for y in range(len(per)):
      compat_per[x][y] = personality_chart.loc[per[x]][per[y]]
  return compat_per

def array_of_tuple_matches (group, final_compatible_chart):
  names = group['name'].tolist()
  emails = group['email'].tolist()
  gender = group['gender'].tolist()
  index_list_of_females = [i for i, x in enumerate(gender) if x == "F"]
  index_list_of_males = [i for i, x in enumerate(gender) if x == "M"]
  M_names = [names[i] for i in index_list_of_males]
  M_emails = [emails[i] for i in index_list_of_males]
  F_names = [names[i] for i in index_list_of_females]
  F_emails = [emails[i] for i in index_list_of_females]

  arr = []
  for x in range(len(names)):
    if gender[x] == 'M':
      F_final_compat = [final_compatible_chart[x][i] for i in index_list_of_females]
      arr.append(sorted(zip(F_final_compat, F_names,F_emails), reverse=True)[:3])
    else:
      M_final_compat = [final_compatible_chart[x][i] for i in index_list_of_males]
      arr.append(sorted(zip(M_final_compat, M_names, M_emails), reverse=True)[:3])


  return arr

def df_with_best_matches (arr, group):
  match_names = ['Best Match 1', 'Best Match 2', 'Best Match 3']
  match_df = pd.DataFrame(arr, columns = match_names)
  match_df.reset_index(drop=True, inplace=True)
  group.reset_index(drop=True, inplace=True)
  res = pd.concat([group, match_df], axis =1)
  res['Best Match 1 Email'] = res['Best Match 1'].apply(lambda x: x[2] if x != None else None)
  res['Best Match 2 Email'] = res['Best Match 2'].apply(lambda x: x[2] if x != None else None)
  res['Best Match 3 Email'] = res['Best Match 3'].apply(lambda x: x[2] if x != None else None)
  res['Best Match 1 Score'] = res['Best Match 1'].apply(lambda x: x[0] if x != None else None)
  res['Best Match 2 Score'] = res['Best Match 2'].apply(lambda x: x[0] if x != None else None)
  res['Best Match 3 Score'] = res['Best Match 3'].apply(lambda x: x[0] if x != None else None)
  res['Best Match 1 Name'] = res['Best Match 1'].apply(lambda x: x[1] if x != None else None)
  res['Best Match 2 Name'] = res['Best Match 2'].apply(lambda x: x[1] if x != None else None)
  res['Best Match 3 Name'] = res['Best Match 3'].apply(lambda x: x[1] if x != None else None)

  final_table = res[['name', 'email', 
                     'Best Match 1 Name', 'Best Match 1 Email', 'Best Match 1 Score', 
                     'Best Match 2 Name', 'Best Match 2 Email', 'Best Match 2 Score',
                     'Best Match 3 Name', 'Best Match 3 Email', 'Best Match 3 Score']]
  return final_table

#df = pd.read_excel("/content/Test Dataset for Algorithm.xlsx")
#df = df.head(100)
def main_algo (df):

    aes_arr = encoding('aesthetic', df)
    rel_arr = encoding('religion', df)
    df = pd.concat([df, aes_arr, rel_arr], axis=1).drop(columns = ['aesthetic', 'religion'])
    number_of_cluster = 3
    df = kmeans(df, number_of_cluster)
    groups = sort_into_groups(df,number_of_cluster)

    for gp in groups.keys():
        compat_height = compatible_height_calc(groups[gp])
        compat_age = compatible_age_calc(groups[gp])
        compat_race = compatible_race_calc(groups[gp])
        compat_per = compatible_personality_calc(groups[gp], compatible_personality_chart())
        final_compatibility = 15 * compat_age + 25 * compat_height + 35 * compat_race + 25 * compat_per
        np.fill_diagonal(final_compatibility, 0)
        arr = array_of_tuple_matches(groups[gp], final_compatibility)
        result = df_with_best_matches(arr, groups[gp])
        groups[gp] = result
    return groups

#final_lst = groups['group_0'.values.tolist()]
#for gp in range(1, len(groups.keys())):
  #finals_lst = np.concatenate((final_lst, groups[gp].values.tolist()), axis =0)
#final_lst
#final_df = pd.DataFrame(final_lst, columns = ['Email', 'Best Match 1 Email', 'Best Match 1 Score', 
                     #'Best Match 2 Email', 'Best Match 2 Score',
                     #'Best Match 3 Email', 'Best Match 3 Score'])
#final_df
