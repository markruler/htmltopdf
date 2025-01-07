from libs.pdf import content_to_pdf


async def get_pdf_from_content(
        html: str,
        css: str,
        orientation: str
):
    return await content_to_pdf(
        html=html,
        css=css,
        orientation=orientation,
    )
