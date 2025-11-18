# Revision control

Revision control is very useful. Just imagine you write your thesis and suddenly you delete a part without realizing it. You safe it, and then you write more. At some point you realize the problem. With revision control you can track back each of your steps.

And here we use it for updating your codetricks course. But the great part of git is that you can work in teams. It was invented by Linus Thorwald who wrote Linux. We use it in science when we program large simulation programs in teams or sofisticated experimental control systems.

Lets install it, by downloading from [https://git-scm.com/](https://git-scm.com/) or using the code tour (only works in the source code view of vs-code)...

Now all you have to do, is download the repository with ``git clone https://github.com/kiliansinger/codetricks.git`` (only needed if you have not downloaded the zipped [codetrick.zip](codetricks.zip) file and unzipped it) then ``cd codetricks`` and to update it type ``git pull`` from the command line to get updates.
For the lazy ones I have it in the hint...

And now you can see more chapters and also this text was updated.
If you want to learn more about git you can start here: [https://rogerdudler.github.io/git-guide/](https://rogerdudler.github.io/git-guide/)

Have also a look I updated the [01-welcome](./01-welcome.md) with hints where to learn more about Markdown.

At some point while trying to update with ``git pull`` you might get an error message stating that you will overwrite changes that you have performed on your editor.
You can store your changes by using the command ``git stash``. This will save your current changes and allow you to perform a ``git pull`` without losing any of your work.
If you later want to retrieve your changes then type ``git stash apply`` this will update the new documents including your changes.

If you made changes that you would like to all undo then do ``git reset --HARD origin/main``.

So you see ``git`` is a very usefull tool to keep track of changes and to undo changes.

In [04-My Webpage](./04-my_webpage) you will make an account on github and then make a minimal webpage.
