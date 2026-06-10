import plotly.graph_objects as go
import plotly.express as px

def get_wellness_radar_chart(results):
    """Creates a radar chart showing wellness balance across categories."""
    categories = []
    scores = []
    
    for key, data in results.items():
        if data:
            categories.append(key.replace("_", " ").title())
            scores.append(data.get("score", 0))
            
    if not categories:
        return None

    # Close the polygon
    categories.append(categories[0])
    scores.append(scores[0])

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=scores,
        theta=categories,
        fill='toself',
        line=dict(color='#00BFA6'),
        fillcolor='rgba(0, 191, 166, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100]),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        margin=dict(l=40, r=40, t=20, b=20)
    )
    return fig


def get_score_gauge(score, title):
    """Creates a gauge chart for a specific score."""
    color = "#00BFA6" if score >= 70 else "#FFB347" if score >= 40 else "#FF6584"
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        title = {'text': title, 'font': {'color': 'white', 'size': 18}},
        gauge = {
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': color},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 40], 'color': 'rgba(255, 101, 132, 0.2)'},
                {'range': [40, 70], 'color': 'rgba(255, 179, 71, 0.2)'},
                {'range': [70, 100], 'color': 'rgba(0, 191, 166, 0.2)'}
            ]
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=250,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig
