import time  # this is just an example of how we include external code (either system-level

# libraries or code you've added to the python path) or code that is in the
# same folder


class introClassFunObject:
    """
    This class is pretty simple and pretty silly, but here you go. This is the documentation
    that is displayed when you have auto-complete enabled. Comments with the triple apostrophe
    can also be added underneath any function definition if you think it might help.
    """

    # this is an initilization function (called a constructor) that should be defined for every new
    # type of class that you would want to make. This code is called first, and only once, when you
    # make a new object of this type.
    def __init__(self):
        self.name = "Bob"
        self.scores = [10, 10, 9, 10, 3]

    # the rest of the functions below either operate on other member functions or member variables.
    # the term "member" just refers to functions or variables that belong to the class. Notice
    # how every member variable (that you want to be accessible in other functions or used in
    # external code) and every member function require "self" in the syntax.
    def get_name(self):
        print(self.name)

    def get_avg_scores(self):
        total = 0.0

        for score in self.scores:
            total = total + score
            print("this is the score:\t", score)

        avg_score = total / len(self.scores)

        print("Avg score is:\t", avg_score)

    def add_score(self, new_score):
        self.scores.append(new_score)


### This 2nd example of a class definition is not something we would normally do since it's so
# similar to the first class, however, I wanted to show an example where you can pass in an
# argument to the __init__ function.
class introClassFunObjectPartTwo:
    """
    This class is pretty simple and pretty silly, but here you go, part 2.
    """

    def __init__(self, name="bob"):
        self.name = name
        self.time_created = time.time()

    def get_time_created(self):
        print(self.time_created)

    def set_scores(self, scores):
        self.scores = scores

    def get_avg_scores(self):
        total = 0.0

        for score in self.scores:
            total = total + score

        avg_score = total / len(self.scores)

        print("Avg score is:\t", avg_score)
