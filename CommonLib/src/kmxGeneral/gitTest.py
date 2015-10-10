'''
Created on Oct 11, 2015

@author: MUKUND
'''
import os
from git import Repo
os.environ["GIT_PYTHON_GIT_EXECUTABLE"]=r'G:\Git\bin\git.exe'     
srepo = 'J:\devcon-scripts'

repo = Repo(srepo)

print(repo)
print(repo.heads.master)

print(repo.commit('master'))