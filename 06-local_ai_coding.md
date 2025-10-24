# Local AI coding

If you are using copilot and you want to try the local coding agent, then you need to first deactivate copilot in the extension manager. Local coding agent has the advantage that your source code is not transferred into the cloud.
If you work in a company they might demand this from you.

Then first install the continue.dev extension. Follow the tour...

Next we need to install a locally deployed AI model runner: Ollama
Follow the tour...

open command line and install the needed languange models:

```bash
ollama pull dengcao/Qwen3-Reranker-0.6B:Q8_0  
ollama pull danielsheep/Qwen3-Coder-30B-A3B-Instruct-1M-Unsloth:UD-IQ3_XXS 
ollama pull hf.co/dat-lequoc/Fast-Apply-1.5B-v1.0_GGUF:latest  
ollama pull nate/instinct:latest  
ollama pull nomic-embed-text:latest  
ollama pull Qwen2.5-coder:1.5b   
```

in %USERPROFILE%\.continue\config.yaml

```yaml
name: Local Config
version: 1.0.0
schema: v1
models:
  - name: Autodetect
    provider: ollama
    model: AUTODETECT

    roles:
      - chat
      - edit
      - apply
      - summarize
      - autocomplete
      - rerank
  - name: embeddingsProvider
    provider: lmstudio
    model: text-v2-moeext-embedding-nomic-embed-t
    roles:
      - embed
context:
  - provider: code
  - provider: docs
  - provider: diff
  - provider: terminal
  - provider: problems
  - provider: folder
  - provider: codebase
```

the following configurations needs to be set in continue extension by selecting ``open settings`` from the continue menue (bottom right):

![](06-local_ai_coding.assets/20251023_220003_image.png)

Now you can use continue to tap complete your code but also to chat.
To open the chat window you can do the following press CTRL+SHIFT+P then type ``View: toggle continue``.
In chat - which you open with CTRL+L -  you can type for example type:

```
please explain me this codebase @Codebase

how does this file work @filename

```

and click on file.

you can also mark a text and press CTRL+I and say for example: ``make comments``.

Lets make a different thing how about a fibonacci [$f(0)=0, f(1)=1,f(n)=f(n-1)+f(n-2)$] number calculator.

lets make life a bit hard for ai by starting with something completely corrupted:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calculator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
        }
        
        button {
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            background-color: #4CAF50;
            color: white;
            cursor: pointer;
        }
        
        input[type="number"] {
            width: 100%;
            height: 40px;
            margin-bottom: 10px;
            padding: 0 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
    </style>
</head>
<body>

    <h2>Calculator</h2>
    <input type="number" id="num1" placeholder="Number 1">
    <input type="number" id="num2" placeholder="Number 2">
    <button onclick="calculate()">Calc</button>
    <p id="result"></p>
    <!--a secound field with result2-->
    <p id="result2"></p>

    <script>
        function calculate() {
            var num1 = document.getElementById("num1").value;
            var num2 = document.getElementById("num2").value;

            // now we want to multiply num1 with num2
           var result = num1 * num2;//I have just typed TAB on the keyboard
           
            
            document.getElementById("result").innerHTML = "Result: " + result;

            //we want to also output the sum of num1 and num2
            var result2=num1+num2;
            document.getElementById("result2").innerHTML = "Sum: "+result2;
            //again with TAB it was writing the code for me
            //now lets ask
            //calculate the nth fibonacci number
            function fibonacci(n) {
                if (n <= 1) return n;
    else return fibonacci(n-1)+fibonacci(n-2)
            }

                    
    
    </script>
</body>
</html>

```
 and just put your cursor where the fibonacci function is and try to press tab to get the results.

Then use the life server extension to see the result. It does not work.

Ask the ai chat to correct it itteratively.

Next we will use an ai coding agent that can even generate complete projects.