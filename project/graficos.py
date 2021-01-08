
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt

def graficar_distribucion(nf,ncol,datos):
    
    # Gráfico de distribución para cada variable numérica
    # ==============================================================================
    # Ajustar número de subplots en función del número de columnas
    fig_prueba, axes = plt.subplots(nrows=nf, ncols=ncol, figsize=(12, 8))
    axes = axes.flat
    columnas_numeric = datos.select_dtypes(include=['float64', 'int64']).columns
    columnas_numeric = columnas_numeric.drop(['id'])
    sns.set_theme(style="whitegrid")
    
    for i, colum in enumerate(columnas_numeric):
        sns.histplot(
            data    = datos,
            x       = colum,
            stat    = "count",
            kde     = True,
            palette='viridis',#color   = (list(plt.rcParams['axes.prop_cycle'])*2)[i]["color"],
            line_kws= {'linewidth': 2},
            alpha   = 0.3,
            ax      = axes[i]
        )
        axes[i].set_title(colum, fontsize = 10, fontweight = "bold")
        axes[i].tick_params(labelsize = 6)
        axes[i].set_xlabel("")
        
    fig_prueba.tight_layout()
    plt.subplots_adjust(top = 0.85)
    fig_prueba.suptitle('Distribución variables numéricas', fontsize = 10, fontweight = "bold");
        
    return fig_prueba


def grafico_altair_doble(data):
    source = data
    brush = alt.selection(type='interval')
    points = alt.Chart(source).mark_point().encode(
        x='budget:Q',
        y='revenue:Q',
        color=alt.condition(brush, 'Origin:N', alt.value('lightgray'))
    ).add_selection(
    brush
    )
    bars = alt.Chart(source).mark_bar().encode(
        y='Predominant_genre:N',
        color='Predominant_genre:N',
        x='count(Predominant_genre):Q'
    ).transform_filter(
        brush
    )
    visual=points & bars
    return visual



def grafico_scatter_doble(data):
    source = data
    brush = alt.selection(type='interval', resolve='global')
    base = alt.Chart(source).mark_point().encode(
        y='profitableness_MUS$',
        color=alt.condition(brush, 'Predominant_genre', alt.ColorValue('gray')),
    ).add_selection(
        brush
    ).properties(
        width=250,
        height=250
    )
    base.encode(x='budget') | base.encode(x='revenue')
    return base.encode(x='budget') | base.encode(x='revenue')


def grafico_voto_altair(data):
    
    source = data
    base = alt.Chart(source).encode(x='Predominant_genre:O')
    bar = base.mark_bar().encode(y='vote_average:Q')
    line =  base.mark_line(color='red').encode(
        y='vote_count/10:Q')
    text = line.mark_text(
        align='left',
        baseline='middle',
        dx=3  # Nudges text to right so it doesn't appear on top of the bar
    ).encode(
        text='# Films:Q'
    )
    aprw=(bar+line+text)
    return aprw


def grafico_vot(data):
    source = data
    b=alt.Chart(source).mark_circle().encode(
        alt.X('budget', scale=alt.Scale(zero=False)),
        alt.Y('profitableness_MUS$', scale=alt.Scale(zero=False, padding=1)),
        color='Predominant_genre',
        size='vote_average'
    )
    return b