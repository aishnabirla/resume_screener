import pdfplumber
import re


def extract_text_from_pdf(pdf_file):
    text = ""
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = _extract_page_text(page)
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""
    return clean_text(text)


def _extract_page_text(page):
    """
    Tries multiple extraction strategies in order:
    1. Standard extract_text (works for simple single-column PDFs)
    2. Column-aware extraction (works for two-column resumes like Lakshay's)
    3. Word-level fallback (works for image-heavy or structured PDFs)
    """

    # Strategy 1: Standard extraction
    standard_text = page.extract_text(x_tolerance=3, y_tolerance=3)
    if standard_text and len(standard_text.strip()) > 100:
        return standard_text

    # Strategy 2: Column-aware extraction
    # Split page into left and right halves and extract each separately
    # This handles two-column resume layouts
    try:
        width = page.width
        height = page.height

        left_bbox  = (0,        0, width * 0.48, height)
        right_bbox = (width * 0.48, 0, width,    height)

        left_page  = page.crop(left_bbox)
        right_page = page.crop(right_bbox)

        left_text  = left_page.extract_text(x_tolerance=3, y_tolerance=3) or ""
        right_text = right_page.extract_text(x_tolerance=3, y_tolerance=3) or ""

        combined = (left_text + "\n" + right_text).strip()
        if len(combined) > 80:
            return combined
    except Exception:
        pass

    # Strategy 3: Word-level fallback
    try:
        words = page.extract_words(
            x_tolerance=3,
            y_tolerance=3,
            keep_blank_chars=False
        )
        if words:
            words.sort(key=lambda w: (round(w['top'] / 10), w['x0']))
            lines = {}
            for word in words:
                line_key = round(word['top'] / 10)
                if line_key not in lines:
                    lines[line_key] = []
                lines[line_key].append(word['text'])
            return "\n".join(" ".join(lines[k]) for k in sorted(lines.keys()))
    except Exception:
        pass

    return standard_text or ""
def clean_text(text):
    text = re.sub(r'\(cid:\d+\)', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    text = text.strip()
    return text

def extract_text_from_string(text):
    return clean_text(text)