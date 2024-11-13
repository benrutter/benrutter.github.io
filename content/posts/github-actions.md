---
title: Fun & Torture with Github Actions
description: How I learned to stop worrying and stop using github actions
date: 2024-11-13
draft: false
---

I've been working hard on a new project called [*Wimsey*](https://benrutter.github.io/wimsey) lately. I'll save writing about the project itself for another day, but it got me thinking about github actions (or really *any* CICD workflow tool). And crucially, how my process for setting up a new CICD flow always winds up being:

1. Write a nice clean yaml config
2. Feel like everything is very neat and tidy
3. Push to a branch and try running it
4. It doesn't work
5. Ammend, thinking I've fixed it, commit and push
6. It still doesn't work
7. Repeat steps 5 & 6 at least 10 more times
8. Swear a bit
7. Repeat steps 5 & 6 at least 14 more times
9. Cry in front of my friends and colleagues
10. Repeat steps 5 & 6 at least 7 more times
11. It now works! Praise the lords of github actions
12. Vow never to touch it again

Setting up the CICD for Wimsey was no different, only this time somewhere between steps 6 and 11 I found a new step where I thought about the issues with this workflow, which I'm now converting into this blog.


## Nothing is fine and everything hurts

Ok, so why does CICD seem to always fall into this mental pit? For the most part, I like to think that I'm *at least ok* as a developer, but I ***definitely do not feel this way*** when I am writing github actions. I think the crux of the issue is that, normally, there's a certain feedback loop I can follow with development where I'm writing code, testing code, and committing/pushing when I'm happy with how things are working. All this goes out the window with github actions because *the only way to test something is to commit and push*. On top of all that, it's made worse by the fact that, I'm rarely in my confort zone with CICD - I'm not usually writing Python or code I can reason about, instead I'm writing yaml configs for actions that I've *probably never used before* and will *probably never edit again* after this initial first pass.

So, I've landed on a semi-fix, which will probably not solve the problem entirely, but it'll *at least* reduce the number of "maybe this?" commit messages that I push.


## How I Learned to Stop Worrying and Stop Using Github Actions

Initially, I was using a prebuilt github action to build our mkdocs, and then publish them. I pushed *a lot* of commit messages trying to get it to work, and while I was cursing that "this shouldn't be so hard, doing it locally is just a case of running 'mkdocs gh-deploy'" I realised that I could effectively do *exactly that*.

Put simply, if you *already know* how to do something locally, why use a github action? Either put the command straight into github actions as a shell command, or right a simple shell script that you can run. I took my endless tinkering with a prebuilt action, and effectively made it into this:

```yaml
run: |
  python -m mkdocs gh-deploy
```

In other, more complex cases before I've done something like this:
```yaml
run: |
  python path/to/my/release/script.py
```

(I'm using python here, but go/bash/lisp/pick-your-scripting-lang could work too!)

This is probably obvious to a lot of people already, but to me learning that *I don't have to use prebuilt github actions* has been a game changer. `path/to/my/release/script.py` is crucially something that can be *ran and tested locally*. That means if it breaks, you can test it, reason about it, heck even *debug it!*.

There's obviously a limit to this philosophy, you'll still need to make sure the action installs libraries correctly, has the right permissions, yada yada, and if you're doing something github action specific like publishing or consuming an artifact, then you're out of luck, and back to crying in front of your friends and colleagues. But honestly, whenever you can, *just run scripts from CI/CD* and thank me next time it only takes 15 commits to get that action working ok!
