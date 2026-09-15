from warcio.archiveiterator import ArchiveIterator
from bs4 import BeautifulSoup
import csv


pages = []


# Open the WARC file
with open("books-clean.warc.gz", "rb") as stream:

    for record in ArchiveIterator(stream):

        # Only process HTTP response records
        if record.rec_type != "response":
            continue

        # Get information from WARC
        url = record.rec_headers.get_header("WARC-Target-URI")
        status = record.http_headers.get_statuscode()
        content_type = record.http_headers.get_header("Content-Type")

        # Only process HTML pages
        if not content_type or "text/html" not in content_type:
            continue

        # Ignore category pages
        if "/catalogue/category/" in url:
            continue

        # Only process pages inside /catalogue/
        if "/catalogue/" not in url:
            continue

        # Read the HTML content
        html = record.content_stream().read().decode(
            "utf-8",
            errors="ignore"
        )

        # Parse HTML
        soup = BeautifulSoup(html, "html.parser")

        # Get page title
        if soup.title:
            page_title = soup.title.get_text(strip=True)
        else:
            page_title = "No title"

        # Find price
        price_element = soup.select_one(".price_color")

        # Find availability
        availability_element = soup.select_one(".availability")

        # Only keep pages that contain both price and availability
        if not price_element or not availability_element:
            continue

        price = price_element.get_text(strip=True)

        availability = availability_element.get_text(
            " ",
            strip=True
        )

        # Save the page
        pages.append({
            "page_title": page_title,
            "price": price,
            "availability": availability,
            "status": status,
            "url": url
        })


# Save the extracted data to CSV
with open(
    "clean-books-results.csv",
    "w",
    newline="",
    encoding="utf-8-sig"
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "page_title",
            "price",
            "availability",
            "status",
            "url"
        ]
    )

    writer.writeheader()

    writer.writerows(pages)


# Print summary
print("=" * 70)
print("CLEAN BOOK PAGES")
print("=" * 70)

print("Book pages found:", len(pages))

print("\nFirst 10 book pages:")
print("-" * 70)

for page in pages[:10]:

    print("Page title:", page["page_title"])
    print("Price:", page["price"])
    print("Availability:", page["availability"])
    print("Status:", page["status"])
    print("URL:", page["url"])
    print()

print("=" * 70)
print("Results saved to: books-results.csv")
print("=" * 70)
 
