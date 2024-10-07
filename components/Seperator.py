from dash import html

def Seperator(horizontal=True, className=None):
    return html.Div(
                className="{} self-stretch bg-gradient-to-tr from-transparent via-neutral-500 to-transparent opacity-25 dark:via-neutral color {}".format("w-full h-px min-w-full" if horizontal else "h-full w-px min-h-full", className if className else ""),
                )