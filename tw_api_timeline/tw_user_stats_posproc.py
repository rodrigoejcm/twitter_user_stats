import pandas as pd
import os
import json
import ast

### cria dataframe vazio
### buscas arquivos e  abre como dataframe
path = 'result_json/'
dataframes = []

for root, dirs, files in os.walk(path):
    for filename in files:

        df = pd.read_csv(path+filename, sep = "\t")
     
        soma = sum(ast.literal_eval(df['total_likes'].values[0]))
        df['total_likes_sum'] = soma
        soma = sum(ast.literal_eval(df['total_replies'].values[0]))
        df['total_replies_sum'] = soma
        soma = sum(ast.literal_eval(df['total_retweets'].values[0]))
        df['total_retweets_sum'] = soma

        df['total_retweets_mean'] = round(df['total_retweets_mean'],3)
        df['total_replies_mean'] = round(df['total_replies_mean'],3)
        df['total_likes_mean'] = round(df['total_likes_mean'],3)




        dataframes.append(df)


result_df_temp = pd.concat(dataframes)


columns = [ 'name',
            'id',
            'total_followers',
            'total_following',
            'total_posts',
            'total_likes_sum',
            'total_likes_mean',
            'total_likes_median',
            'total_retweets_sum',
            'total_retweets_mean',
            'total_retweets_median',
            'total_replies_sum',
            'total_replies_mean',
            'total_replies_median',
            'posts_count'
            ]



result_df = result_df_temp[columns]
result_df.to_csv("stats_results.csv", sep='\t')
