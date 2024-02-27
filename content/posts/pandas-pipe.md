---
title: Empty Objects & Pandas' Pipe Method
description: Learning design patterns by example
data: 2024-02-22
draft: false
---

The other day, I listened to the episode of [Richard Feldmans's *Softward Unscripted* with Greg Wilson](https://pod.link/1602572955/episode/7de37354dfa00eb3308e523467f410aa). It's a brilliant episode (in fact, the every episode is brilliant so you should probably check it out instead of reading this) and Greg has a lot of great insights around how we teach and discuss software engineering.

One thing that really got me thinking was when Greg pointed out that we are *pretty bad* at talking about design patterns and **really bad** at talking about design patterns with examples.

I thought it would be fun to look at some actual road-tested open source code, and talk about design patterns. One of the simplest examples I can think of that I learnt a lot from is the pandas framework's use of *empty objects* to provide an object style API while avoiding some of the downsides.

I think its pretty easy to discuss, especially because if we take the *.pipe* method, there's actually very little code to unpick.

## Ok, but what is .pipe?

Yeah good question header! We probably can't explain the pattern without first knowing what the function is implementing.

Pandas is a library that provides a central `DataFrame` object, which if you haven't used it before, is basically a table like you might make in Microsoft's excel or something similar. You can carry out operations on columns which is very useful for data science, engineering and analysis.

There are *a lot* of ways you can manipulate pandas DataFrame's, but one that's quite popular [for reasons I won't talk about now, but have written about before](https://benrutter.github.io/posts/restricted-pandas/) is method chaining, which is the practice of carry out all your operations on pandas DataFrames as method calls:

```python
some_df: DataFrame = (
    pd.read_csv("cool_data.csv")
    .astype({"column_a": float, "column_b": int})
    .assign(column_c=lambda df: df.column_a + df.column_b)
)
```

This isn't the only way to manipulate pandas dataframes, and a consequence of that, is that there are some limits. Say we want to do something slightly more involved, like timesing every column by 7 say.

There probably *is* a way to do this using chaining, but doing it without is the most obvious:

```python
for col in some_df.columns:
    some_df[col] = some_df[col] * 7
```

And pandas' `.pipe` method, gives us a nice way to keep things in a method chain:

```python
def times_stuff_by_seven(df: pd.DataFrame) -> pd.DataFrame:
    copy_df = df.copy()
    for col in copy_df.columns:
      copy_df[col] = copy_df[col] * 7
    return copy_df

some_df: pd.DataFrame = (
    pd.read_csv("cool_data.csv")
    .astype({"column_a": float, "column_b": int})
    .assign(column_c=lambda df: df.column_a + df.column_b)
    .pipe(times_stuff_by_seven)
)
```

So basically, `.pipe` is a nice escape hatch for us, when we want some more complex functionality within the method chain.


## Ok, so what's your point?

Yeah, all that's just background for the actual interesting part, which is that when you look at the code for `DataFrame.pipe` you'll see this (this is the actual code, except I've stripped out docstrings and all the other methods):

```python
class NDFrame(PandasObject, indexing.IndexingMixin):
    @final
    @doc(klass=_shared_doc_kwargs["klass"])
    def pipe(
        self,
        func: Callable[..., T] | tuple[Callable[..., T], str],
        *args,
        **kwargs,
    ) -> T:
        if using_copy_on_write():
            return common.pipe(self.copy(deep=None), func, *args, **kwargs)
        return common.pipe(self, func, *args, **kwargs)

```

You'll notice that this doesn't actually include any implementation code, which is exactly what I love about this! Objects, like pandas' `DataFrame` (essentially the `NDFrame` we're seing here) can be helpful in building out nice APIs for end users to act on datastructures. There are definitely other ways of building APIs, but especially for working with Python, objects have some nice advantages:
- Function chaining isn't supported by Python as per (although you can use something like monads to make it possible) but method chaining is
- In the reply, Python has a nice `dir(some_object)` function, that'll tell you all the methods and variables an object has.
- If you're building a data structure with some set ways of interacting, objects let you put "everything in one place" without requiring the user to know where they have to import individual functions from.

But objects can also have some annoying downsides for development, most specifically, that they're big huge balls of state. Every time you have an object you have to start thinking about what state its in, how it has initialised, what its inheriting from, what that's inheriting from. This can make them pretty unwieldy when they get as big as something like the pandas `DataFrame`.

## The "empty object" design pattern

What's happening here, is that the pandas project is keeping the "nice api" part of the `DataFrame` object, but electing to implement almost all the functionality with functions, which are *a lot* smaller in scope, state and much easier to test or reason about.

Here's what the Pandas `pipe` function looks like (again, actual pandas code but I've stripped out docstrings):

```python
def pipe(
    obj, func: Callable[..., T] | tuple[Callable[..., T], str], *args, **kwargs
) -> T:
    if isinstance(func, tuple):
        func, target = func
        if target in kwargs:
            msg = f"{target} is both the pipe target and a keyword argument"
            raise ValueError(msg)
        kwargs[target] = obj
        return func(*args, **kwargs)
    else:
        return func(obj, *args, **kwargs)
```

This is *really easy* to reason about, basically, `obj` is either a tuple or its not. If its not, then:
```python
return func(obj, *args, **kwargs)
```
We just call the given function on the object, along with any arguments and keyword arguments passed in.

Otherwise things are, only a bit, more complicated:
```python
func, target = func
if target in kwargs:
    msg = f"{target} is both the pipe target and a keyword argument"
    raise ValueError(msg)
kwargs[target] = obj
return func(*args, **kwargs)
```

We unpack the tuple into the first and second part, which are meant to be the function, and the keyword that the object should be associated with. Then we use that information to update our keyword arguments (the `kwargs` variable) and just call:
```python
return func(*args, **kwargs)
```

There's not a lot going on here, which is exactly the point. By offloading the method into a function call, we can massively reduce what we need to keep in our heads at a given time. We don't need to think about any of the object variables a `DataFrame` has, just that its an object getting called by a function, and we can immediately tell this from looking at the `pipe` function.

There's an increase in boiler plate code, for sure, but for a large codebase like pandas, that has a lot of people with very different levels of expertise working on it at a given time, the payback in maintainability and testability is easily worth it.

So, if you have a library or module build around a single datastructure, and its growing unwieldy, remember *pandas and the empty object pattern*.




*ps. I made up the "empty object pattern" term because I couldn't find this pattern documented anywhere (there are things like interfaces, but these tend to be **a lot** more object oriented) - if you know its actual name, please do reach out and let me know!*
