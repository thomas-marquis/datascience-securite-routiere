import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px

medianprops = {'color': 'black'}
meanprops = {'marker': 'o', 'markeredgecolor': 'black',
             'markerfacecolor': 'firebrick'}
boxplot_kwargs = dict(showfliers=False, medianprops=medianprops,
                      vert=False, patch_artist=True, showmeans=True, meanprops=meanprops)


def plot_killed(acc: pd.DataFrame):
    nb_usag_per_year = acc[['year', 'Num_Acc']] \
        .groupby(by='year') \
        .count() \
        .rename(columns={'Num_Acc': 'tot_victims'}) \
        .reset_index()
    nb_killed_per_year = acc.loc[acc['grav'] == 'killed', ['year', 'Num_Acc']] \
        .groupby(by='year') \
        .count() \
        .rename(columns={'Num_Acc': 'killed'}) \
        .reset_index()
    bilan = pd.merge(nb_usag_per_year, nb_killed_per_year,
                     on='year', how='inner')
    bilan = bilan.reset_index()

    fig = px.bar(bilan, x='year', y='killed')
    fig.show()

    return bilan, fig


def plot_bilan(df: pd.DataFrame):
    df_to_plot = df.copy()
    df_to_plot = df_to_plot \
        .groupby(by=['year', 'grav']) \
        .count() \
        .reset_index()
    fig = px.bar(df_to_plot, x='year', y='Num_Acc',
                 color='grav', labels={'Num_Acc': 'victims'})
    fig.show()
    return df_to_plot, fig


def plot_box_cat(df, cat_col_name, num_col_name, **kwargs) -> None:
    groupes = []
    names = df[cat_col_name].unique()
    for name in names:
        groupes.append(df.loc[df[cat_col_name] == name, num_col_name])

    plt.boxplot(groupes, labels=names, **boxplot_kwargs, **kwargs)
    plt.show()
