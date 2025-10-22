# Local AI coding

If you are using copilot and you want to try the local coding agent. It is as good bye the way!
And fully private. Then you need to first deactivate copilot in the extension manager.

Then first install the continue.dev extension. Follow the tour...

Next we need to install a locally deployed AI model runner: Ollama
Follow the tour...

open command line and install the needed languange models:
```bash
ollama pull Qwen2.5-coder:7b 
ollama pull nomic-embed-text:latest
ollama pull llama3.2:latest         
```

in %USERPROFILE%\.continue\config.yaml
```yaml
name: Local Agent
version: 1.0.0
schema: v1
models:  
  - name: LLama 3.2
    provider: ollama  
    model: llama3.2:latest
    roles:  
      - chat  
      - edit  
      - apply  
      - summarize  
  - name: Qwen 2.5 coder
    provider: ollama  
    model: Qwen2.5-coder:7b
    roles:  
      - autocomplete
    requestOptions:
      extraBodyProperties:
        think: false # turning off the thinking
    autocompleteOptions:
      multilineCompletions: always
  - name: embeddingsProvider  
    provider: ollama  
    model: nomic-embed-text  
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
Now you can use continue to tap complete your code but also to chat.
In chat - which you open with CTRL+L -  you can type for example type:
  
```
please explain me this codebase @Codebase

how does this file work @filename

```
and click on file.
