# My Webpage

I know webpages might be a bit oldschool as you might have a social media account.
But it also offers full control. You only decide what is stored and also what you want to show. 

You will also see that it does not have to be a webpage.
It can also be a web-app that behaves like a real app on Linux, Windows, Mac, Android and even IPhone and IPads. True multiplatform without the need to make an expensive developer account.

See for example my calculator that works with SI units.
[SIcalc](https://kiliansinger.github.io/SIcalc/)

The sources are available at
[SIcalc](https://github.com/kiliansinger/SIcalc)
And you can get the sources by typing ``git clone https://github.com/kilianSinger/SIcalc.git``
from the command line.

In general you can host these pages even at your home on e.g. a raspberry pi but step by step. A simple webpage will be enough for now.

Lets make an new account if you do not have it already:
[Signup](https://github.com/signup)

Try to use your university account because this will give you Copilot+ AI guided coding (see later).

install the github command line interface (CLI) by following the tour...

Once you have an account. Lets create a local repository. For detailed description follow the tour link below...µµ
```bash
mkdir mywebpage
cd mywebpage
git init
echo hello >README.md
git add README.md
git commit -m "first commit"
```
Now we have a local git repository. 
Next will create a git repository on https://github.com and synchronize it with our local.
First log in:
```bash
gh auth login
```
then press 5 times return, you should see:
```
? Where do you use GitHub? GitHub.com
? What is your preferred protocol for Git operations on this host? HTTPS
? Authenticate Git with your GitHub credentials? Yes
? How would you like to authenticate GitHub CLI? Login with a web browser

! First copy your one-time code: 9113-2090
Press Enter to open https://github.com/login/device in your browser...
✓ Authentication complete.
- gh config set -h github.com git_protocol https
✓ Configured git protocol
✓ Logged in as kiliansinger
```
now we are logged in and we create a new remote repository (Replace the ACCOUNTNAME with you account name):
```bash
gh repo create --source=. --public --description "my webpage"
git remote add origin https://github.com/ACCOUNTNAME/mywebpage.git   
git push --set-upstream origin main
git remote add origin https://github.com/ACCOUNTNAME/mywebpage.git
```
