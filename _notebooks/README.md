# Auto-convert Jupyter Notebooks and notebook-like py files To Posts

Two options are supported:
1. Notebook files (`.ipynb`)
2. Python files (`.py`) that are convertible to notebooks (via [jupytext](https://github.com/mwouts/jupytext))

You must save your notebook or python file with the naming convention `YYYY-MM-DD-*`.  Examples of valid filenames are:

```shell
2020-01-28-My-First-Post.ipynb
2020-01-28-My-First-Post.py
2012-09-12-how-to-write-a-blog.ipynb
```

If you fail to name your file correctly, `fastpages` will automatically attempt to fix the problem by prepending the last modified date of your notebook. However, it is recommended that you name your files properly yourself for more transparency.

See [Writing Blog Posts With Jupyter](https://github.com/fastai/fastpages#writing-blog-posts-with-jupyter) for more details.