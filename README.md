# Web Crawling, WARC & PySpark Pipeline

A practical mini-project demonstrating an end-to-end workflow from web crawling and web archiving to structured data extraction and PySpark processing.

## Project Overview

The goal of this project was to become familiar with:

* Web Crawling
* WARC file format
* Web Scraping
* MapReduce
* Apache Spark
* PySpark

The practical implementation uses **Books to Scrape** as a small test website.

The project demonstrates how raw web content can be collected, archived, extracted, cleaned, and finally processed using PySpark.

---

## Project Pipeline

```text
Books to Scrape
       ↓
   Wget Crawler
       ↓
      WARC
       ↓
 Python + Warcio
       ↓
  BeautifulSoup
       ↓
 Data Cleaning
       ↓
      CSV
       ↓
    PySpark
       ↓
 Data Analysis
```

---

## Technologies Used

| Technology    | Purpose                        |
| ------------- | ------------------------------ |
| Wget          | Web crawling                   |
| WARC          | Web content archiving          |
| Python        | Data extraction and processing |
| Warcio        | Reading WARC files             |
| BeautifulSoup | Parsing HTML                   |
| CSV           | Structured data storage        |
| Apache Spark  | Distributed data processing    |
| PySpark       | Python API for Spark           |

---

# 1. Web Crawling

Web crawling is the automated process of visiting web pages and following links to discover and download web resources.

For this project, **Wget** was used as the crawler.

The crawl started from:

```text
https://books.toscrape.com/
```

The crawl was initially tested with depth 1 and later increased to depth 2.

---

# 2. WARC

WARC (Web ARChive) is a standardized format for storing web resources captured during crawling.

In this project, the crawl generated:

```text
books-clean.warc.gz
```

The WARC file contains captured web responses and metadata such as URLs and HTTP information.

Important distinction:

```text
Crawler → collects
WARC → archives
Scraper → extracts
```

---

# 3. Crawling vs Scraping

These concepts are related but different.

### Crawling

Discovers and downloads web resources.

### WARC

Stores the captured resources in an archive format.

### Scraping

Extracts specific information from the captured HTML.

In this project:

```text
Wget
  ↓
Crawling

WARC
  ↓
Storage / Archive

Python + BeautifulSoup
  ↓
Extraction / Scraping
```

---

# 4. Crawl Depth Experiment

The first experiment used:

```text
--level=1
```

The crawl depth was then increased to:

```text
--level=2
```

This allowed the crawler to reach deeper pages, including individual book pages.

The final crawl used:

```bash
wget --recursive --level=2 --no-parent --warc-file=books-clean https://books.toscrape.com/
```

### Crawl Result

* Downloaded resources: 1,141
* Downloaded size: approximately 19 MB
* WARC file: `books-clean.warc.gz`

The 1,141 downloaded resources do not represent 1,141 books. The crawl also included other resources such as HTML pages, images, and related web files.

---

# 5. Data Extraction

The WARC file was processed using:

* Python
* Warcio
* BeautifulSoup

The extraction process filtered the WARC records to keep relevant HTML book pages.

The extracted fields were:

| Field          | Description              |
| -------------- | ------------------------ |
| `page_title`   | Title of the page        |
| `price`        | Book price               |
| `availability` | Availability information |
| `status`       | HTTP response status     |
| `url`          | Book page URL            |

The final structured dataset contained:

```text
519 actual book pages
```

---

# 6. Data Cleaning

The raw crawl contained different types of pages and resources.

Filtering was applied to remove irrelevant pages such as category pages and keep actual book pages.

Price values initially looked like:

```text
£51.77
```

They were converted into numeric values:

```text
51.77
```

Availability information was also processed to extract the available quantity when present.

The cleaned data was saved as:

```text
clean-books-results.csv
```

---

# 7. Apache Spark & PySpark

Apache Spark is a distributed data processing engine.

PySpark provides a Python API for working with Spark.

PySpark was installed and verified successfully.

Version used:

```text
PySpark 4.2.0
```

The project did not stop at installation. Spark was used to process the actual dataset generated from the WARC crawl.

---

# 8. PySpark Processing

The Spark script performs several operations:

1. Read the CSV dataset.
2. Inspect the DataFrame schema.
3. Count the total number of book pages.
4. Clean price values.
5. Extract availability quantities.
6. Calculate the average book price.
7. Group books by available quantity.
8. Analyze HTTP status codes.

---

# 9. Results

The final PySpark processing produced:

### Total Book Pages

```text
519
```

### Average Book Price

```text
£35.36 approximately
```

### HTTP Status

```text
519 pages → HTTP 200
```

The results demonstrate that the crawled and extracted data could be successfully processed using PySpark.

---

# 10. Challenges & Solutions

## Challenge 1 — Crawl Depth

**Problem:**
Level 1 did not provide sufficient access to the individual book pages needed for analysis.

**Solution:**
The crawl depth was increased from Level 1 to Level 2.

---

## Challenge 2 — Mixed Web Resources

**Problem:**
The WARC contained different types of pages and resources.

**Solution:**
The Python extraction script filtered records based on content type and URL structure.

---

## Challenge 3 — Incorrect Page Selection

**Problem:**
Category pages could contain book information and could therefore be accidentally selected.

**Solution:**
Category pages were explicitly excluded and only relevant catalogue pages containing price and availability information were kept.

---

## Challenge 4 — Price Data Type

**Problem:**
Price values contained the `£` symbol and were initially stored as strings.

**Solution:**
The currency symbol was removed and the values were converted into numeric data using PySpark.

---

## Challenge 5 — Availability Conversion

**Problem:**
Some availability values did not contain an explicit numeric quantity, which caused an integer conversion error.

**Solution:**
The extraction result was validated before converting it to an integer.

---

# 11. Key Takeaways

This project demonstrated an end-to-end data pipeline:

```text
Collect
   ↓
Archive
   ↓
Extract
   ↓
Clean
   ↓
Process
   ↓
Analyze
```

The main lessons were:

* Crawling and scraping are different processes.
* WARC provides a way to archive captured web content.
* Crawl depth affects which pages can be reached.
* Raw web data often requires filtering and cleaning.
* PySpark can be used for real data processing, not only installation and testing.
* Distributed processing concepts such as grouping and aggregation can be demonstrated using Spark.

---

## Conclusion

This project provided practical experience with web crawling, web archiving, data extraction, data cleaning, and Spark-based data processing.

The final workflow transformed raw web content into structured data that could be analyzed using PySpark.
