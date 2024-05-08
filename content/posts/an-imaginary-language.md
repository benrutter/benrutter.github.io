---
title: An Imaginary Language
date: 2024-05-08
---

I don't know where abouts we sit on the wave of yaml-domain-specific-languages. I *really hope* it's the peak, and that things will simmer down. I like yaml a lot as a configuration language, but every time I was to work in a domain specific language pretending to be configuration, it sends chills down my spine.

A big part of it is that github actions and other similar yaml DSLs don't have much tooling, the only way to run and test anything is committing. So I know that in 20 minutes my commit history will look something like this:

- updates to cicd process
- changing way that git head is treated in yaml
- woops, I think it should be like this?
- nope, changing by to the initial
- updating environment variables
- maybe this will work?
- ok what about this?o

That's just one problem though, I also miss having programming language nice-ities. I've been working with azure bicep recently, which does have loops, but the functionality around stuff like this is so hamstrung compared to actual programming languages, that I always end up using jinja to template things out and build the dsl-configuration-hybrid using *python + jinja + the-dsl-itself*. This is a bit of a hassle, and I have an imaginary language that would solve it.

I'm going to call it domain-specific-language-language or DSLL from here on out.

First off, DSLL is basically just *Lua* or something similar (I'm prioritising something that's *embeddable* and *familiar here*), except it operates in two modes:

- DSL definition mode
- DSL mode

## Definition mode

Ok, so in this mode, we're basically just talking about *Lua*, you can import, define functions etc.

Let's say our `main.lua` looks like this:

```lua
local mod = require "mod"

function do_cool_stuff(x)
  if x > 2 then
    mod.thing_one()
  else
    mod.thing_two()
  end
end
```

So far, pretty much just lua.

## DSL Mode

The definition mode has now "created" our DSL. When someone is running within our DSL, their code will pick up from the end of the `main.lua` code. With some extra restrictions:
- No I/O primitives are exposed (aside from `print`). I/O is only possible using functions passed in to engage via a table.
- Importing is no longer possible

This means, all the handy programming features of Lua are there, but that there isn't a given security risk of exposing access to filesystems, networking etc.

We couldn't do much from the `main.lua` context, other than something like this:

```lua
do_cool_stuff(4)
do_cool_stuff(2)
```

But it would be really useful to have something like this with functions for `deploy_model` or `run_test_suite`.

Even better, it would make it *reeeaally* easy to develop a bespoke and tailored DSL for a use case, without the standard problem that you have to choose between:
  - Writing a whole language (introducing a learning barrier for your tool)
  - Using something like json, yaml, toml for a purpose it wasn't designed for.

Anyways, that's it - I think that would be a seriously handy tool to exist, but I probably won't end up building it. Who knows, maybe you will? Even better, maybe it already exists somewhere, and my research skills are just bad. I hope so.
