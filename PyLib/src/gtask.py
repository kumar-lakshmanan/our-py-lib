import libgtasks
user = libgtasks.User('kaymatrix@gmail.com', 'mufuokfvnojtzqvm')
user.login()

print user.requested_list.name
for task in user.requested_list.tasks:
	print task.name