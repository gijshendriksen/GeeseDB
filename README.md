# GeeseDB
[![Build Status](https://app.travis-ci.com/informagi/GeeseDB.svg?branch=master)](https://app.travis-ci.com/informagi/GeeseDB)

## Graph Engine for Exploration and Search
GeeseDB is a Python toolkit for solving information retrieval research problems that leverage graphs as data structures. It aims to simplify information retrieval research by allowing researchers to easily formulate graph queries through a graph query language. GeeseDB is built on top of [DuckDB](http://duckdb.org/), an embedded column-store relational database designed for analytical workloads.

GeeseDB is available as an easy to install Python package. In only a few lines of code users can create a first stage retrieval ranking using BM25. Queries read and write Numpy arrays and Pandas dataframes, at zero or negligible data transformation cost (dependent on base datatype). Therefore, results of a first-stage ranker expressed in GeeseDB can be used in various stages in the ranking process, enabling all the power of Python machine learning libraries with minimal overhead. Also, because data representation and processing are strictly separated, GeeseDB forms an ideal basis for reproducible IR research.

## Package Installation
Install latest version of GeeseDB via [PyPI](https://pypi.org/project/geesedb/):

```
pip install geesedb==0.0.2
```

GeeseDB depends on a couple of packages that can also be installed using `pip`. It is also possible to install the development installation of GeeseDB using `pip`:

```
pip install git+https://github.com/informagi/GeeseDB.git
```

If you are planning to contribute to the package it is possible to clone the package, and install it using `pip` in editable version:
```
git clone git@github.com:informagi/GeeseDB.git && cd GeeseDB && pip install -e .
```

You can run our tests to confirm if everything is working as intended (in the repository folder):
```
pytest
```

## How do I index?
The fastest way to load text data into GeeseDB is through CSV files. There should be three csv files: one for terms, one for documents, and one that connects the terms to the documents. Small examples of these files can be found in the repository: [docs.csv](./geesedb/tests/resources/csv/example_docs.csv), [terms_dics.csv](./geesedb/tests/resources/csv/example_term_dict.csv), and [term_doc.csv](./geesedb/tests/resources/csv/example_term_doc.csv).

These can be generated using the CIFF [to_csv](./geesedb/utils/ciff/to_csv.py) class from [CIFF](https://github.com/osirrc/ciff) collections, or you can create them however you like. The documents can be loaded using the following code:

```python3
from geesedb.index import FullTextFromCSV

index = FullTextFromCSV(
    database='/path/to/database',
    docs_file='/path/to/docs.csv',
    term_dict_file='/path/to/term_dict.csv',
    term_doc_file='/path/to/term_doc.csv'
)
index.load_data()
```

## How do I search?
After indexing in the data, it is really easy to construct a first stage ranking using BM25:

```python3
from geesedb.search import Searcher

searcher = Searcher(
    database='/path/to/database', 
    n=10
)
hits = searcher.search_topic('cat')
```

In this case the searcher returns the top 10 documents for the query: `cat`. 

## How can I use SQL with GeeseDB?
GeeseDB is built on top of [DuckDB](http://duckdb.org/), and we inherit all its functionalities. It is possible to directly query the data in GeeseDB using SQL. The following example shows an example on how to use SQL on the data loaded in the example above:

```python3
from geesedb.connection import get_connection

db_path = '/path/to/database/'
cursor = get_connection(db_path)
cursor.execute("SELECT count(*) FROM docs;")
cursor.fetchall()
```

## How can I use Cypher with GeeseDB
GeeseDB also supports a subset of the Cypher graph query language, in particular the following keywords: `MATCH`, `RETURN`, `WHERE`, `AND`, `DISTINCT`, `ORDER BY`, `SKIP`, and `LIMIT`. We plan to support the full Cypher query langauge in the future. In order to use the Cypher query language with GeeseDB, first a metadata file needs to be loaded. 

The metadata represents the graph structure represented in the database, the table name `_meta` is used for this. The metadata is represented as a Python dictionary object with the following structure:
```python
{
    'from_node':
    {
        'to_node':
        {
            [['join_table',
              'from_node_join_key',
              'join_table_from_node_join_key',
              'join_table_to_node_join_key',
              'to_node_join_key'
              ]]
        }
    }
}
```
Using this structure we know which tables in the database related to eachother. If this information is known it is possible to translate Cypher queries to SQL queries. An example of a Cypher query that can be translated to SQL is shown belows:

Cypher:
```cypher
MATCH (d:docs)-[]-(:authors)-[]-(d2:docs)
WHERE d.collection_id = "96ab542e"
RETURN DISTINCT d2.collection_id
```

SQL:
```sql
SELECT DISTINCT d2.collection_id
FROM docs AS d2
JOIN doc_author AS da2 ON (d2.collection_id = da2.doc)
JOIN authors AS a2 ON (da2.author = a2.author)
JOIN doc_author AS da3 ON (a2.author = da3.author)
JOIN docs AS d ON (d.collection_id = da3.doc)
WHERE d.collection_id = '96ab542e'
```

The queries can be translated the following way:

```python
from geesedb.interpreter import Translator

c_query = "cypher query"
translator = Translator('path/to/database')
sql_query = translator.translate(c_query)
```

## Cite
GeeseDB was published at DESIRES: [Read here](https://ceur-ws.org/Vol-2950/paper-11.pdf)

If you use GeeseDB you can cite use using bibtex:
```
@inproceedings{geesedb,
	author    = {Chris Kamphuis and Arjen P. de Vries},
	title     = {{GeeseDB: A Python Graph Engine for Exploration and Search}},
	booktitle = {Proceedings of the 2nd International Conference on Design of Experimental Search \& Information REtrieval Systems},
	pages     = {10-18},
	year      = {2021},
	url       = {http://ceur-ws.org/Vol-2950/paper-11.pdf},
	address   = {Aachen},
	publisher = {CEUR-WS.org},
	series    = {DESIRES '21}
}
```
