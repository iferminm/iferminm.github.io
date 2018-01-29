Title: What to do when linux freezes?
Subtitle: don't press the shutdown button
Author: Israel Fermín Montilla
Date: 2017-12-24
Tags: linux
Cover: https://dl.dropboxusercontent.com/s/nofhzatwj098ntz/measure.jpg
Thumbnail: https://dl.dropboxusercontent.com/s/nofhzatwj098ntz/measure.jpg


Well, we all know that nothing is perfect, not even linux, it sometimes freezes.
It has happened to me several times,
my solution? well, press and hold the power button and hope for the best. 

Well, I was thinking *there must be a better way to do it* and, like most of the times, **there is**. 
It's called *SysRq* keys and it's a key combination only understood by the Linux kernel that lets you
perform some low level operations no matter the state of the system, think of it like a safe reset button.

The key combination is *Ctrl + Alt + PrtSc + REISUB*, this means, you need to press and hold *Ctrl + Alt + PrtSc*
and while pressing that combination, you need to write *REISUB*, each letter has one function

* **R** gives the kernel back the control of the keyboard from X
* **E** sends *SIGTERM* to all processes, allowing them to terminate gracefully
* **I** sends *SIGKILL* to all remaining processes, forcing them to terminate right away
* **S** flushes data to disk
* **U** remounts all filesystems in *read-only* mode
* **B** reboot!

That way your system won't suffer any damage and it will gracefully **R**eboot **E**ven
**I**f **S**ystem **U**tterly **B**roken.

If you need to turn off your computer instead of reboot, you
can switch **B** for **O**. You're welcome.
