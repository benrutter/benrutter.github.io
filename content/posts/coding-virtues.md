---
title: Coding Virtues
description: ...
date: 2023-09-01
draft: true
---

I have a pretty unusual and specific guilty pleasure. Well actually I have an entire music taste based on that premise. More specifically though, I have one that relates to programming: *clean coding*.

By that, I don't mean that all my code is super clean or beautiful or anything, but some part of my brain really enjoys reading about clean code. I have a neat bookshelf of books on programming, with a healthy dose of books like [Uncle Bob's Clean Code](), [Fowler's Refactoring]() and plenty more 90s joys that promised me they where going to solve all the problems I make for myself when writing programs. Actually, if I'm honest, I think it's less about my own code, and more about fodder for when I don't like something. Saying "I don't like this" is rarely accepted, and never helpful, but somewhere along the way "this is a code smell" has become cannon.

I think clean code is a pretty important feature, but I still see my relationship to it as essentially a guilty pleasure, something like the programming version of *virtue signalling*. Ultimately, for me it comes down to the fact that once you've read about the general principles of clean code early on in your programming career, reading about it again is basically just confirming your alread existing beliefs. My experience tells me code is almost always either reasonable, or completely horrible, and there isn't that much in between. While a bunch of people could maybe do with googling clean code, very few need to "brush up" on clean coding.

Which makes me end up asking myself, *why does it feel so good to talk about clean code?*. I don't think I'm alone - I've witnessed a lot of times where pull requests have been bogged down in style comments, and bikeshedding on style seems to be a pretty commonly reported phenomenon. I think the temptation is that style is *easy*, understanding performance and correctness of code can be challenging, and often involves a lot of work up front to understand what the code is trying to do and how it achieves it. Good style comments are based around this, but most style comments (like "this variable name is bad and should be longer", "this function name is bad and should be shorter") require only a cursory glance at the code to make.

I've noticed murmors recently around [clean code being less important than performant code](https://www.youtube.com/watch?v=tD5NrevFtbU) and while that linked video is great, it's easy for this just to become another opportunity for bikeshedding.

That's why I'm introducing my ultra-trademarked-propriety-copyrighted-pay-me-£10-each-time-you-say-it trio of coding virtues! I think that rather "this is bad" / "this is good", we should focus on these three qualities. Code is nice, when it is:
- Expressive: it's easy to understand what's going on and reason about the code
- Performant: the code runs faster on average
- Maintainable: it's easier to make changes to the codebase, and avoiding breakages over time

This isn't some kind of holy trinity and there's no other good qualities code can have.