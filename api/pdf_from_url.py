from libs.pdf import url_to_pdf


def get_pdf_from_url(
        url: str,
        orientation: str
):
    return url_to_pdf(
        url=url,
        orientation=orientation
    )
