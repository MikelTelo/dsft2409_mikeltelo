import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib
from utils.campaign_utils import (
    load_and_preprocess_data,
    perform_clustering,
    create_cluster_radar_chart,
    calculate_campaign_metrics,
    update_campaign_assignments,
    adjust_adspend_automatically,
    create_campaign_analysis_charts,
    calculate_conversion_metrics,
    get_original_cluster_assignments,
    create_adspend_distribution_charts
)

# Page config
st.set_page_config(page_title="Marketing Campaign Optimizer", layout="wide", initial_sidebar_state="collapsed")

# Title
st.title("🎯 Marketing Campaign Optimizer")

# Load data and model
@st.cache_data
def load_initial_data():
    df = load_and_preprocess_data("data/digital_marketing_campaign_dataset.csv")
    model = joblib.load("model/RandomForest_best_pipeline.pkl")
    return df, model

df, model = load_initial_data()

# Step 1: Original Campaign Analysis
st.header("1. Análisis de Campaña Original")

# Campaign Overview Metrics
metrics = calculate_conversion_metrics(df)

# Display metrics in tabs
tab1, tab2 = st.tabs(["Métricas por Tipo de Campaña", "Métricas por Canal"])

with tab1:
    st.subheader("Rendimiento por Tipo de Campaña")
    campaign_metrics_df = pd.DataFrame([
        {
            'Tipo': campaign_type,
            'Total Clientes': metrics['total_customers'],
            'Conversiones': metrics['conversions'],
            'Tasa de Conversión': f"{metrics['conversion_rate']:.2%}",
            'Gasto Total': f"${metrics['total_spend']:,.2f}",
            'Gasto Promedio': f"${metrics['avg_spend']:,.2f}",
            'Costo por Conversión': f"${metrics['cost_per_conversion']:,.2f}"
        }
        for campaign_type, metrics in metrics['campaign_types'].items()
    ])
    st.dataframe(campaign_metrics_df, use_container_width=True)

with tab2:
    st.subheader("Rendimiento por Canal")
    channel_metrics_df = pd.DataFrame([
        {
            'Canal': channel,
            'Total Clientes': metrics['total_customers'],
            'Conversiones': metrics['conversions'],
            'Tasa de Conversión': f"{metrics['conversion_rate']:.2%}",
            'Gasto Total': f"${metrics['total_spend']:,.2f}",
            'Gasto Promedio': f"${metrics['avg_spend']:,.2f}",
            'Costo por Conversión': f"${metrics['cost_per_conversion']:,.2f}"
        }
        for channel, metrics in metrics['channels'].items()
    ])
    st.dataframe(channel_metrics_df, use_container_width=True)

# Campaign Analysis Charts
st.subheader("Análisis Visual de la Campaña")
fig1, fig2, fig3, fig4 = create_campaign_analysis_charts(df)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig1, use_container_width=True)
    st.plotly_chart(fig3, use_container_width=True)
with col2:
    st.plotly_chart(fig2, use_container_width=True)
    st.plotly_chart(fig4, use_container_width=True)

# Step 2: Cluster Analysis and Assignment
st.header("2. Análisis de Clusters y Asignación")

# Perform clustering
cluster_labels, cluster_metrics, data_scaled, scaler = perform_clustering(df)
df['cluster'] = cluster_labels

# Cluster Selection and Analysis
col1, col2 = st.columns([1, 2])

with col1:
    selected_cluster = st.selectbox("Seleccionar Cluster para Analizar", range(len(cluster_metrics)))
    
    # Cluster Metrics
    st.subheader(f"Métricas del Cluster {selected_cluster}")
    cluster_data = df[df['cluster'] == selected_cluster]
    
    metrics = {
        "Tamaño del Cluster": f"{len(cluster_data):,}",
        "Tasa de Conversión Actual": f"{cluster_data['Conversion'].mean():.2%}",
        "Gasto Promedio": f"${cluster_data['AdSpend'].mean():,.2f}",
        "Gasto Total": f"${cluster_data['AdSpend'].sum():,.2f}"
    }
    
    for metric, value in metrics.items():
        st.metric(metric, value)

with col2:
    # Radar Chart for selected cluster
    st.plotly_chart(create_cluster_radar_chart(cluster_metrics, selected_cluster), use_container_width=True)

# Campaign Assignment Section
st.subheader("Asignación de Campaña y Canal")

# Create a DataFrame for cluster assignments
if 'cluster_assignments' not in st.session_state:
    # Get original assignments
    st.session_state.cluster_assignments = get_original_cluster_assignments(df)

# Display cluster assignments in an editable table with original values
edited_df = st.data_editor(
    st.session_state.cluster_assignments,
    column_config={
        'Cluster': st.column_config.NumberColumn(
            'Cluster',
            help="Número de cluster",
            disabled=True
        ),
        'Tipo de Campaña': st.column_config.SelectboxColumn(
            'Tipo de Campaña',
            options=['Awareness', 'Consideration', 'Conversion', 'Retention'],
            required=True
        ),
        'Canal': st.column_config.SelectboxColumn(
            'Canal',
            options=['Email', 'PPC', 'Referral', 'SEO', 'Social Media'],
            required=True
        )
    },
    num_rows="fixed",
    use_container_width=True
)

# Step 3: Campaign Optimization and Prediction
st.header("3. Optimización y Predicción de Campaña")

if st.button("Optimizar y Predecir Resultados"):
    # Update assignments
    campaign_type_assignments = dict(zip(edited_df['Cluster'], edited_df['Tipo de Campaña']))
    channel_assignments = dict(zip(edited_df['Cluster'], edited_df['Canal']))
    
    # Update DataFrame with new assignments
    df_mod = update_campaign_assignments(df, cluster_labels, campaign_type_assignments, channel_assignments)
    
    # Automatically adjust AdSpend
    df_mod = adjust_adspend_automatically(df, df_mod, campaign_type_assignments)
    
    # Make predictions
    X_mod = df_mod.drop(columns=['Conversion', 'CustomerID', 'cluster'])
    predictions = model.predict_proba(X_mod)[:, 1]
    df_mod['Predicted_Conversion'] = predictions
    
    # Display Results
    st.subheader("Resultados de la Optimización")
    
    # Key Metrics Comparison
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Conversiones Originales",
            f"{df['Conversion'].sum():,}",
            f"Tasa Base: {df['Conversion'].mean():.2%}"
        )
    
    with col2:
        predicted_conversions = (df_mod['Predicted_Conversion'] > 0.5).sum()
        st.metric(
            "Conversiones Predichas",
            f"{predicted_conversions:,}",
            f"{((predicted_conversions / len(df_mod)) - df['Conversion'].mean()) * 100:+.1f}% Cambio"
        )
    
    with col3:
        original_spend = df['AdSpend'].sum()
        new_spend = df_mod['AdSpend'].sum()
        st.metric(
            "Eficiencia del Presupuesto",
            f"${new_spend/predicted_conversions:,.2f}/conversión",
            f"{((new_spend/predicted_conversions) / (original_spend/df['Conversion'].sum()) - 1) * 100:+.1f}% Costo por Conversión"
        )
    
    # Detailed Metrics for Optimized Campaign
    st.subheader("Métricas Detalladas de la Campaña Optimizada")
    
    # Calculate metrics for optimized campaign
    df_mod['Conversion'] = df_mod['Predicted_Conversion'] > 0.5
    optimized_metrics = calculate_conversion_metrics(df_mod)
    
    # Display metrics in tabs
    tab1, tab2 = st.tabs(["Métricas por Tipo de Campaña", "Métricas por Canal"])
    
    with tab1:
        st.subheader("Rendimiento por Tipo de Campaña")
        campaign_metrics_df = pd.DataFrame([
            {
                'Tipo': campaign_type,
                'Total Clientes': metrics['total_customers'],
                'Conversiones': metrics['conversions'],
                'Tasa de Conversión': f"{metrics['conversion_rate']:.2%}",
                'Gasto Total': f"${metrics['total_spend']:,.2f}",
                'Gasto Promedio': f"${metrics['avg_spend']:,.2f}",
                'Costo por Conversión': f"${metrics['cost_per_conversion']:,.2f}"
            }
            for campaign_type, metrics in optimized_metrics['campaign_types'].items()
        ])
        st.dataframe(campaign_metrics_df, use_container_width=True)
    
    with tab2:
        st.subheader("Rendimiento por Canal")
        channel_metrics_df = pd.DataFrame([
            {
                'Canal': channel,
                'Total Clientes': metrics['total_customers'],
                'Conversiones': metrics['conversions'],
                'Tasa de Conversión': f"{metrics['conversion_rate']:.2%}",
                'Gasto Total': f"${metrics['total_spend']:,.2f}",
                'Gasto Promedio': f"${metrics['avg_spend']:,.2f}",
                'Costo por Conversión': f"${metrics['cost_per_conversion']:,.2f}"
            }
            for channel, metrics in optimized_metrics['channels'].items()
        ])
        st.dataframe(channel_metrics_df, use_container_width=True)
    
    # Comparative Analysis
    st.subheader("Análisis Comparativo")
    
    # First row: Conversion comparisons
    tab3, tab4 = st.tabs(["Por Tipo de Campaña", "Por Canal"])
    
    with tab3:
        # Campaign Type Performance
        fig = go.Figure()
        campaign_types = ['Awareness', 'Consideration', 'Conversion', 'Retention']
        
        # Original conversions
        original_conversions = []
        for ct in campaign_types:
            mask = df[f'CampaignType_{ct}'] == 1
            original_conversions.append(df[mask]['Conversion'].sum())
        
        # Predicted conversions
        predicted_conversions = []
        for ct in campaign_types:
            mask = df_mod[f'CampaignType_{ct}'] == 1
            predicted_conversions.append(df_mod[mask]['Conversion'].sum())
        
        fig.add_trace(go.Bar(
            name="Original",
            x=campaign_types,
            y=original_conversions,
            marker_color='lightblue'
        ))
        
        fig.add_trace(go.Bar(
            name="Optimizado",
            x=campaign_types,
            y=predicted_conversions,
            marker_color='lightgreen'
        ))
        
        fig.update_layout(
            title="Conversiones por Tipo de Campaña",
            barmode='group',
            xaxis_title="Tipo de Campaña",
            yaxis_title="Número de Conversiones",
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        # Channel Performance
        fig = go.Figure()
        channels = ['Email', 'PPC', 'Referral', 'SEO', 'Social Media']
        
        # Original conversions
        original_conversions = []
        for ch in channels:
            mask = df[f'CampaignChannel_{ch}'] == 1
            original_conversions.append(df[mask]['Conversion'].sum())
        
        # Predicted conversions
        predicted_conversions = []
        for ch in channels:
            mask = df_mod[f'CampaignChannel_{ch}'] == 1
            predicted_conversions.append(df_mod[mask]['Conversion'].sum())
        
        fig.add_trace(go.Bar(
            name="Original",
            x=channels,
            y=original_conversions,
            marker_color='lightblue'
        ))
        
        fig.add_trace(go.Bar(
            name="Optimizado",
            x=channels,
            y=predicted_conversions,
            marker_color='lightgreen'
        ))
        
        fig.update_layout(
            title="Conversiones por Canal",
            barmode='group',
            xaxis_title="Canal",
            yaxis_title="Número de Conversiones",
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # AdSpend Distribution Analysis
    st.subheader("Distribución de AdSpend")
    col1, col2 = st.columns(2)
    
    with col1:
        # Channel AdSpend box plot
        fig = go.Figure()
        
        for channel in channels:
            # Original data
            channel_data_orig = df[df[f'CampaignChannel_{channel}'] == 1]['AdSpend']
            fig.add_trace(go.Box(
                y=channel_data_orig,
                name=channel,
                boxpoints=False,
                offsetgroup='Original',
                legendgroup='Original',
                marker_color='lightblue'
            ))
            
            # Modified data
            channel_data_mod = df_mod[df_mod[f'CampaignChannel_{channel}'] == 1]['AdSpend']
            fig.add_trace(go.Box(
                y=channel_data_mod,
                name=channel,
                boxpoints=False,
                offsetgroup='Optimizado',
                legendgroup='Optimizado',
                marker_color='lightgreen'
            ))
        
        fig.update_layout(
            title="Distribución de AdSpend por Canal",
            yaxis_title="AdSpend",
            boxmode='group',
            xaxis_tickangle=45,
            template="plotly_white",
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Campaign Type AdSpend box plot
        fig = go.Figure()
        
        for c_type in campaign_types:
            # Original data
            type_data_orig = df[df[f'CampaignType_{c_type}'] == 1]['AdSpend']
            fig.add_trace(go.Box(
                y=type_data_orig,
                name=c_type,
                boxpoints=False,
                offsetgroup='Original',
                legendgroup='Original',
                marker_color='lightblue'
            ))
            
            # Modified data
            type_data_mod = df_mod[df_mod[f'CampaignType_{c_type}'] == 1]['AdSpend']
            fig.add_trace(go.Box(
                y=type_data_mod,
                name=c_type,
                boxpoints=False,
                offsetgroup='Optimizado',
                legendgroup='Optimizado',
                marker_color='lightgreen'
            ))
        
        fig.update_layout(
            title="Distribución de AdSpend por Tipo de Campaña",
            yaxis_title="AdSpend",
            boxmode='group',
            xaxis_tickangle=45,
            template="plotly_white",
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by Your Team") 