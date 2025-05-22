---
title: Planning to Fail
description: Some ideas around expressive error messaging
date: 2025-05-16
draft: false
---

I read the hilarious ["Please Please Please" Phorge entry](https://we.phorge.it/book/flavor/article/please_please_please/) today and it's as hilarious as it is trauma inducing.

As somebody who spends a bunch of time working on libraries, I sometimes see feedback like this gem from the aforementioned entry:

```
Subject: help
X-Priority: 1
it dun work
```

There's also the opposite side, where in my head an error stack is super expressive but I see this:

> Subject: Strange Error
> 
> Not sure why but when I call this script:
> ```python
> from amazing_strings import make_uppercase
> 
> make_uppercase(44)
> ```
> 
> I get some kind of confusing error message I don't understand:
> ```
> YouHaveGiven44InsteadOfAStringException:
> You Have give the number 44 as an entry, but you should have passed in
> a string, like "44" or "forty-four"
> 
> ```

This is obvious an exageration, but it feels like this sometimes!

I'm pretty sure though that I have a serious bias towards thinking exception messages I've raised are super clear, and that other people's are terrible.

For instance, here's an error message I saw in the wild just the other day, from pyarrow:
```
    ...
    return self.reader.read_all(column_indices=column_indices,
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "pyarrow\\_parquet.pyx", line 1717, in pyarrow._parquet.ParquetReader.read_all
  File "pyarrow\\error.pxi", line 92, in pyarrow.lib.check_status
OSError: Repetition level histogram size mismatch
```

I've only included the end, but I promise you the rest of it doesn't make any more sense to me either!

The actual issue is that pyarrow v19.0.0 (just that patch verion) has a very specific bug where it can't interpret certain metadata from future arrow implementations.

I'm sure someone somewhere is thinking "Isn't it obvious! Why else would the repetition level histogram size have a mismatch!?" but it might have well been in hyroglyphics to me.

## What's actually broken?

I think the key question is how we can make more expressive errors. One of the things that complications this, is that somebody's code is broken, but we don't necesarily know who's code. This can be messy for users, take this for example:

```python
def roi(gain: float | int, cost: float | int) -> float:
    """Return on investment"""
    return (gain - cost) / cost

roi("seven", "five")  # <- this will throw an error because you're using it wrong
roi(0, 0)  # <- this will throw an error, but maybe I should have handled it?
```

Those two errors are different, especially to new users (probably in more complicated examples than this one), they might not know that ROI isn't built to handle 0 cost projects. Take my pyarrow histogram error, my first thought wasn't "I'll go raise a bug ticket or check one exists", it was "I must have somehow added a wierd data type into this file".

The zero division error doesn't get thrown by our function, so it's not obvious that we (the writers of the function) thought that might happen.

We can help that a *little* by adding in error messages, whenever we see a possibility happenning:

```python
def roi(gain: float | int, cost: float | int) -> float:
    """Return on investment"""
    try:
      return (gain - cost) / cost
    except ZeroDivisionError as error:
      raise ValueError("Zero cost projects are not handled") from error
```

That's more clear - most languages are kind of a nightmare for this though, because we never know where the errors might come from.

Some languages, like Rust, force us to be more explicit, the above example would be:

```rust
fn roi(gain: f64, cost: f64) -> f64 {
    (gain - cost) / cost
}
```

That *can't* throw an error, because rust will return `INFINITY` for that case, if we wanted to throw an error we could use the result type:

```rust
fn roi(gain: f64, cost: f64) -> <f64, &'static str> {
    if cost == 0.0 {
      Err("Zero cost projects are not handled")
    } else {
      Ok((gain - cost) / cost)
    }
}
```

I really like this because now our user *has* to think about the errors they're getting rather than just assuming that things will go well. This massively improves the likely hood of good quality errors (errors thrown by us rather than one of our dependencies).


## Why can't we have nice things?

Ok, so can't we have that in Python? There's plenty of libraries that offer result types, but unless you're designing a business application with users already bought it, suddenly using "Result" types is gonna throw a lot of people off, and not in a good way.

The last 20 years of python development are all based on dynamic typing. This is why we can't have nice things Python! 😭

One,  option would be to do something like this:

```python
from functools import wraps
from typing import Callable

class UnexpectedException(Exception): ...

def raises(*exceptions: type[Exception]) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @wraps(func)
        def wrapped(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if type(e) in exceptions:
                    raise
                msg = (
                    "You've encountered an unexpected exception in the "
                    "programme, please raise a bug with https://bugsite.cool"
                )
                raise UnexpectedException(msg) from e
        return wrapped
    return wrapper


@raises(ZeroDivisionError)
def roi(gain: float | int, cost: float | int) -> float:
    """Return on investment"""
    try:
      return (gain - cost) / cost
    except ZeroDivisionError as error:
      raise ValueError("Zero cost projects are not handled") from error
```

I think this is pretty ideal in *some* ways, because we have a nice error message when we're expecting it, and something pointing people to the fact that unexpected behaviour has been hit when we stray from the happy path. That couldn't go wrong right?

```python
x = roi("seven", "five")

# UnexpectedException: You've encountered an unexpected expection in the programme, please raise a bug with https://bugsite.cool
```

Oh no. . .

Maybe this:
```python
@check_types
@raises(ZeroDivisionError)
def roi(gain: float | int, cost: float | int) -> float:
    """Return on investment"""
    try:
      return (gain - cost) / cost
    except ZeroDivisionError as error:
      raise ValueError("Zero cost projects are not handled") from error
```

Which might mean we get something like this:

```python
x = roi("seven", "five")

# TypeError: You have given str "seven" in place of a float | int type
```

But that'll introduce a big runtime premium, worst still, we're at two wrappers now just for a simple function, it isn't going to be long before:

```python
@check_types
@raises(ZeroDivisionError)
@class_method
@wraps
...  # you get the picture
```

Maybe this is an exageration, maybe it wouldn't happen in reality? The error raises would already be a "TypeError" before the UnexpectedException message. My instict is that maybe there isn't a neat tech-fix for the problem of user design. You can communicate with your users, try to write error messages as clear as possible, you'll probably still get:

```
Subject: help
X-Priority: 1
it dun work
```

And they'll probably still get:

```
    ...
    return self.reader.read_all(column_indices=column_indices,
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "pyarrow\\_parquet.pyx", line 1717, in pyarrow._parquet.ParquetReader.read_all
  File "pyarrow\\error.pxi", line 92, in pyarrow.lib.check_status
OSError: Repetition level histogram size mismatch
```

Maybe we're all to blame. I'll try and bear that in mind next time I respond to an issue.
