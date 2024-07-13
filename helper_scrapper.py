from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

async def run_playwright(site):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await setup_browser_page(browser, site)
        content = await extract_content(page)
        await browser.close()
    return content

async def setup_browser_page(browser, site):
    """Set up the browser page by navigating to the site."""
    page = await browser.new_page()
    await page.goto(site)
    return page

async def extract_content(page):
    """Extract and clean text content from the webpage."""
    page_source = await page.content()
    text_content = parse_and_clean_html(page_source)
    return text_content

def parse_and_clean_html(html):
    """Remove script/style, get the text, and clean up the lines."""
    soup = BeautifulSoup(html, "html.parser")
    remove_scripts_and_styles(soup)
    text = soup.get_text()
    clean_text = clean_up_text(text)
    return clean_text

def remove_scripts_and_styles(soup):
    """Remove all script and style elements."""
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

def clean_up_text(text):
    """Clean up text by removing extra spaces and blank lines."""
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    clean_text = '\n'.join(chunk for chunk in chunks if chunk)
    return clean_text

# Usage:
# output = await run_playwright("https://example.com")
