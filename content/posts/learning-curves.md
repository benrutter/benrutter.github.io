---
title: Learning Curves
description: The UI conflict between depth and speed to get started
date: 2024-04-19
draft: false
---

People (sadly) don't go around asking me my favourite text editor a lot. But if they did, I'd answer in a second, ("Helix!")[https://helix-editor.com/].

But weirdly, I have worked a bunch in the past with people who are new to coding, and have recomended them editors, I've *never* recommended Helix to someone starting out.

That probably isn't that wierd if you're familar with Helix. If you're not, it's a lot like Vim or Neovim. You edit from the terminal (which I love) and you have different *modes* for writing, reading and selecting (which makes keyboard shortcuts very optimised for each of those). A lot of people have used modal editors, a lot of people love them, and a lot of people can agree that they come with a pretty steep learning curve when you first get started.

That makes modal text editors a really bad recommendation for someone who's new to coding, since they're already learning a bunch of stuff already, you don't really want to give them a whole load of new stuff to learn on top of that. I almost always recommend VS code, because it's quick to get started with but also has a good level of depth and support for advanced features that can make you really productive when you get going with it. But, at least in my experience, it bottoms out quicker than modal editors do - you can get pretty productive with it, but modal editors will take you further.

I think that's interesting because that seems to be a conflict that comes up *a lot* in user interfaces, and there aren't many exceptions where the "best in class" for highest productivity, is also the best for ease of getting started. For example:

**Automatic vs manual cars**: Automatic cars are easier to drive, but there's a reason that F1 drivers don't (at least not yet) use automatic gear changes.

**Dynamic vs static types**: Probably a controversial one, but I think dynamic languages are way easier to get started with (for me at least, by the time I have my first pass Rust code just *compiling*, I could have knocked up a prototype in Python several times over) but they bottom out faster for more complex code bases (dynamic types seem to inherently bring a lot of complex bugs where types are wrong, but don't error until they've been passed around several times - these are alot worse for larger codebases)

**MS Paint vs Photoshop**: I actually don't know how to use photoshop, but I can use all the features of MS Paint to make low rate digital sketches. Photoshop takes a lot of learning to get started with, but there's a reason it gets used to design magazine covers, and MS Paint doesn't.

**API design**: Plotly vs Matplotlib is a good example of this. Ploty is much easier to put together a visualisation with, but matplotlib can do some *crazy detailed* things that just aren't possible in plotly. Try annotating a 3d subplot within 5 other different plots and you'll see what I mean - actually don't do that, it sounds terrible.


I think about this a lot, especially when it comes to library design. I don't think there's a right or a wrong side to fall on, and there are definitely cases where you can do a good job of somewhat accomodating both (I think VSCode is good for this, it's quick to learn and *does* have good depth, even if not as much as my beloved Helix). But being aware of the tension between ease of learning, and ultimate power of the tool you're building is important. You don't want to start out dreaming of a jet plane, and find out you've build a scooter, and you don't want to build a childrens toy that involves learning assembly to get started with (1980s, I'm looking at you).
