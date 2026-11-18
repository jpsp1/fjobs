fjobs - browser the Internet for jobs offerings compatible with a CV and other constraints 

---------------------- FILES:

  README.md  = this file

 pyproject.toml =  modules for "uv sync"

load_key.txt  - source this to load the ssh key to push file to the github repository

 upload.ssh  -  update from here to the github repository

node_js_install.sh - sample script


 tests/test01.py -   LLM "hello world" test

tests/test02.py -   read PDF test

tests/test03.py -  pushover external app test (needs API Key)

tests/test04.py -  usage of tools:
     server-filesystem  - open / read / write local files 
     mcp-server-fetch  - fetch URL
    @playwright/mcp@latest  - use browser
    
------------------- INSTALL:

$ cd projects 

$ git clone https://github.com/jpsp1/fjobs

$ cd fjobs

edit .git/config





--------------- node and playwright

$ npx -y playwright@latest screenshot --channel=chrome https://news.ycombinator.com playwright_check.png
Error: command.parse: Chromium distribution 'chrome' is not found at /opt/google/chrome/chrome
Run "npx playwright install chrome"

aaaaaaaaaaaaaa
WARNING: It looks like you are running 'npx playwright install' without first ║
║ installing your project's dependencies.                                       ║
║                                                                               ║
║ To avoid unexpected behavior, please install your dependencies first, and     ║
║ then run Playwright's install command:                                        ║
║                                                                               ║
║     npm install                                                               ║
║     npx playwright install                                                    ║
║                                                                               ║
║ If your project does not yet depend on Playwright, first install the          ║
║ applicable npm package (most commonly @playwright/test), and                  ║
║ then run Playwright's install command to download the browsers:               ║
║                                                                               ║
║     npm install @playwright/test                                              ║
║     npx playwright install                  

------------------- $ which chromium
chromium --version
/usr/bin/chromium
Chromium 156.0.8078.79 built on Debian GNU/Linux 12 (bookworm)


--------------$ npm install playwright

added 2 packages in 2s


aaaaaaaaaaaaaaaaa

git clone https://github.com/jpsp1/fjobs

cat .git/config
[core]
	repositoryformatversion = 0
	filemode = true
	bare = false
	logallrefupdates = true
[remote "origin"]
	url = git@github.com:jpsp1/fjobs
	fetch = +refs/heads/*:refs/remotes/origin/*
[branch "main"]
	remote = origin
	vscode-merge-base = origin/main
	merge = refs/heads/main
[user]
	email = joao.pagaime@gmail.com
	name = joao.pagaime@gmail,com


aaaaaaaaaaaaa

