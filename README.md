fjobs - browser the Internet for jobs offers compatible with a CV and other constraints. Make a report of it, separating new offers from old offers

                 nov 2026, João Pagaime
				 (credits on snippets to Ed Donner's wonderful online course on agentic AI)

https://github.com/jpsp1/fjobs

---------------------- general requirments

several API keys - openai, etc

---------------------- FILES:

  README.md  = this file

 pyproject.toml =  modules for "uv sync"

load_key.txt  - source this to load the ssh key to push file to the github repository

 upload.ssh  -  update from here to the github repository

node_js_install.sh - sample script


 tests/test01.py -   LLM "hello world" test

tests/test02.py -   read PDF test

tests/test03.py -  pushover external app test (needs API Key)

tests/test04.py -  usage of MCP tools:
     server-filesystem  - open / read / write local files 
     mcp-server-fetch  - fetch URL
    @playwright/mcp@latest  - use browser
    
tests/test05.py -  usage of MCP tools:	
     @modelcontextprotocol/server-memory 

tests/test06.py -  example os structured outputs with list 

fjobs.py - main file

------------------- INSTALL:

$ cd projects 

$ git clone https://github.com/jpsp1/fjobs

$ cd fjobs

edit .git/config

...and more
