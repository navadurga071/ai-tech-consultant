
import pytest

from app.crawler import crawl


def test_crawl_rejects_zero_pages():
    with pytest.raises(ValueError):
        crawl(max_pages=0)


def test_crawl_rejects_negative_delay():
    with pytest.raises(ValueError):
        crawl(max_pages=1, delay_seconds=-1)
