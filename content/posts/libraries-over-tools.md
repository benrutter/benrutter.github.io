---
title: Libraries over tools
description: Why libraries lead to composable architectures
date: 2024-08-20
draft: false
---

Especially in the dark realm of data engineering, there's a huge range of neat low-code/no-code UI tools. I don't want to complain about those today, but I *do want* to talk about why libraries (as opposed to low-code UI) are really awesome.

## Low code is good code!

One thing that I think get's missed out, is that low-code can *still be code*. Plotly and dash is a really nice example of this. Here's the code to make a bar chart:

```python
px.bar(pandas_df, x="category", y="some_value")
```

That really isn't a lot of code (it's probably less code than the amount of excel or dax formulas you'd need if you used Excel or Power BI). But *because* it's code, you can do all sorts of cool stuff with it that you otherwise couldn't:

```python
if day_of_week == "monday":
   px.bar(dynamic_dataset(), x="category", y="some_value")
```

This is kinda pretend code, but my point is it's pretty easy to add something like this into a code-written dashboard, and now we have a dynamic section of the report. All just using if statements and function calls - which you can use with *any other library too*!

Even better, you can roll up connection *into* functions, so if you have a specific use case nobodies built for, you can still have very simple code if you get the abstractions right!

```python
if day_of_week == "monday":
    report = build_out_report(for="diego")
    email_with_friendly_message(report, to="myboss@megacorp.com")
```


## Run on anything

Let's take another *low-code-but-still-code* library that's gaining some attention lately (for good reason) - dlt. Here's a sample pipeline:

```python
pipeline = dlt.pipeline(
    pipeline_name='chess_pipeline',
    destination='duckdb',
    dataset_name='player_data'
)
```

We don't have to worry too much about what it's doing right now, but it's a data pipeline just like you might have in Airbyte or Azure Data Factory (two GUI tool equivalents).

With those tools (or other low-code GUI tools) where you can run it, depends a little on decisions someones already made (maybe you can self-host, maybe no, scaling is kinda plan dependent if not).

With libraries, you can run them on anything, like, *actually anything*. You can test your code locally on your laptop, run it in serverless functions on the cheap, or put it on some gigantic 240GB RAM machine in a server room. It's just code, so you really can choose wherever you want to run it.


## Unit testing

Oh boy, this is a really big one! But you can *actually* unit test stuff, annnnd you can package all your uses into a single module if it works, and have your unit testing run together. That also means you can right a single really nice release process that doesn't terrify new people in your team but lets not get ahead of ourselves!

Unit testing is suuuch a great crutch! Especially if your new to a project, knowing you haven't borked everything entirely with your latest change is the exact kind of peace of mind that lets people iterate really fast.


## Conclusion

Libraries are awesome because they let you:

- Abstract things up to simple code
- Pick your own compute
- Have tests!
