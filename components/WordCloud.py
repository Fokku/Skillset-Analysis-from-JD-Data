from wordcloud import WordCloud as WC
import base64
from io import BytesIO
from dash import html

def WordCloud(data, Title="Most In-Demand Skills", id="skills-wordcloud"):
    # Generate word cloud
    wc = WC(width=800, height=400, background_color='white').generate_from_frequencies(data)
    
    # Convert to image
    img = wc.to_image()
    
    # Save image to a buffer
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    
    # Encode the image to base64 string
    img_str = base64.b64encode(buffer.getvalue()).decode()

    return html.Div(
        className="col-span-2 p-4 transition-shadow border rounded-lg shadow-sm hover:shadow-lg",
        children=[
            html.H1(
                className="text-xl text-center font-semibold text-slate-800",
                children=Title,
            ),
            html.Img(
                id=id,
                src=f"data:image/png;base64,{img_str}",
                className="w-full h-auto",
            ),
        ],
    )
