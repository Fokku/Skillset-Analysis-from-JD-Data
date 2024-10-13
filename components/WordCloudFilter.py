from dash import dcc, html
from wordcloud import WordCloud
import base64
from io import BytesIO
import plotly.graph_objs as go

# Generate a word cloud image
def generate_wordcloud_image(skill_frequencies):
    if not skill_frequencies:
        return None

    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(skill_frequencies)

    # Save word cloud to an image buffer
    img = BytesIO()
    wordcloud.to_image().save(img, format='PNG')
    img.seek(0)

    # Convert to base64 string
    img_base64 = base64.b64encode(img.getvalue()).decode()

    return img_base64

# Return the word cloud layout or a message if no data is available
def WordCloudLayout(skill_frequencies=None, Title="Most Skill needed", id=None):
    # Generate the word cloud image
    wordcloud_image = generate_wordcloud_image(skill_frequencies)

    # If no industries are selected, return a message
    if wordcloud_image is None:
        return html.Div(
            id="wordcloud",
            # className="p-4 transition-shadow border rounded-lg shadow-sm hover:shadow-lg",
            children=[
                html.H1(
                    className="text-xl text-center font-semibold text-slate-800",
                    children="No selected industry.",
                )
            ],
        )

    # If industries are selected, display the word cloud
    trace = go.Image(
        source=f"data:image/png;base64,{wordcloud_image}",
        hoverinfo='skip' 
    )

    layout = go.Layout(
        title=dict(
            text=Title,
            x=0.5,
            xanchor="center"
        ),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        margin=dict(l=0, r=0, t=30, b=0),
    )

    # Return the layout with dcc.Graph instead of html.Img
    return html.Div(
        id="wordcloud",
        # className="p-4 transition-shadow border rounded-lg shadow-sm hover:shadow-lg",
        children=[
            dcc.Graph(
                figure={"data": [trace], "layout": layout},
                config={"displayModeBar": False},
                className="w-full h-[300px]"
            ),
        ],
    )