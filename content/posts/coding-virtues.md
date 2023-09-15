---
title: Coding Virtues
description: Thinking about code quality in ways beyond simply 'good' or 'bad'
date: 2023-09-01
draft: false
---

I have a pretty unusual and specific guilty pleasure. Well actually I have an entire music taste based on that premise. More specifically though, I have one that relates to programming: *clean coding*.

By that, I don't mean that all my code is spotless or beautiful or anything, but some part of my brain really enjoys reading about clean code. I have a neat bookshelf of books on programming, with a healthy dose of books like **Uncle Bob's Clean Code**, **Fowler's Refactoring** and plenty more 90s joys that promised me they where going to solve all the problems I make for myself when writing programs. Actually, if I'm honest, I think it's less about my own code, and more about fodder for when I don't like something. Saying "I don't like this" is rarely accepted, and never helpful, but somewhere along the way "this is a code smell" has become cannon.

I think clean code is a pretty important feature, but I still see my relationship to it as essentially a guilty pleasure, something like the programming version of *virtue signaling*. Ultimately, for me it comes down to the fact that once you've read about the general principles of clean code early on in your programming career, reading about it again is basically just confirming your existing beliefs. My experience tells me code is almost always either reasonable, or completely horrible, and there isn't that much in between. While a bunch of people could maybe do with googling clean code, few need to "brush up" on clean coding.

Which makes me end up asking myself, *why does it feel so good to talk about clean code?*. I don't think I'm alone - I've witnessed a lot of times when pull requests have been bogged down in style comments, and bikeshedding on style seems to be a pretty commonly reported phenomenon. I think the temptation is that style is *easy*, understanding performance and correctness of code can be challenging, and often involves a lot of work up front to understand what the code is trying to do and how it achieves it. Good style comments are based around this, but most style comments (like "this variable name is bad and should be longer", "this function name is bad and should be shorter") require only a cursory glance at the code to make.

I've noticed murmurs recently around [clean code being less important than performant code](https://www.youtube.com/watch?v=tD5NrevFtbU) and while that linked video is great, it's easy for this just to become another opportunity for bikeshedding.

That's why I'm introducing my ultra-trademarked-propriety-copyrighted-pay-me-£10-each-time-you-say-it trio of coding virtues! I think that rather "this is bad" / "this is good", we should focus on these three qualities. Code is nice, when it is:
- Expressive: it's easy to understand what's going on and reason about the code
- Performant: the code runs faster on average
- Maintainable: it's easier to make changes to the codebase, and avoiding breakages over time

This isn't some kind of holy trinity and there's plenty of other good qualities code can have, but these correspond nicely to the three things that we do with code: reading, running and editing.

Rather than go into some kind of diatribe about the necessary and sufficient conditions for each, I think it's more helpful just to look at some quick examples where we have a choice to trade one off for the other.

## Performance VS Expressiveness

This is probably the most common trade off because performance often introduces complexity, which almost always affects codes readability negatively. Take the following python code:

```python
from typing import Any, Optional

def get_biggest_7_value_key(
    some_dict: dict[Any: float],
) -> Optional[Any]:
    """
    Return the corresponding key, for the largest
    divisible by seven value in a dict
    """
    divisible_by_seven_dict = {k: v for k, v in some_dict.items() if v % 7 == 0}
    if len(divisible_by_seven_dict) == 0:
        return None
    max_value = max(divisible_by_seven_dict.values())
    max_key = [k for k, v in some_dict.items() if v == max_value][0]
    return max_key
```

This is a pretty silly example, hopefully its clear enough what its doing - its looking only at a dictionaries keys, finding the *largest one that's divisible by 7* and then returning the corresponding key.

For example, here:
```python
x: str = get_biggest_7_value_key({"a": 4, "b": 14, "c": 7, "d": 100})
```
the variable x will equal "b", the corresponding key to 14.

Granted, its not clear why we would want to run this code once, but lets say we want to run it a *lot* of times, on some randomly generated, but similar dictionaries:

```python
import random
import time

def example_dict() -> dict[str: float]:
    return {
        k: random.choice([1.0, 7.0, 21.0, 48.0])
        for k in ["a", "b", "c", "d"]
    } | {"e": 7.0}

start = time.perf_counter()
for _ in range(10_000_000):
    some_dict: dict = example_dict()
    get_biggest_7_value_key(some_dict)
end = time.perf_counter()

print(f"Total time taken: {end-start:0.4f} sec")
```

Running on my hardware, that took 30.7597 seconds but your mileage may vary.

Save we want to optimise things, the obvious thing to do here is cache the function values. But we can't since a dictionary isn't a hashable object type. We could easily do something like this though:

```python
from typing import FrozenSet, Tuple
from functools import cache

@cache
def get_biggest_7_value_key(
    set_representation: FrozenSet[Tuple[str, float]],
) -> float:
    """
    Return the corresponding key, for the largest
    divisible by seven value in a dict

    Takes a set of key, value tuples, generated from a dictionary
    """
    divisible_by_seven_set = (i for i in set_representation if i[1] % 7 == 0)
    max_pair = max(divisible_by_seven_set, key=lambda x: x[1])
    return max_pair[0]
```

Now lets run it a bunch of times again:
```python
start = time.perf_counter()
for _ in range(10_000_000):
    some_dict: dict = example_dict()
    get_biggest_7_value_key(frozen_set(some_dict.items()))
end = time.perf_counter()
```

It now takes 24.0632 seconds on my machine - which is faster than before, all that caching paid off, yay! But its undeniably more confusing to read - the function takes a frozen set as its sole argument, but we don't really care about a frozen set at all, we care about some dictionary, but then have to find a different representation so that it will cache, and yada-yada. Code can be a little like a joke sometimes, if you have to offer an explanation, well, it isn't good.

If we are in a context where we care about performance, then this additional confusion is worthwhile, but what if we're only going to pass a single dictionary into this function? Probably it isn't worth it.

One example is more expressive, and one example is more performant, but neither is *better*, they're just two trade-offs we can make.


## Expressiveness vs Maintainability

I think 'maintainability' might not be the most obvious virtue since editing code *also involves reading it*, so it seems like expressiveness and maintainability should be the same thing. But we don't have to look hard to find an example where they are at odds:

```javascript
const makeEven = n => {
    if (n % 2 == 0) {
        return n;
    }
    return n + 1;
}
```

or consider this:

```javascript
var isEven = require('is-even');

const makeEven = n => {
    if (isEven(n)) {
        return n
    }
    return n + 1
}
```

Ok, ok, I get it. These are both perfectly readable and fine, nobodies mind is gonna be blown in either case. But the first one we obviously have to do some brain-work, we're doing some modulo arithmetic, why? Oh right, of course. The second is much more expressive, we're explicitly saying what we're doing, *checking n is even*. This is a toy example, but we can imagine a more sizable logger head with something like, initial checking credit card number validity for example.

In the second example, we get more readability, but we also have to bring in an additional dependency, that needs to be managed from this point on - there's a bunch of practical questions around, can it be relied on, might the api change, etc, etc. If it sounds silly, just think back as far as left pad, where a bunch of organisations had issues with code because a tiny, very similar to *is-even* library was taken down.

For something as simple as *isEven* that I'll go out on a limb and say you probably don't need to introduce a new dependency. But I don't think it's clear where the line is for something like, prime numbers, email validation etc. Those are all judgement calls based on the reliability of a library, and the size and lifespan of the codebase you're introducing dependencies into.


## Don't be a jerk in Pull Requests


Think about these three qualities as a balance - have you thought about *all* of these issues when reviewing or writing code, or just *some*? And never, never, *never*, ***pleeeease never*** write simply "this code would be better. . . " in a review. Even if its true, it probably isn't going to be well received, and definitely isn't a way to lead to a constructive discussion.

Thinking of code quality in terms of describable metrics like expressiveness, maintainability and performance makes for a meaningful conversation about what code is *trying to achieve* and how it could *better do that*. They also cash out in more meaningful ways than "better", "worse", "clean" etc.
