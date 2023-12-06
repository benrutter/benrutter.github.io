---
title: Restricted Pandas
description: Ok here me out on this one, and why you should use less of pandas
date: 2023-12-06
draft: false
---

Bemoaning the design of pandas isn't a very hot take - the success of polars which seems to have kinda rocketed out of nowhere, is probably down, not by a small amount, to just how many people are currently using pandas, but want it to be *faster* (always better right?) and also *more elegant*.

I'm not gonna say to use pandas over polars or vice-versa, but I do think that if you're going to use pandas, joining the cult of method chaining with a reduced feature set makes life a lot easier.

Take this query, which admitedly isn't crazy hard to follow:

```python
def nice_data() -> pd.DataFrame:
    """
    Returns a dataframe with some arbitrary actions carried out on it,
    this logic is all made up for example.
    """
    df = pd.read_csv("nice_data.csv")
    df.rename(columns=str.lower, inplace=True)
    df["total_revenue"] = df[[i for i in df.columns if "revenue" in i]].sum(axis=1)
    df["total_volume"] = df[[i for i in df.columns if "volume" in i]].sum(axis=1)
    df["revenue_per_volume"] = df["total_revenue"] / df["total_volume"]
    df.loc[df["cancelled"] == "YES", "revenue_per_volume"] = 0
    pivot = df.pivot(index="category", values=["revenue_per_volume"], aggfunc="sum")
    return pivot
```

This kind of logic is *basically fine*, it's the sort of pandas I see most often out in the wild. But I really want to convince you that this would be much nicer:

```python
def nice_data() -> pd.DataFrame:
    """
    This is the same logic as before, but using chaining instead
    """
    return (
        pd.read_csv("nice_data.csv")
        .rename(columns=str.lower, inplace=True)
        .pipe(lambda df: df[df["cancelled"] != "YES"])
        .assign(
          total_revenue=lambda df: df[[i for i in df.columns if "revenue" in i]].sum(axis=1),
          total_volume=lambda df: df[[i for i in df.columns if "volume" in i]].sum(axis=1),
          revenue_per_volume=lambda df: (df["total_revenue"] / df["total_volume"]),
        )
        .pivot(index="category", values=["revenue_per_volume"], aggfunc="sum")
    )
```

## Reason One: Linear Process

I think the first reason is probably the most obvious, which is that the chain method forces everything to be processed in a linear method.

For those examples, that might seem artificial, because they're both in reality following the same linear process. But I think there's an important distinction which is that the chain method *guarantees* everything within the indentation block relates to *only* the final output dataframe.

You can read the second one as a kind of story just based on the method calls, without needing to even look at the arguments:
- at the start we're going to *read_csv*
- then *rename* some columns
- then *pipe* the dataframe through a function (ok, this one doesn't work that well)
- then *assign* some custom columns
- and finally *pivot* what we have


You can't do that with the first one, you have to read every line to understand what its doing, what its doing and build a picture in your head for *why* its doing that. That means you have to be smart and attentive, which are both tricky. Whereas method chaining means I can tap into my internal laziness to know what's going on, which is a sure fire win!


## Reason Two: Enemy of The State

Ok, I admit it you thought I was trying to get you to join a pandas cargo-cult, but it turns out there's also a whole functional programming cargo-cult under the hood too!

Some people like objects, some people like functions, but *nooobody* likes state, yuck! It's **always bad**. And method chaining means we don't need any. Take the first example, we created a variable ```df``` that we don't really care about, just so we can pivot it into the ```pivot``` variable later on. Ok, I could have just overwritten ```df``` with the output of pivot, but without chaining, again there's no guarantees of everything. At every step you have to think:
- What variables exist at this point of the process
- What state is being changes

With method chaining, there's one thing being affected, the dataframe being chained. I know you can still use variables within a chain, but there's undoubtably less state to think about or mess up. The pandas "setting with copy" error comes up a lot for beginners, and its often confusing. Chaining just means there's less stuff to keep track of, and only a single output being worked towards per chain.


## Reason Three: Just Less Stuff

So, this is the most important reason for me, and probably the least obvious, but if you've used pandas for a while, you'll know that it is *huuuugge*. There's a lot of stuff you can do, and in a lot of different ways.

Take the rename columns we did earlier, any three of these would do the same thing:

```python
# rename with inplace
df.rename(columns=str.lower, inplace=True)
# rename with variable overriding
df = df.rename(columns=str.lower)
# setting columns directly
df.columns = [i.lower() for i in df.columns]
```

Similary, for overwriting values we have:
```python
# set with loc
df.loc[df["cancelled"] == "YES", "revenue_per_volume"] = 0
# set column directly with numpy where (or mask)
df["revenue_per_volume"] = np.where(df["cancelled"] == "YES", 0, df["revenue_per_volume"])
df["revenue_per_volume"] = df["revenue_per_volume"].mask(df["cancelled"] == "YES", 0)
# just use an apply even though its obviously not necessary
df["revenue_per_volume"] = df.apply(lambda row: row["revenue_per_volume"] if row["cancelled"] != "YES" else 0, axis=1)
# also just do any of those above three options, but using assign instead
df = df.assign(lambda df: df.apply(lambda row: row["revenue_per_volume"] if row["cancelled"] != "YES" else 0, axis=1))
```

Ok, to be there, some of those last few where obviously terrible options, but my point is that pandas has a lot of options, and it isn't always clear, especially if you're new to the library, which are good ones.

This can make a codebase super confusing to newcomers, because there aren't any clear patterns for how to do things.

On the other hand, method chaining is restricted, and opinionated, which are two things pandas can really benefit from. There's normally only one sane way to do things, because you're working with a subset of pandas functionality:
- set columns with assign
- rename columns with rename
- etc

## Reason Four: Debugging

One of the main criticisms I see levied at method chaining, is that it makes debugging harder and you can't just drop "ipdb.set_trace()" in whereever, but honestly, I see it the other way round! The fact that there's less state means debugging is super simple with this trick:


```python
df = (
  pd.read_csv("cool.csv")
  .pipe(lambda df: df[df["col"] == "keep"])
  .pipe(lambda df: (ipdb.set_trace(), df)[1])
  .assign(nice=lambda df: df["a"] + df["b"]
)
```

There you go, step into any point of the chain you like! And even better, because there's no state complexity, it's just a case of adding traces closer and closer to the bug until you find the source.

## Bonus Reason: the joy of Dask

This doesn't apply to a lot of people, but I tend to use a lot of Dask in my work. ```dask.dataframe``` is at its best a drop in replacement for pandas that lets it scale past your computes single core memory. In order to do this, a bunch of super interesting and cool stuff that I won't go into happens, but one important part of this, is that dataframes become lazily evaluated until you call ```.compute()``` on them.

Because of the lazy evaluation, there's a subset of pandas methods and functionality, importantly including things around setting with indexes, that dask can't support. Using method chaining, because it's a restricted subset of pandas functions, means you're already on the right track for an easier swap path if you need it later!
