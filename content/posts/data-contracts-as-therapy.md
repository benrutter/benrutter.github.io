---
title: Data Contracts as Therapy
description: 
date: 2025-01-27
draft: false
---

I think I've heard people say [data is the new gold](https://youtube.com/watch?v=FvG41iEXFrU) at least twenty times. Having worked in data for a while, I'm pretty sure what they mean by that is that extracting and processing is a laborious and often violent process.

It's possible that my take is inspired by working as a data engineer, and therefore being the victim of other people's data continuously. I once, during my first few weeks at work, came in to find that multiple pipelines had failed because a huge data provider had suddenly replaced a bunch of values with "field-7". Worst off, it wasn't obvious that that's what had happened, because the error was happening further down the line when it was being processed.

There's a constant tension in data-related software development, between **exploratory work** like data-science, where we want *dynamic*, *loosely-typed* libraries, that will let us ingest data and start exploring quicky; and **process-oriented work** where we really want everything to be *strict*, *static* and nailed down so that it doesn't run off and start causing fires.

This is exactly why I came to love. . . 

## Data Contracts! (yay!!)

The idea of a data contract is you have a document, that describes the data, as loosely or strictly as you want, and you can then test data against this document.

I've been working on a project called *Wimsey* recently and here's what a data contract looks like:

```yaml
- test: columns_should
  have:
    - rating
    - predicted_rating
    - category
- test: type_should
  column: category
  be: string
- test: min_should
  column: rating
  be_less_than_or_equal_to: 0
- test: max_should
  column: rating
  be_less_than_or_equal_to: 10
- test: average_difference_from_other_column_should
  column: rating
  other_column: predicted_rating
  be_less_than: 4
```

I want to propose thinking about writing data contracts as a kind of therapy we can engage in. You can start generating one right away (my examples use Wimsey, but I'd recommend Great Expectations or Soda too) like this using a pre-existing dataset (my example uses local storage, but I'd recommend in real life, setting up some kind of object storage just for data contracts and similar things):

```python
from the_scary_outside_world import some_dataframe
from wimsey.profile import starter_tests_from_sampling

save_starter_tests_from_sampling(
    path="my-first-test.yaml",
    df=some_dataframe,
    samples=10_000,
    fraction=0.05,
    margin=3,
)
```

This will generate new tests, straight off the bat, based on building up a sample from your dataset. Ahhh, don't things just feel safer already?

What I love about data contracts is not just having a type-signature (i.e. what columns should be there, should they be integers or floats etc) but also that we can express *boundaries of what normal data looks like*. A lot of data failures are things like, a column which is normally only 2% null values, suddenly being 90% null values. This isn't a problem of asserting that a column isn't *nullable* it's more a vibe of "it's not *that* nullable". 

Similary, in the above example, we were able to express that predicted_ratings shouldn't be *more that 4 different* on average from ratings, otherwise something is going badly in the predicted data we're recieving.

With data contracts, next time we recieve data, we can check it before we do anything else:

```python
from the_not_so_scary_anymore_outside_world import df
from wimsey import validate

df = (df
  .pipe(validate, "my-first-test.yaml")
  .groupby(["category"])
  .max()
)
```

Meaning we can now code as if that contract is a *guarantee* because we know that anytime is fails, our run time will throw a clear, descriptive error.

Finally, one of the *very best* bits, it's that it throws us into a virtuous test cycle, where:

- We have a test for data
- Something goes wrong still
- We update our test to catch it next time
- Repeat

Which means, next time we receive "field-7" instead of sensible integers, we can replace the rage we feel, with the satisfaction of knowing that our fix is making the world (ok, well maybe just our codebase) a safer place. Phew!
