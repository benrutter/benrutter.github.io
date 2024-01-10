---
title: The Joy of Monads
description: Turns out monads aren't that complicated after all!
date: 2024-01-10
draft: false
---

I love taking some time out in December, but my code obsessed brain often results in me using it to learn about some new coding concepts. This year, I took to reading though Miran Lipovača's awesome [Learn You a Haskell for Great Good!](https://www.learnyouahaskell.com/) which had previously sat on my bookshelf unread for a long time.

Probably one of the main reasons I didn't approach it was that Haskell has a reputation for being a difficult language. I still think that reputation is pretty well earned, but more than anything, mainly because its such a *big* language. There's a lot in Haskell, and it has a pretty complex type system. As a digression, I think this is what makes Rust famously difficult to pick up too. Rust doesn't have very many "gotchas" compared to other languages, but that doesn't stop the fact that there's *a lot of completely new concepts* you'll need to learn in order to pick it up.

One of the things that suprised me most, was from learning the concept of Monads, which I've always assumed where insanely complicated. Turns out, the first sentence of the [wikipedia article on Monads](https://en.wikipedia.org/wiki/Monad_(functional_programming)) is enough:

> a monad is a structure that combines [functions] and wraps their return values in a type with additional computation

That's literally it. In other words, a monad is a design pattern where we abstract away additional work that happens on each function call.

I ended up putting together a [super small library for implementing monads in python](https://github.com/benrutter/monads) as a learning exercise. So lets work the "Result" monad from that as an example!


Take this extremely helpful code:

```python
import requests

def get_age():
    age = input("what is your age?")
    return age

def human_to_dog_years(age):
    response = requests.get("https://animalyrconverter.com/api/v1/humantodog")
    dog_yr_per_human_yr = response.json()[converter]
    return age * dog_yr_per_human_yr
    
def dog_to_cat_years(age):
    response = requests.get("https://animalyrconverter.com/api/v1/dogtocat")
    cat_yr_per_dog_yr = response.json()[converter]
    return age * cat_yr_per_dog_yr

if __name__ == "__main__":
    cat_years = dog_to_cat_years(
        human_to_dog_years(
            int(get_age())
        )
    )
    print(f"you are {cat_years} cat years old!")
```

I'm sure you can see lots of problems with this example that I haven't even notices, but lets just focus on one + a bonus:
- Main problem: we don't have any structured error handling
- Bonus: pythons nested functions are kinda janky to read

Let's ignore the bonus for now, and just implement some basic error handling to guarantee no runtime errors:

```python
if __name__ == "__main__":
    try:
        cat_years = dog_to_cat_years(
            human_to_dog_years(
                int(get_age())
            )
        )
        print(f"you are {cat_years} cat years old!")
    except Exception as error:
        print(f"I don't know how old you are in cat years")
        print(f"This error happend: {error}")
```

Python linters are all screaming right now because of the generic ```except``` not specifying an error, but lets not worry about that since this is just a toy example and instead look at what this looks like using a monad to carry out error handling instead:

```python
from monads.monads import Result

if __name__ == "__main__":
    cat_years = (
        Result(get_age())
        .bind(int)
        .bind(human_to_dog_years)
        .bind(dog_to_cat_years
    )
    if cat_years.value:
        print(f"you are {cat_years} cat years old!")
    else:
        print(f"I don't know how old you are in cat years")
        print(f"This error happend: {cat_years.exception}")

```

or, as a bonus we can use some syntactical sugar and express binds like this (don't worry too much about this part though, it's handy, but isn't needed for understanding monads):

```python
from monads.monads import Result

if __name__ == "__main__":
    cat_years = Result(get_age()) >> int >> human_to_dog_years >> dog_to_cat_years
    if cat_years.value:
        print(f"you are {cat_years} cat years old!")
    else:
        print(f"I don't know how old you are in cat years")
        print(f"This error happend: {cat_years.exception}")

```

The Result monad is basically a class wrapping a value, and giving us "bind" to run a function over it. It has a ```value``` and an ```exception```, one of which is always None.

the ```bind``` definition just looks like this:
```python
def bind(self, func):
    if self.exception:
        return self
    try:
        return Result(func(self.value))
    except Exception as exception:
        return Result(None, exception)
```

Basically we're saying:
- If there's already an error, don't even attempt to do anything
- Otherwise, try to return a new Result with the updated value
- If that fails, return a new Result with the relvant exception

I'm just aiming to explain monads here rather than evangelising them, but some motivations for this approach might be:
- More complicated error handling behaviour is easier since you have an exception variable that isn't within the ```except Exception``` nest
- You can pass the Result monad around different parts of your program easily, which is trickier with try/catch statements

The result handling itself though, is just an example, what makes this a monad is that it is doing the result handling on each function call, so our function calls don't need to worry about the result handling at all.

If that's still a little fuzzy, let's take a look at the ```Maybe``` monad:

```python
import random

from monads.monads import Maybe

def maybe_not():
    return random.choice([7, None])

def double(x):
    return x * 2

def square(x):
    return x ** 2

if __name__ == "__main__":
    result = Maybe(maybe_not()) >> double >> square
    if result.value:
        print(result)
    except:
        print("nope")
```

Here ```Maybe``` handles the possibility that something is None for us. Here's its definition:

```python
class Maybe(Generic[T], Monad):
    def bind(self, func: Callable) -> "Maybe":
        if self.value is None:
            return Maybe(None)
        return Maybe(func(self.value))
```

Basically, if the value is None, we won't do anything, otherwise, we'll return a new Maybe with the executed function.

This means that we don't have to think about the possibility of whether something is ```None``` within our double or square calls, which would otherwise error.

And one more, the ```List``` monad:

```python
from monads.monads import List

def double(x):
    return x * 2

def square(x):
    return x ** 2

if __name__ == "__main__":
    result = List([1, 2, 3]) >> double >> square
    print(result)
```

Here the ```List``` monad abstracts away the complexity of dealing with a List and applies a function to all the members. Otherwise we'd have to change functions like double to be this:
```python
def list_double(x_list):
    return [x * 2 for x in x_list]
```

Hopefully I've convinced you now that monads are just a pretty regular (and helpful) design pattern, and not some kind of dark magic!

To summarise, monads:
- wrap some kind of value
- do a bunch of extra work on function calls to that value

Which means:
- we don't need to repeat logic on those individual function calls
- function definitions don't need to handle additional abstractions or logic

I had a bunch of fun learning about this - hoping to dive into some more functional programming stuff next. Happy new year 🎉
