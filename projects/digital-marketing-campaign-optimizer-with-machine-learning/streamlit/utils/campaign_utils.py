import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import plotly.graph_objects as go
import plotly.express as px

def load_and_preprocess_data(data_path):
    """Load and preprocess the marketing campaign data."""
    df = pd.read_csv(data_path)
    
    # Convert categorical variables to dummy variables if not already done
    categorical_columns = ['Gender', 'CampaignChannel', 'CampaignType']
    for col in categorical_columns:
        if col in df.columns:
            df = pd.get_dummies(df, columns=[col], drop_first=False)
    
    # Drop unnecessary columns if they exist
    columns_to_drop = ['AdvertisingPlatform', 'AdvertisingTool']
    df = df.drop(columns=[col for col in columns_to_drop if col in df.columns])
    
    return df

def perform_clustering(df, n_clusters=31):
    """Perform clustering on customer data."""
    # Select clustering features
    cluster_features = [
        "Income", "ClickThroughRate", "TimeOnSite", 
        "SocialShares", "EmailClicks", "PreviousPurchases"
    ]
    
    # Ensure all features exist in the dataframe
    available_features = [col for col in cluster_features if col in df.columns]
    
    # Use available features for clustering
    data_cluster = df[available_features]
    
    # Scale the data
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data_cluster)
    
    # Perform clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    cluster_labels = kmeans.fit_predict(data_scaled)
    
    # Calculate cluster metrics
    cluster_metrics = pd.DataFrame()
    cluster_metrics['cluster'] = range(n_clusters)
    
    for var in available_features:
        cluster_metrics[f'avg_{var}'] = [
            data_cluster[cluster_labels == i][var].mean() 
            for i in range(n_clusters)
        ]
    
    return cluster_labels, cluster_metrics, data_scaled, scaler

def create_cluster_radar_chart(cluster_metrics, cluster_num):
    """Create a radar chart for a specific cluster."""
    # Get metrics for the cluster
    metrics = cluster_metrics.drop('cluster', axis=1)
    
    # Normalize the metrics
    normalized_metrics = (metrics - metrics.min()) / (metrics.max() - metrics.min())
    
    # Create the radar chart
    categories = [col.replace('avg_', '') for col in metrics.columns]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=normalized_metrics.iloc[cluster_num].values,
        theta=categories,
        fill='toself',
        name=f'Cluster {cluster_num}'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        showlegend=True,
        title=f'Perfil del Cluster {cluster_num}'
    )
    
    return fig

def calculate_campaign_metrics(df, cluster_assignments):
    """Calculate campaign performance metrics by cluster."""
    metrics = pd.DataFrame()
    metrics['cluster'] = range(len(df['cluster'].unique()))
    
    # Calculate metrics per cluster
    for i in metrics['cluster']:
        cluster_data = df[df['cluster'] == i]
        metrics.loc[metrics['cluster'] == i, 'conversion_rate'] = cluster_data['Conversion'].mean()
        metrics.loc[metrics['cluster'] == i, 'avg_adspend'] = cluster_data['AdSpend'].mean()
        metrics.loc[metrics['cluster'] == i, 'size'] = len(cluster_data)
    
    return metrics

def update_campaign_assignments(df, cluster_labels, campaign_type_assignments, channel_assignments):
    """Update campaign type and channel assignments based on cluster."""
    df_mod = df.copy()
    
    # Reset all campaign type and channel columns
    campaign_types = ['Awareness', 'Consideration', 'Conversion', 'Retention']
    channels = ['Email', 'PPC', 'Referral', 'SEO', 'Social Media']
    
    for c_type in campaign_types:
        df_mod[f'CampaignType_{c_type}'] = 0
    
    for channel in channels:
        df_mod[f'CampaignChannel_{channel}'] = 0
    
    # Update assignments based on cluster
    for cluster, c_type in campaign_type_assignments.items():
        mask = df_mod['cluster'] == cluster
        df_mod.loc[mask, f'CampaignType_{c_type}'] = 1
    
    for cluster, channel in channel_assignments.items():
        mask = df_mod['cluster'] == cluster
        df_mod.loc[mask, f'CampaignChannel_{channel}'] = 1
    
    return df_mod

def adjust_adspend(df_original, df_modified, budget_assignments, channel_budgets=None):
    """Adjust AdSpend based on new campaign type and channel assignments."""
    df_mod = df_modified.copy()
    
    # Calculate total budget
    total_budget = df_original['AdSpend'].sum()
    
    # Adjust budget by cluster
    for cluster, budget_pct in budget_assignments.items():
        mask = df_mod['cluster'] == int(cluster)
        cluster_size = mask.sum()
        if cluster_size > 0:
            cluster_budget = total_budget * budget_pct
            budget_per_customer = cluster_budget / cluster_size
            df_mod.loc[mask, 'AdSpend'] = budget_per_customer
    
    return df_mod 

def create_campaign_analysis_charts(df):
    """Create the four main campaign analysis charts."""
    # 1. CampaignChannel vs Conversion
    channel_conversion_data = []
    for channel in [col for col in df.columns if col.startswith('CampaignChannel_')]:
        channel_name = channel.replace('CampaignChannel_', '')
        channel_data = df[df[channel] == 1]
        channel_conversion_data.extend([
            {'Channel': channel_name, 'Conversion': 0, 'Count': len(channel_data) - channel_data['Conversion'].sum()},
            {'Channel': channel_name, 'Conversion': 1, 'Count': channel_data['Conversion'].sum()}
        ])
    
    channel_df = pd.DataFrame(channel_conversion_data)
    fig1 = px.bar(
        channel_df,
        x='Channel',
        y='Count',
        color='Conversion',
        title='Relación Canal y Conversión',
        barmode='group',
        labels={'Count': 'Frecuencia', 'Channel': 'Canal'}
    )
    fig1.update_layout(showlegend=True, xaxis_tickangle=45)

    # 2. CampaignType vs Conversion
    type_conversion_data = []
    for c_type in [col for col in df.columns if col.startswith('CampaignType_')]:
        type_name = c_type.replace('CampaignType_', '')
        type_data = df[df[c_type] == 1]
        type_conversion_data.extend([
            {'Type': type_name, 'Conversion': 0, 'Count': len(type_data) - type_data['Conversion'].sum()},
            {'Type': type_name, 'Conversion': 1, 'Count': type_data['Conversion'].sum()}
        ])
    
    type_df = pd.DataFrame(type_conversion_data)
    fig2 = px.bar(
        type_df,
        x='Type',
        y='Count',
        color='Conversion',
        title='Relación Tipo de Campaña y Conversión',
        barmode='group',
        labels={'Count': 'Frecuencia', 'Type': 'Tipo de Campaña'}
    )
    fig2.update_layout(showlegend=True, xaxis_tickangle=45)

    # 3. CampaignChannel vs AdSpend
    fig3 = go.Figure()
    for channel in [col for col in df.columns if col.startswith('CampaignChannel_')]:
        channel_data = df[df[channel] == 1]['AdSpend']
        fig3.add_trace(go.Box(y=channel_data, name=channel.replace('CampaignChannel_', '')))
    fig3.update_layout(
        title='Relación Canal y AdSpend',
        yaxis_title='AdSpend',
        showlegend=False,
        xaxis_tickangle=45
    )

    # 4. CampaignType vs AdSpend
    fig4 = go.Figure()
    for campaign_type in [col for col in df.columns if col.startswith('CampaignType_')]:
        type_data = df[df[campaign_type] == 1]['AdSpend']
        fig4.add_trace(go.Box(y=type_data, name=campaign_type.replace('CampaignType_', '')))
    fig4.update_layout(
        title='Relación Tipo de Campaña y AdSpend',
        yaxis_title='AdSpend',
        showlegend=False,
        xaxis_tickangle=45
    )

    return fig1, fig2, fig3, fig4

def calculate_conversion_metrics(df):
    """Calculate detailed conversion metrics for campaigns and channels."""
    metrics = {
        'campaign_types': {},
        'channels': {}
    }
    
    # Campaign Type metrics
    for col in [col for col in df.columns if col.startswith('CampaignType_')]:
        campaign_data = df[df[col] == 1]
        campaign_name = col.replace('CampaignType_', '')
        metrics['campaign_types'][campaign_name] = {
            'total_customers': len(campaign_data),
            'conversions': campaign_data['Conversion'].sum(),
            'conversion_rate': campaign_data['Conversion'].mean(),
            'total_spend': campaign_data['AdSpend'].sum(),
            'avg_spend': campaign_data['AdSpend'].mean(),
            'cost_per_conversion': campaign_data['AdSpend'].sum() / campaign_data['Conversion'].sum() if campaign_data['Conversion'].sum() > 0 else 0
        }
    
    # Channel metrics
    for col in [col for col in df.columns if col.startswith('CampaignChannel_')]:
        channel_data = df[df[col] == 1]
        channel_name = col.replace('CampaignChannel_', '')
        metrics['channels'][channel_name] = {
            'total_customers': len(channel_data),
            'conversions': channel_data['Conversion'].sum(),
            'conversion_rate': channel_data['Conversion'].mean(),
            'total_spend': channel_data['AdSpend'].sum(),
            'avg_spend': channel_data['AdSpend'].mean(),
            'cost_per_conversion': channel_data['AdSpend'].sum() / channel_data['Conversion'].sum() if channel_data['Conversion'].sum() > 0 else 0
        }
    
    return metrics

def adjust_adspend_automatically(df_original, df_modified, cluster_assignments):
    """Automatically adjust AdSpend based on cluster performance and size."""
    df_mod = df_modified.copy()
    total_budget = df_original['AdSpend'].sum()
    
    # Calculate cluster performance metrics
    cluster_metrics = {}
    for cluster in range(31):
        cluster_data = df_original[df_original['cluster'] == cluster]
        if len(cluster_data) > 0:
            conversion_rate = cluster_data['Conversion'].mean()
            size = len(cluster_data)
            cluster_metrics[cluster] = {
                'conversion_rate': conversion_rate,
                'size': size,
                'performance_score': conversion_rate * size
            }
    
    # Calculate budget allocation based on performance score
    total_score = sum(metrics['performance_score'] for metrics in cluster_metrics.values())
    for cluster, metrics in cluster_metrics.items():
        budget_share = metrics['performance_score'] / total_score if total_score > 0 else 1/len(cluster_metrics)
        cluster_budget = total_budget * budget_share
        
        # Assign budget to customers in cluster
        mask = df_mod['cluster'] == cluster
        customers_in_cluster = mask.sum()
        if customers_in_cluster > 0:
            df_mod.loc[mask, 'AdSpend'] = cluster_budget / customers_in_cluster
    
    return df_mod 

def get_original_cluster_assignments(df):
    """Get the original campaign type and channel assignments for each cluster."""
    cluster_assignments = []
    
    for cluster in range(31):
        cluster_data = df[df['cluster'] == cluster]
        
        # Get most common campaign type
        campaign_types = [col for col in df.columns if col.startswith('CampaignType_')]
        campaign_type_counts = cluster_data[campaign_types].sum()
        most_common_type = campaign_type_counts.idxmax().replace('CampaignType_', '')
        
        # Get most common channel
        channels = [col for col in df.columns if col.startswith('CampaignChannel_')]
        channel_counts = cluster_data[channels].sum()
        most_common_channel = channel_counts.idxmax().replace('CampaignChannel_', '')
        
        cluster_assignments.append({
            'Cluster': cluster,
            'Tipo de Campaña': most_common_type,
            'Canal': most_common_channel
        })
    
    return pd.DataFrame(cluster_assignments) 

def create_adspend_distribution_charts(df_original, df_modified):
    """Create box plots comparing AdSpend distribution between original and modified campaigns."""
    # Channel AdSpend box plot
    fig1 = go.Figure()
    channels = ['Email', 'PPC', 'Referral', 'SEO', 'Social Media']
    
    for channel in channels:
        # Original data
        channel_data_orig = df_original[df_original[f'CampaignChannel_{channel}'] == 1]['AdSpend']
        fig1.add_trace(go.Box(
            y=channel_data_orig,
            name=channel,
            boxpoints=False,
            offsetgroup='Original',
            legendgroup='Original'
        ))
        # Modified data
        channel_data_mod = df_modified[df_modified[f'CampaignChannel_{channel}'] == 1]['AdSpend']
        fig1.add_trace(go.Box(
            y=channel_data_mod,
            name=channel,
            boxpoints=False,
            offsetgroup='Optimizado',
            legendgroup='Optimizado'
        ))
    
    fig1.update_layout(
        title="Relación Canal y AdSpend",
        yaxis_title="AdSpend",
        boxmode='group',
        xaxis_tickangle=45,
        template="plotly_dark",
        showlegend=False,
        height=500
    )
    
    # Campaign Type AdSpend box plot
    fig2 = go.Figure()
    campaign_types = ['Awareness', 'Consideration', 'Conversion', 'Retention']
    
    for c_type in campaign_types:
        # Original data
        type_data_orig = df_original[df_original[f'CampaignType_{c_type}'] == 1]['AdSpend']
        fig2.add_trace(go.Box(
            y=type_data_orig,
            name=c_type,
            boxpoints=False,
            offsetgroup='Original',
            legendgroup='Original'
        ))
        # Modified data
        type_data_mod = df_modified[df_modified[f'CampaignType_{c_type}'] == 1]['AdSpend']
        fig2.add_trace(go.Box(
            y=type_data_mod,
            name=c_type,
            boxpoints=False,
            offsetgroup='Optimizado',
            legendgroup='Optimizado'
        ))
    
    fig2.update_layout(
        title="Relación Tipo de Campaña y AdSpend",
        yaxis_title="AdSpend",
        boxmode='group',
        xaxis_tickangle=45,
        template="plotly_dark",
        showlegend=False,
        height=500
    )
    
    return fig1, fig2 