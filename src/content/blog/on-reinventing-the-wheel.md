# On Reinventing The Wheel

Good news if you work in software - impress your friends and colleagues with these magnificent sentences!

- "Have we thought about scalability?"
- "Let's stop and think about what problem we're actually trying to solve"
- "We don't need to reinvent the wheel"

You can say these at any point, in any meeting, without considering context and people will nod in agreement, and think you're very clever. It's not without good reason: scalability is normally important (though probably not quite as much as people think); it's never a bad idea to refocus your thoughts and make sure haven't lost sight of the task at hand; and if reinventing the wheel was a good idea, then step one of every project would involve writing the linux kernel.

In fact, "don't reinvent the wheel" is maybe special, in that it's sort of the whole point of writing software. Let's think about hello world in javascript:

```javascript
console.log("hello world!")
```

First off the bat, you only need to write this once, and not *every single time you want to print out hello world* - that's pretty nice, especially if you want to do something a lot of times. You only have to come up with a method for doing something, and that can be repeated again and again. Even better, when you write this, you don't even have to come up with a method for most of the stuff that's actually happening, like:

- How strings are encoded into data
- What a console is, and actually *how* to write to it
- The interpretting of javascript code
- etc, etc

You can probably imagine that if we had to write all these component parts then very little would ever get done. But I actually want to make the case that **reinventing the wheel is totally awesome and you should definitely do it!** Here's why:


## Reinventing the wheel makes you consider the design of things you take for granted

There's a great blog post called [I am my only user](https://blubsblog.bearblog.dev/i-am-the-only-user/) which talks about building your own tools. That's a great idea for lots of reasons, but actually, some of the things I've learnt the most from are tools I've made that *I wouldn't even [dogfood](https://en.wikipedia.org/wiki/Eating_your_own_dog_food) to myself*. To give an example, I wanted to experiment with what an ideal interactive shell would look like, so I [wrote one that extends python called clamshell](). There's lots of reasons why this is a bad idea, here's a few:
- There are already a gazzilion interactive shells in the world
- There is already an interactive shell in python that's very good
- There are lots of shells you can copy lines of code for (eg) installation into. It's unlikely that most software is going to start writing ready-to-use-code for my bespoke shell script.

But I learnt a whole bunch out of doing this exercise - taking things back to first principles made me realise a bunch of usability features that I actually wanted out of an interactive shell. For instance:

- It's kinda annoying that the default way to remove things "rm" just straight up burns whatever file you had out of all existence
- It's also unnecessary that when moving directories with "cd" you have to know exactly where you're going "i.e. cd ../../Documents/some-folder/sub-folder" when it's really quick to parse the non-hidden folders in a user directory.
- Posix shell more or less is string-only-input-and-output, which is probably one of the reasons it's been so easy to plug programs together in unix historically, but also seems lacking by today's standards.

After implementing this in my home-brewed shell script, and then deciding not to use it, I found ways to alter the behaviour of "rm" to move things to my OS' recycle bin and introduce a handy "jump" function in my .zshrc file (where you can "jump sub-folder" and "cd" to the first match for "subfolder" that fdfind runs into). I don't have a solution for 3 yet, other than that I think passing json between shell scripts would solve this, although the fact I've never seen it done makes me wonder if it's a terrible idea for some reason I haven't bumped into yet.

Implementing these things isn't particularly difficult, but neither are things I would have thought to do if I hadn't undertaken the task of writing an interactive shell. I'd been using bash/zsh/fish more or less every day of my life for about 5 years at the point I started writing clamshell, and had never considered these things, and I probably would have gone another 5 years without thinking about them if I hadn't reinvented the wheel.


## Reinventing the wheel is a great way to learn new things

I'm currently working on a **super-secret-project** (tm) that involves writing an esoteric programming language and a bespoke interpretter. I won't go into details here, but it's probably fair to say that my contributions to the world of code interpretation aren't going to be taught in Computer Science classes of the future.

But I'm also learning a huge amount about code, and the way it runs. You don't get a lot of opportunities to learn about and practically develop these kind of things *unless you specifically reinvent the wheel*. There are only *three major operating systems* (sorry BSD) and *two major compiler toolchains** (GCC & LLVM). That's not a whole lot of real work to go around, but a lot of people would benefit from / enjoy learning about compilation and OS'. [Serenity OS](https://serenityos.org/) probably isn't going to be running in offices any time soon, but that doesn't stop lots of people from learning huge amounts, and creating something awesome in the meantime.

In fact, it's exactly because *code is so good at helping us avoid re-inventing the wheel* that means without doing so, it's easy to program with only a surface level understanding of what's going on under the hood.

Wikipedia lists around [700 programming languages](https://en.wikipedia.org/wiki/List_of_programming_languages), something like [900 historical OS'](https://en.wikipedia.org/wiki/List_of_operating_systems) and cites [almost 27 million profressional programmers](https://en.wikipedia.org/wiki/Software_engineering_demographics), by my logic, there's probably room for a few more wheels in the universe.