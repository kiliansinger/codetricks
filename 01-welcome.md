# Codetricks

These little light tutorials are ment to show important tricks with programming and tools to be efficient in physics. But it also introduces you important skills that are relevant in the current job marked.

## Things to do First

If you have not already done so, download the zip file and unpack it: [codetrick.zip](codetricks.zip)

For all tricks we see here, we need an editor. Install vscode from:
[https://code.visualstudio.com/](https://code.visualstudio.com/)

It works on Linux, Windows and Mac.

If you are lazy with the terminal you could use the Codetour extension. You can install it by opening the extension menue that resembles 4 boxes with one box rotated. Otherwise you should get acquainted with the terminal. Till 2014 there was a nice web page called learn linux the hard way. Fortunately it can be still found on the [web archive](https://web.archive.org/web/20141229230059/https://nixsrv.com/llthw). This is linux specific. But it will also be usefull when working in osx or in windows subsystem for linux on windows platform (which we will use in later parts when setting up programming environments).

![](01-welcome.assets/20251118_054934_image.png)

There search for ```codetour``` and install it. In order to take advantage of this extension you need to open the *.md files with vs-code! This is ideally done, if you open the folder with vs-code by using file/open folder.

## Then

Now we can use The [Codetour](https://marketplace.visualstudio.com/items?itemName=vsls-contrib.codetour) feature to automatically install and give tours that are inserted into the tutorials such that you need to type less. They also detect on which operating system you are. So now you just need to click on  link to automatically install it...

This file is actually Markdown. You might know it from the web.
The first thing we do is, we use the codetour extension to install a good markdown extension that allows us to use life editing of math formulas ($\gamma=\frac{1}{\sqrt{1-v^2/c^2}}$) and linking files and pictures. This is very important if you work in physics labs in research. Unfortunately links are currently broken in that viewer. So you need to CTRL/(OPTION on mac) click the links in the source file.

Just click on this link here to install [Markdown preview enhanced extension](https://marketplace.visualstudio.com/items?itemName=shd101wyy.markdown-preview-enhanced).

Now you can just press CTRL+SHIFT+V to view the preview and CTRL+K then V to see this document in side by side view. Note: On Mac OPTION corresponds to ALT and COMMAND is the CTRL key.

You can also paste images directly into the editor view. But before you should install the paste image extension:
[Markdown extension](https://marketplace.visualstudio.com/items?itemName=telesoho.vscode-markdown-paste-image).
change the setting of that extension as following:
![](01-welcome.assets/20260428115615.png)

Now you can directly paste images with CTRL+ALT+V.

Such that all images are stored relative to your markdown source file in a folder called ``filename.assets``.

## Markdown cheat sheets

If you want to create markdown files yourself here is a cheat sheet. We use markdown all the time in the lab for our electronic labbooks.
[https://github.com/lifeparticle/Markdown-Cheatsheet](https://github.com/lifeparticle/Markdown-Cheatsheet)
