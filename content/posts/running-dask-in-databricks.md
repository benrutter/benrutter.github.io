---
title: Running Dask in Databricks
description: How to run dask workers on the databricks platform
date: 2023-11-02
draft: false
---

I should probably admit that there's a bit of a contradiction between two thoughts that I have:
- I really love spark
- I really hate spark

Spark is one of the most powerful dataframe libraries on the planet. It can process multiple petabytes of data. But it's also overkill and unwieldy for most jobs.

For smaller datasets, tools like [Polars](https://pola.rs) or [Duckdb](https://duckdb.org) or pretty awesome - but for teams that *sometimes* deal with big datasets (but mostly don't) they pose a problem. Namely, do you:
- Do everything in a tool that's overkill
- Do everything with the most optimal tool for the job, but maintain multiple tools and rewrite pipelines when the data grows too big

This is exactly why I love [Dask](https://dask.org). [Pandas](https://pandas.pydata.org) is already the most popular dataframe library for dataframes in Python, and has a huge ecosystem of compatible libraries. Dask-dataframe is built on top of pandas soi that code can keep the same api but scale much bigger. And Dask as a whole is a really nicely written scheduler that'll let you distribute any python code.

Anyway, all this is just a long way of saying, when I read [this github question about running dask on a databricks cluster](https://github.com/dask/dask/discussions/9877) (which is for the most part, a managed spark service) it sent me down a rabbit hole.

This [article from medium looked like a promissing start](https://medium.com/behindthewires/dask-on-azure-databricks-37b5a1537595), and *it really was*, but it's very old and involves using databricks conda setup, which isn't available anymore.

Here's a run through of how to get dask running on databricks in 2023.

## The init script

Databricks offers "init scripts" as a central way for customing cluster behaviour. These scripts will run on any databricks machines (workers or drivers) so are a great tool for stuff like making sure specific versions or requirements are available throughout a cluster.

Here's the init script to get dask running:

```bash
pip install "dask[complete]"

if [[ $DB_IS_DRIVER = "TRUE" ]]; then
  dask scheduler &
  sleep 100
else
  sleep 100
  dask worker tcp://$DB_DRIVER_IP:8786 &
fi
```

It's not particularly complicated but lets run through it step by step:

```bash
pip install "dask[complete]"
```
First we're installing dask on every cluster, so far so good

```bash
if [[ $DB_IS_DRIVER = "TRUE" ]]; then
  dask scheduler &
```
Then, if we're on a driver node ($DB_IS_DRIVER is an environment variable available during initialisation) we'll start dask with ```dask scheduler``` in the background (```&```) since otherwise the script would never exit and we wouldn't get to use our cluster.

```bash
else
   sleep 80
   dask worker tcp://$DB_DRIVER_IP:8786 &
```

If it's not the driver node, we'll start a dask worker listening to the driver node. We sleep for 80 seconds first, just to make absolutely sure that the driver is up and running before the workers. There's a similar sleep for the dask driver, which is to halt execution of notebooks until the driver and workers are likely to be up and running.

## The Notebook

This bit is a lot simpler, since it's just a dummy example.

We set up a client using the local spark IP on the port we used earlier:

```python
from dask.distributed import Client
import os

client = Client(f'{os.environ["SPARK_LOCAL_IP"]}:8786')

def inc(x):
    return x + 1

x = client.submit(inc, 10)
```

If we print out x, we'll see it's completed - yay, we have a nice distributed dask cluster running on databricks!


## Disclaimer

This might not be the best solution depending on your needs. Databricks comes with a bunch of additional tooling which means a heavy (i.e. slow/expensive) footprint for just running dask. If you're *never going to use spark* you might be better off either managing a kubernetes instance, or just getting a *dask as a service* offering a la [coiled](https://coiled.io).


## Edit: Update

This experiment, along with a lot of extra work from much smarter people, winded its way into an actual supported libary. This is a good guide if you're interested in what that library is doing under the hood (although it has some much improved tweaks, like waiting for response calls rather than just sleeping for 80 seconds) but if you actually want to run dask in databricks, just add this to your init.sh:

```bash
/databricks/python/bin/pip install --upgrade dask[complete] dask-databricks
dask databricks run
```

You'll also have access to dask's monitoring dashboard amongst other handy utils, check out the project over at [dask-contrib/dask-databricks](https://github.com/dask-contrib/dask-databricks)

