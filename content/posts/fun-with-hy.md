---
title: Fun with Hy and Pandas
description: Functional data programming with Hy!
date: 2024-10-02
draft: false
---

I don't keep it much of a secret- I *love* functional programming. Or maybe I'm just burned form spending hours of my life chasing back inheritance to see where an object variable was defined. Either was, when I saw that [hy lang](https://hylang.org/) v1.0 was release the other day, I was pretty kean to try it out!

One of the downsides of new or more experimental languages, is the lack of ecosystem while things take time to catch on. That makes languages like Hy or Clojure a way easier sell, since they bring everything you love about Lisps without needing you to give up on the libraries of Python or Java respectively.

I set out to have a play with Hy, and see what it'd look like with Pandas. Getting set up is as simple as `pip install hy` (or `uv add hy` since I was trying out uv at the same time). The first thing I found is that I *reeaally* wanted functions chaining, and that (from what I could see) wasn't supported out the box, meaning I pretty quickly wound up writing something like this:


```clojure
(setv df
  (.head
    (.assign
        (pd.read_csv "cool.csv")
        :c (fn [x] (* x.a 2)))
  2))
(print df)
```

Which, at least for me, melted my brain by line three. So far, not so cool. But hey, this is a lisp, instead of whining can't I just write a macro?

I don't have a lot of experience writing macros, and my early experiments into trying to coax chat gpt into not lying to me about the features of Hy didn't go so well, fortunately, what I wanted to do was pretty simple, and I wound up writing this:


```clojure
(defmacro -> [x #* forms]
   `(do
      (setv _ ~x)
      ~@(map (fn [form] `(setv _ ~form)) forms)
      _))
```

Essentially, this macro will take any number of s-expressions, it'll set the first one to the variable `_`, then run and set the next one to `_` etc etc. The upshot of this, is we can do some nice functional chaining:

```clojure
(setv cool
  (-> (+ 3 4)
      (- _ 3)
      (* _ 4 5)))
```

This obviously isn't very complex code, but I was really happy with how easy to read this makes things, even with very little experience with Hy, it's pretty obvious to see that the variable `cool` is:
- 3 + 4 = 7
- 7 - 3 = 4
- 7 * 4 * 5 = 60

After spending a while feeling smug about the 5 lines of code I'd written so far, I set to work checking out how Hy might work with Pandas, and honestly I was blown away. Everything was way easier than I expected, here's some dummy code:

```clojure
(setv df
  (->  (pd.read_csv "cool.csv")
       (.assign _
         :c (* _.a 2)
         :d (+ _.a 4)
         :e (.astype _.b "string[pyarrow]"))
       (.head _ 2)))
```

And here's a replication of some code from Tom Ausberger's modern pandas:

```clojure
(defn read [fp]
  (-> (pd.read_csv fp)
      (_.rename :columns str.lower)
      (_.drop 'unnamed: 36' :axis 1)
      (_.pipe extract_city_name)
      (_.pipe time_to_datetime ["dep_time" "arr_time" "crs_arr_time" "crs_dep_time"])
      (_.assign
        :fl_date (pd.to_datetime _.fl_date)
        :dest (pd.Categorical _.dest)
        :origin (pd.Categorical _.origin)
        :tail_num (pd.Categorical _.tail_num)
        :unique_carrier (pd.Categorical _.unique_carrier)
        :cancellation_code (pd.Categorical _.cancellation_code))))
```

For completeness and here's the python equivalent (the original code):

```python
def read(fp):
    df = (pd.read_csv(fp)
            .rename(columns=str.lower)
            .drop('unnamed: 36', axis=1)
            .pipe(extract_city_name)
            .pipe(time_to_datetime, ['dep_time', 'arr_time', 'crs_arr_time', 'crs_dep_time'])
            .assign(fl_date=lambda x: pd.to_datetime(x['fl_date']),
                    dest=lambda x: pd.Categorical(x['dest']),
                    origin=lambda x: pd.Categorical(x['origin']),
                    tail_num=lambda x: pd.Categorical(x['tail_num']),
                    unique_carrier=lambda x: pd.Categorical(x['unique_carrier']),
                    cancellation_code=lambda x: pd.Categorical(x['cancellation_code'])))
    return df
```

Honestly, Hy actually brings this code much closer to how I'd like the code to look. It's a lot more terse without sacrificing readability.

I think this demonstrates the niceties of macros pretty well - there are hundreds of language features I wish I could change about python, but practically I can't (renaming `lambda` to `fn` would be pretty high on my list 😂). I can see the pit falls too in fairness, if I *was* allowed to rename `lambda` to `fn` in my python codebases, those kind of changes could add up pretty quickly to an ecosystem where every library has its own dialect.

Either way, I'm stoked to experiment more with the awesome Hy!
