from typing import List, Tuple
from urllib.parse import urlparse

import nltk
import spacy
from metaphor_python import DocumentContent, Result
from nltk.corpus import stopwords, wordnet
from nltk.corpus.reader.wordnet import WordNetError
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize

nltk.download("wordnet")
nltk.download("punkt")
nltk.download("stopwords")

nlp = spacy.load("en_core_web_sm")


def extract_product_name_from_url(url: str) -> str:
    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    domain_parts = domain.split(".")

    if len(domain_parts) >= 1:
        return domain_parts[0]
    else:
        return ""


def count_product_mentions(content: str, product_name: str) -> int:
    return content.lower().count(product_name.lower())


def extract_useful_products(content: str) -> List[str]:
    products = []

    doc = nlp(content)

    for ent in doc.ents:
        if ent.label_ == "PRODUCT" or ent.label_ == "ORG":
            products.append(ent.text)

    return products


def extract_keywords(content: str) -> List[str]:
    words = word_tokenize(content.lower())

    stop_words = set(stopwords.words("english"))
    filtered_words = [word for word in words if word not in stop_words]

    word_freq = FreqDist(filtered_words)

    keywords = [word for word, freq in word_freq.most_common(5)]

    return keywords


def word_similarity(word1: str, word2: str) -> float:
    if not word1 or not word2:
        return 0.0

    try:
        synset1 = wordnet.synset(word1 + ".n.01")
        synset2 = wordnet.synset(word2 + ".n.01")

        similarity = synset1.wup_similarity(synset2)
        return similarity if similarity is not None else 0.0
    except WordNetError:
        return 0.0


def check_similarity(keywords: List[str], url: str, author: str) -> bool:
    url_words = extract_product_name_from_url(url).lower().split()

    if author:
        author_words = author.lower().split()
    else:
        author_words = []

    for keyword in keywords:
        for url_word in url_words:
            similarity = word_similarity(keyword, url_word)
            if similarity >= 0.8:
                return True

        for author_word in author_words:
            similarity = word_similarity(keyword, author_word)
            if similarity >= 0.8:
                return True

    return False


def filter_data(
    results: List[Result],
    contents: List[DocumentContent],
    mention_threshold: int = 5,
    num_extracts: int = 5,
) -> Tuple[List[Result], List[str], List[str]]:
    filtered_results = []
    all_useful_products = set()
    useful_links = []

    content_map = {content.id: content.extract for content in contents}

    for result in results:
        if len(filtered_results) >= num_extracts:
            break

        potential_product_name = extract_product_name_from_url(result.url)
        potential_product_mentions = 0

        extract = content_map.get(result.id, "")

        if potential_product_name:
            potential_product_mentions = count_product_mentions(
                extract, potential_product_name
            )

        keywords = extract_keywords(extract)

        if potential_product_mentions < mention_threshold and not check_similarity(
            keywords, result.url, result.author
        ):
            useful_products = extract_useful_products(extract)

            filtered_results.append(result)
            all_useful_products.update(useful_products)
            useful_links.append(result.url)

    return filtered_results, list(all_useful_products), useful_links
