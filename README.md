# tech_summarization [WIP]

Abstractive summarization of man pages and technical documentation to generate TLDR pages.

### Usage:

#### To create the data set:

```bash
$ export PYTHONPATH=$(pwd)
$ python src/generate_data.py
```

#### To host the app:

```bash
$ docker build -t tech_summarization .
$ docker-compose up
```