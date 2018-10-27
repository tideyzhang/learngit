几个命令：

git add <filename>
添加具体的文件

git commit -m "what you want to say"
将此前添加的文件提交到 git 中

git status
查看 git 的状态

git diff 
查看更改的地方

git checkout -- <filename>
舍弃工作区的修改，使文章与版本库中一致


git rm <filename>
删除文件，然后需要再次 commit

git reset HEAD <filename>
撤销暂存区的修改，重新置于工作区

HEAD 指当前版本

git log 
查看修改的日志，查看提交的历史（commit）

git log --pretty=oneline
查看历史，以更简单的形式显示

git reset --hard commit_id
回退到指定的版本，版本 id 为 <commit>

git reflog
查看命令历史，以便查看版本
