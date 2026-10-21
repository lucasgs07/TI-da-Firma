import reflex as rx

config = rx.Config(
    app_name="TI_da_Firma",
    env_file=".env",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
        rx.plugins.RadixThemesPlugin(theme=rx.theme(appearance="light", accent_color="green", radius="medium")),
    ]
)
