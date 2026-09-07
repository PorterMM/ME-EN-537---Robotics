# The first step is to import the code from the file "introClass.py" that we wrote.
# other ways to do this include the following (instead of what is shown on line 6):
#######  from introClass import introClassFunObject, introClassFunObjectPartTwo
# but then you would remove the "ic." characters on the lines below.
# %%
import introClass as iC

# now we are making an object of type "introClassFunObject"
studentA = iC.introClassFunObject()

# we can make another student as well:
studentB = iC.introClassFunObject()

# but both of these students will be named "Bob" and have the same scores. Instead
# we can use our other class and do the following which probably makes more sense:
# %%
student2A = iC.introClassFunObjectPartTwo("Sue")
student2B = iC.introClassFunObjectPartTwo("Jim")

# now they have two different names assigned to them, and I can assign different
# lists of scores too (they don't even have to be the same length)
student2A.set_scores([20, 20, 20])
student2B.set_scores([9, 19, 0, 5])


students = [student2A, student2B]

# now we can loop through the students and print their names and scores:
for student in students:
    print(student.name())
