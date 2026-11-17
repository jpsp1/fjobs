fjobs - browser the Internet for jobs offerings compatible with a CV and other constraints 

---------------------- FILES:

  README.md  = this file

 pyproject.toml =  modules for "uv sync"

load_key.txt  - source this to load the ssh key to push file to the github repository

 upload.ssh  -  update from here to the github repository

------------------- INSTALL:

$ cd projects 

$ git clone https://github.com/jpsp1/fjobs

$ cd fjobs

edit .git/config



aaaaaaaaaaa


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

