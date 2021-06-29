import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')

# Adding an 'overweight' column
df['overweight'] = ( df['weight']/((df['height']/100)**2) ).apply(lambda x: 1 if x>25 else 0)

# Normalizing data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.

df['cholesterol'] = df['cholesterol'].apply(lambda x: 0 if x==1 else 1)
df['gluc'] = df['gluc'].apply(lambda x: 0 if x==1 else 1)

# Categorical Plot
def draw_cat_plot():
    # Creating DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.

    df_cat = pd.melt(df,id_vars = ['cardio'], value_vars = ['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])


    # Grouping and reformating the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    df_cat['total'] = 1
    df_cat = df_cat.groupby(['cardio','variable','value'], as_index = False).count()

    # Drawing the catplot with 'sns.catplot()'
    fig = sns.catplot(x='variable', y = 'total',data = df_cat, hue ='value', kind='bar',col = 'cardio').fig

    # saving the figure
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Cleaning the data
    df_heat = df[(df['ap_lo'] <= df['ap_hi']) & (df['height'] >= df['height'].quantile(0.025)) & (df['height'] <= df['height'].quantile(0.975)) & (df['weight'] >= df['weight'].quantile(0.025)) & (df['weight'] <= df['weight'].quantile(0.975))]

    # Calculating the correlation matrix
    corr = df_heat.corr(method = 'pearson')

    # Generating a mask for the upper triangle
    mask = np.triu(corr)

    fig, ax = plt.subplots(figsize = (10,10))

    # Drawing the heatmap with 'sns.heatmap()'
    ax = sns.heatmap(corr, mask = mask, linewidths=1, annot = True, square = True, fmt = '.1f', center = 0.08, cbar_kws = {'shrink':0.5} )

    # Saving the figure
    fig.savefig('heatmap.png')
    return fig
