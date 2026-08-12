def style_chart(fig):

    fig.update_layout(

        paper_bgcolor="#151515",

        plot_bgcolor="#151515",

        font=dict(

            family="Inter",

            color="#F8F8F8",

            size=14

        ),

        title=dict(

            font=dict(

                size=22,

                color="white"

            ),

            x=0.02

        ),

        margin=dict(

            l=20,

            r=20,

            t=60,

            b=20

        ),

        legend=dict(

            orientation="h",

            y=1.08,

            x=0

        ),

        transition_duration=500,

        hoverlabel=dict(

            bgcolor="#222",

            font_size=14

        )

    )

    fig.update_xaxes(

        showgrid=False,

        linecolor="#2A2A2A",

        tickfont=dict(

            color="#BDBDBD"

        )

    )

    fig.update_yaxes(

        gridcolor="#2A2A2A",

        linecolor="#2A2A2A",

        tickfont=dict(

            color="#BDBDBD"

        )

    )

    for trace in fig.data:

        if trace.type in ["bar", "scatter", "pie"]:

            trace.marker.line.width = 0

    return fig