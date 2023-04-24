# Hi, I'm <mark>Ben</mark> 👋

I'm a data/ML engineer, generative artist, and all round maker of things with code.

Anything I indepently develop is available under either an MIT or GPL open source license and can be found on my github or codeberg repo.

Here are some key projects I've put together:

# House of Left 🎨
## Generative, mostly visual, art systems

I make and share generative art under the moniker *house of left*. I use a range of tools like my own Shades, Processing, p5.js, nannou and Sonic Pi.

I tend to explore simple geometry or color rules - there's some sound pieces, and I have some video stuff in the the works, but for the most part I make static image generators that can be ran to produce different results each time.

You can check out a sample of stuff right here, follow me on (instagram)[https://www.instagram.com/houseofleft/] and (mastodon)[https://graphics.social/@houseofleft], or just check out the (code repos directly)[https://github.com/benrutter/house-of-left].

# Shades 🕶️
## A Python module for 2D generative image creation

Shades is a module for geometric image creation that helps produce colour gradient based artwork. It's built on a paradigm of reusable Shade objects to help create generative 2D images. It simplifies production of generative images, and features an easily hackable abstract base class for expanding upon the code base whenever needed.

Although it makes some sensible choices like vectorised and batched Perlin noise calculations, it's still a Python native library (something I conciously chose so that it could easily be pulled apart and tweaked by the user). This means it isn't exactly a speed demon, so although it works well for sketches, isn't a great choice for complex 3d image generation or animation. For two dimensional artworks, I find it a  really helpful tool, and I use it all the time for artworks, even if later translating them into Processing or Nannou pieces.

Check out the (source code on github)[https://github.com/benrutter/shades] or (download the library through pip)[https://pypi.org/project/shades/]


## Hop 📁
## A terminal based file browser for Linux, Apple and Windows

I use the terminal a lot in my workflow, and having a dedicated file manager tool can be really helpful when deleting, moving or copying several files at once. Projects like Midnight Commander, Ranger and nnn all make this easier on Linux, but can't be used on Windows. I wanted to make an OS-agnostic tool that was simple and easy to get up and running with, so I built Hop, and use it in my workflow to this day.

The (source code is available on github)[https://github.com/benrutter/hop] and (you can download the tool through pip)[https://pypi.org/project/hop-file-browser/]


# Clamshell
## An experimental, python based interative shell

Software development is a field with hundreds of well established and effective tools, sometimes though, you just get the urge to reinvent the wheel. I wanted to experiment with what my dream interative shell might look like, and landing on adapting Python with some additional convenience syntax and functions.

I strongly recommend you *don't* use this as your daily driver, but it works on linux, apple and windows and has some cool features like user friendly syntax, autocompletion, a dynamic "cd" equivalent that you can use to switch into key folders from any location, a fully customisable python based config and an "rm" equivalent that sends stuff into your OS's trash can instead of burning it out of existence entirely.

Check out the (source code)[https://github.com/benrutter/clamshell], read about it on (hacker news)[https://news.ycombinator.com/item?id=34557775], or (road test it yourself)(https://pypi.org/project/clamshell/)


## mpy3 🎵
### An ultra minimal, command line mp3 player

I wanted a simple, no-frills, distraction-free command line mp3 player, and couldn't find one, so put together mpy3. The whole thing has around 50 lines of code, and is written with Typer and Pygame - it plays mp3s with a very, verrryyy minimal feature set (shuffle, skip and nothing else).

Check out the (source code)[https://github.com/benrutter/mpy3] or (download through pip)[https://pypi.org/project/mpy3]


## Rad Waves 🌊 
### An arcade surfing game with original assets

Rad waves is an arcade surfing game. You get points for doing spins and picking up coins, but die if you touch a skull, just like in real life.

It's built with Phaser.js with original assets - I finished it off for Itch's Finally Finish Something 2022 game jam which was a bunch of fun.

Play on (itch)[https://supercoolgames.itch.io/rad-waves] or (see more here)[https://github.com/benrutter/rad-waves]


# Endless Asteroids 
## The arcade classic reworked into an endless runner

Endless Asteroids was a quick, fun project to try out the Phaser.js framework. It's a rework of the arcade classic asteroids, but as an endless runner.

Play on (itch)[https://supercoolgames.itch.io/endless-asteroids] or (see more here)[https://github.com/benrutter/endless-asteroids]


# This Websites Templating Tool 🌍
## You're kinda looking at it now

I think as a rule every developer at some stage makes their own website into a pet project. Hundreds of static site generators already exist, so I figured one more couldn't hurt.

This website uses Python's Jinja2 templating along with classless CSS and file structures to generate itself from only markdown files.
