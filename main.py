import pandas as pd
import streamlit as st
import plotly.express as px

df = pd.read_csv('path to df')
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')
df = df.dropna(subset=['InvoiceDate'])
df = df[(df['Quantity'] > 0) & (df['Price'] > 0)]

def quantityPrice():

    df_agg = df.groupby('Description').agg({'Price': 'mean','Quantity': 'sum'}).reset_index()

    st.title("Análise de Relação entre Preço e Quantidade Vendida")
    
    fig = px.scatter(df_agg,x='Price',y='Quantity',labels={'Price': 'Preço Médio', 'Quantity': 'Quantidade Vendida'},title='Relação entre Preço e Quantidade Vendida',hover_data=['Description'],color='Quantity',size='Quantity')
    
    st.plotly_chart(fig)

def profit():

    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['YearMonth'] = df['InvoiceDate'].dt.to_period('M').dt.strftime('%Y-%m')
    df['TotalValue'] = df['Quantity'] * df['Price']

    df_agg = df.groupby('YearMonth')['TotalValue'].sum().reset_index()

    all_months = pd.date_range(df['InvoiceDate'].min(), df['InvoiceDate'].max(), freq='MS').strftime('%Y-%m')
    all_months_df = pd.DataFrame(all_months, columns=['YearMonth'])
    all_months_df['TotalQuantity'] = 0

    df_merged = pd.merge(all_months_df, df_agg, on='YearMonth', how='left').fillna(0)

    st.title('Média de venda por mês')

    fig = px.bar(df_merged,x='YearMonth',y='TotalValue',labels={'YearMonth': 'Mês', 'TotalValue': 'Valor'})

    st.plotly_chart(fig)

def salesEvolution():
    df['YearMonth'] = df['InvoiceDate'].dt.to_period('M').dt.strftime('%Y-%m')

    st.title("Evolução das vendas por mês")

    produto_selecionado = st.selectbox("Escolha o produto:", ['Todos os produtos'] + list(df['Description'].unique()))
    
    if produto_selecionado != 'Todos os produtos':
        df_produto = df[df['Description'] == produto_selecionado]
    else:
        df_produto = df

    df_agg = df_produto.groupby('YearMonth')['Quantity'].sum().reset_index()

    all_months = pd.date_range(df_produto['InvoiceDate'].min(), df_produto['InvoiceDate'].max(), freq='MS').strftime('%Y-%m')
    all_months_df = pd.DataFrame(all_months, columns=['YearMonth'])
    all_months_df['Quantity'] = 0 

    df_merged = pd.merge(all_months_df, df_agg, on='YearMonth', how='left').fillna(0)

    df_merged['Quantity'] = df_merged['Quantity_y']
    df_merged = df_merged.drop(columns=['Quantity_x', 'Quantity_y'])

    fig = px.line(df_merged, x='YearMonth', y='Quantity', title=f"Quantidade de Vendas de {produto_selecionado} ao Longo do Tempo", markers=True)

    st.plotly_chart(fig)

def topProduct():

    df_agg = df.groupby('Description')['Quantity'].sum().reset_index()
    df_agg = df_agg.sort_values(by='Quantity', ascending=False).nlargest(10, 'Quantity')

    st.title("Top 10 produtos mais vendidos")

    fig = px.bar(df_agg, x='Description', y='Quantity', labels={'Quantity':'Quantidade','Description':'Produto'}, text_auto=True)

    st.plotly_chart(fig)


def countrySales():

    df_agg = df.groupby('Country')['Quantity'].sum().reset_index()
    df_agg = df_agg.sort_values(by='Quantity', ascending=False)

    st.title("Paises que mais compram")

    fig = px.bar(df_agg, x='Country', y='Quantity', labels={'Quantity':'Quantidade','Country':'País'})

    st.plotly_chart(fig)

def countryByClient():

    df['Customer ID'] = df['Customer ID'].dropna().astype(int)

    df_agg = df.groupby('Country')['Customer ID'].nunique().reset_index()
    df_agg = df_agg.sort_values(by='Customer ID', ascending=False).nlargest(10, 'Customer ID')

    st.title('Top 10 paises com mais clientes')

    fig = px.bar(df_agg,x='Country',y='Customer ID',labels={'Customer ID': 'Número de Clientes', 'Country': 'País'},text_auto=True,)

    st.plotly_chart(fig)

topProduct()
quantityPrice()
salesEvolution()
profit()
countrySales()
countryByClient()