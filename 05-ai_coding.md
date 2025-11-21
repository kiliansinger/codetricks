# AI coding

Warning: You need to still be able to program. There was
an incidence where chatgpt was writing a crypto wallet that
stole the money and transfered it to an hacker's account ([https://www.heise.de/news/ChatGPT-Code-mit-betruegerischer-API-kostet-Programmierer-2500-US-Dollar-10169146.html](https://www.heise.de/news/ChatGPT-Code-mit-betruegerischer-API-kostet-Programmierer-2500-US-Dollar-10169146.html)).

Also be aware that approximately in one out of three cases AI models currently just invent wrong facts: https://www.heise.de/hintergrund/KI-und-die-Halluzinationen-Warum-sind-so-viele-Antworten-falsch-10962482.html

Also depending from where the model comes it can output vulnerabilities if your query contains references to taiwan and others. (https://the-decoder.com/deepseek-outputs-weaker-code-on-falun-gong-tibet-and-taiwan-queries/)

But AI coding can really speed up as you will see with our recipie webpage.

As a student of the university you are able to get a free educational account of github copilot.
Apply here: [https://github.com/education](https://github.com/education)

For all others and those that do not want to let the AI read all their code with potential private information, I will show how to run local AI to be nearly as proficient. Follow the code tour (only works in the source code view of vs-code) to install the needed extensions...

In case you go for github copilot you need to install two extensions: [Github Copilot](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot) and [Github Copilot Chat](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat) Use the code tour (only works in the source code view of vs-code)...

Then try yourself to add a recipee to your webpage. And add the functionality to adjust the amount of ingredients dependent on the portions.

The result could look similar to the following code (Ask copilot chat to explain things if you do not understand). I modified the code such that the measures only occur in one place. A good programming paradigm is to avoid multiple places where same values are given.

Result:

```html
<!doctype html>
<html>
  <head>
    <title>My Recipies</title>
      <link rel="stylesheet" href="simple.css">
      <style>
        .inline {
          width: 3em;
        }
      </style >
<script>
  document.addEventListener('DOMContentLoaded', (event) => {
    const portionsInput = document.getElementById("pancake-portions");
    portionsInput.addEventListener('input', (e) => {
      const portions = parseInt(e.target.value) || 0;
       adjustPancake(portions);
    });
     adjustPancake();
  });

  function  adjustPancake(portions) {
    if(typeof  adjustPancake.portions == "undefined"){
       adjustPancake.portions = parseInt( document.getElementById("pancake-portions").value) || 0;
       adjustPancake.flour = document.getElementById('pancake-flour').textContent;
       adjustPancake.milk =  document.getElementById('pancake-milk').textContent;
       adjustPancake.eggs = document.getElementById('pancake-eggs').textContent;
       adjustPancake.salt = document.getElementById('pancake-salt').textContent;
       adjustPancake.butter = document.getElementById('pancake-butter').textContent;
       return;
    }
    document.getElementById('pancake-flour').textContent =   adjustPancake.flour / adjustPancake.portions * portions;
    document.getElementById('pancake-milk').textContent =  adjustPancake.milk / adjustPancake.portions * portions;
    document.getElementById('pancake-eggs').textContent =  adjustPancake.eggs / adjustPancake.portions * portions;
    document.getElementById('pancake-salt').textContent =  adjustPancake.salt / adjustPancake.portions * portions;
    document.getElementById('pancake-butter').textContent =  adjustPancake.butter / adjustPancake.portions * portions;
  }

</script>
  </head>
  <body>
    <h1>Recipies</h1>
    <p>In the following you find my <strong>favourite</strong> recipies. Some are quick to prepare and others might be more sofisticated. This page also allows you to caclulate the ingredients from the portions.</p>
    <h2>Pancakes</h2>
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/Thin_pancakes.jpg/330px-Thin_pancakes.jpg" alt="Delicious pancakes" width="300">
    <h3>Ingredients</h3>
    <p>For <input class="inline" type="text"  id="pancake-portions" pattern="[\d]+" size="32" value="2"> portions</p>
    <ul>
      <li><span id="pancake-flour">200</span> g flour</li>
      <li><span id="pancake-milk">300</span> ml milk</li>
      <li><span id="pancake-eggs">2</span> eggs</li>
      <li><span id="pancake-salt">1</span> pinch of salt</li>
      <li><span id="pancake-butter">20</span> g butter for frying</li>
    </ul>
    <h3>Preparation</h3>
    <ol>
      <li>In a mixing bowl, combine the flour, milk, eggs, and salt. Whisk until smooth.</li>
      <li>Heat a non-stick pan over medium heat and add a little butter.</li>
      <li>Pour in some batter to form pancakes of your desired size.</li>
      <li>Cook until bubbles form on the surface, then flip and cook until golden brown.</li>
      <li>Repeat with the remaining batter, adding more butter as needed.</li>
    </ol>
  </body>
</html>
```

But don't worry if you have no university account for github.
The following result was optained as easily with an AI running locally for free.
I will explain in the next tutorial how to do that...
