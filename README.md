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

