# %% [markdown]
# # Intro to Python
# This is a brief introduction to Python for those who are new to the language. Any "markdown" section
# is text or a comment that will not be displayed if you run the code using Python. But if you run the
# code using Jupyter Notebook, the markdown sections will be displayed as text. This syntax
# (# %% [markdown]) and (# %% [code]) is specific to Jupyter Notebook, and is not used in Python. But
# it will allow you to run individual sections or cells of code in the notebook, instead of the whole
# script.

# %%[markdown]
# ## Printing to the Console or Terminal

# %%[code]
# This is how we do a comment! Anything with the "#" symbol will not be evaluated.

# printing is something we need to do often, but it's easy in Python:
print("Hello, world!")  # notice that it's a function we call,
# and pass what we want printed as an argument

# we can also print a mix of strings and variables:
a = "the number is:\t"  # \t is a formatting character for a tab
b = 5
print(a, b)  # notice that we can print multiple things at once

# %%[markdown]
# ## Working with Lists

# %%[code]

# the default way to hold arrays of variable types is a list:
c = [1, 2, 3, 4, 5]
print("a normal list:", c)

# we can access elements of a list by index:
print("\n demonstrations of list indexing:")
print(c[0])  # 0-based indexing

# we can also access elements from the end of the list:
print(c[-1])  # negative indexing starts from the end

# we can also access a range of elements similar to MATLAB:
print(c[1:3])  # the range is inclusive of the first index and exclusive of the second

# we can also access a range of elements from the beginning or end:
print(c[:3])  # the range starts at the beginning

# we can also access a range of elements to the end:
print(c[3:])  # the range goes to the end


# we can also operate on each entry in a list as follows:
for i in range(len(c)):
    c[i] = c[i] + 1

# but if we don't like using indices, or the list is already ordered, we can use a for-each loop:
print("\n example of a for-each loop:")
for entry in c:
    print(
        entry
    )  # this will print each entry in the list, and "entry" is a variable that we
    # we get to pick, i.e. it could be anything as it just represents an entry
    # in the list "c"

# finally, there are ways in Python to operate on lists more efficiently, such as using "list comprehension":
c_new = [
    entry + 1 for entry in c
]  # This will add 1 to each entry in the list "c", with the result being
# another list.
# Using list comperehension is much faster, but sometimes hard to perform
# the desired operation on each element in the list.
print("\n list comprehension example:")
print(c_new)


# we can add lists together, but this usually means concatenation, not matrix or vector addition:
d = [6, 7, 8]
e = c + d
print("\n concatenation of two lists:")
print(e)

# finally, lists can be used to hold any type of variable:
d = [
    "a",
    1,
    2.0,
    [1, 2, 3],
]  # but mixing data types like we've done here is not recommended.

# Dictionaries are another way to store arrays of information by keys or key words, rather than indices:
a_dict = {"red": 1, "green": 2, "blue": 3}
print("\n dictionary example of using key to access value:")
print(a_dict["red"])  # this will print the value associated with the key "red"

# to get keys and values from a dictionary, we can use the following:
keys = a_dict.keys()

# then we can use the keys to step through entries in the dictionary:
print("\n example of stepping through each entry in a dictionary:")
for key in keys:
    print(a_dict[key])


# %%[markdown]
# ## Numpy Arrays and Operations for Linear Algebra

# %%[code]

# because we can't do matrix operations with lists, we use numpy arrays from the numpy library:
import numpy as np  # This is how we import a library in Python, it's like an "include" statement in C++.

# Using the "as" keyword allows us to give the library a shorter name that we can use
# thereafter in the rest of the code.

a = np.array([1, 2, 3, 4, 5])  # this is how we create a numpy array from a list

print("\n numpy array examples:")
# we can access elements of a numpy array the same way we do with lists:
print(a[0])

# we can also access a range of elements the same way we do with lists:
print(a[1:3])

# we can also operate on each entry in a numpy array the same way we do with lists:
b = np.zeros(5)  # this is how we create a numpy array of zeros
print("this is b before:", b)
for i in range(len(a)):
    b[i] = a[i] + 1
print("this is b after:", b)

# now we can also do matrix operations:
b = np.array([6, 7, 8, 9, 10])
c = a + b
print("\n numpy array addition:")
print(c)  # this will add each element in a to the corresponding element in b

# we can also do matrix multiplication:
d = np.array([[1, 2], [3, 4]])
e = np.array([[5, 6], [7, 8]])
f = np.matmul(d, e)
print("\n numpy array matrix multiplication:")
print(f)  # this will multiply the two matrices together

# we can also do element-wise multiplication:
g = a * b
print("\n numpy array element-wise mult.:")
print(g)  # this will multiply each element in d to the corresponding element in e

# we can also use the shortcut for matrix muliplication, which is the "@" symbol:
h = d @ e
print("\n numpy array matrix mult. with @:")
print(h)  # this will multiply the two matrices together

# if we use "@" with two vectors, it will do the dot product:
i = a @ b
print("\n numpy array examples of dot product:")
print(i)  # this will do the dot product of a and b

# but there are often numpy functions to explicitly peform these same operations:
j = np.dot(a, b)
print(j)  # this will do the dot product of a and b

# finally for numpy arrays, we can transpose or reshape them to complete the desired matrix operations:
k = d.T @ e  # this will transpose d and multiply it by e
print("\n numpy array example of transpose:")
print(k)

# we can also reshape a numpy array:
l = np.array([1, 2, 3, 4, 5, 6])
print("\n numpy array example finding shape of array:")
print(
    l.shape
)  # this will print the shape of the numpy array, with row and column dimensions
m = l.reshape((2, 3))
print("\n numpy array example reshaping array:")
print(m)

# we can also flatten a numpy array:
n = m.flatten()
print("\n numpy array example flattening an array:")
print(n)

print("\n numpy array examples of stacking vectors/arrays:")
# we can also stack numpy arrays:
o = np.hstack((d, e))  # this will stack the two matrices horizontally
print(o)
p = np.vstack((d, e))  # this will stack the two matrices vertically
print(p)

# we can also concatenate numpy arrays:
q = np.concatenate(
    (d, e), axis=0
)  # this will concatenate the two matrices along the rows
print(q)


print(
    "\n examples of linear algebra operations are not printed, but shown in code here."
)
# there are also a number of matrix operations, (e.g. inverse, determinant, etc.) that
# we can do with numpy:
d_inv = np.linalg.inv(d)
d_det = np.linalg.det(d)

# we can also solve a system of linear equations:
x = np.linalg.solve(d, np.array([1, 2]))

# we can also find the eigenvalues and eigenvectors of a matrix:
eigvals, eigvecs = np.linalg.eig(d)

# we can also find the singular value decomposition of a matrix:
u, s, vh = np.linalg.svd(d)


# %%[markdown]
# ## Plotting Data
# There isn't space here to devote to lots of plotting examples, but we can show
# some simple examples of using matplotlib:

# %%[code]
import matplotlib.pyplot as plt  # this is how we import the matplotlib library for plotting

plt.figure()  # this creates a new figure for plotting
plt.plot(a, b)  # this will plot the values in a against the values in b
plt.xlabel("a")  # this will label the x-axis
plt.ylabel("b")  # this will label the y-axis
plt.title("a vs b")  # this will give the plot a title
plt.show()  # this will display the plot

# if we want to plot multiple things on the same plot:
plt.figure()
plt.plot(a, b, "k--", label="b")
plt.plot(a, c, "b-.", label="c")
plt.legend()  # this will add a legend to the plot, using the labels we assigned to each line
plt.show()

# we can also plot multiple thing on subplots:
plt.figure()
plt.subplot(
    2, 1, 1
)  # this will create a subplot with 2 rows and 1 column, and plot the first thing
plt.plot(a, b, label="b")
plt.ylabel("b")
plt.subplot(
    2, 1, 2
)  # this will create a subplot with 2 rows and 1 column, and plot the second thing
plt.plot(a, c, label="c")
plt.ylabel("c")
plt.xlabel("a")
plt.show()


# %%[markdown]
# ## Other useful numpy functions:
# Most of the linear algebra functions you would want are available in np.linalg.
# While a number of other useful vector and matrix operations are available in np, such as:

# - np.cos, np.sin, np.atan2
# - np.cross - for a cross product
# - np.mean, np.std, np.var - for statistical operations
# - np.where - for conditional operations on specific elements in a vector
# - np.distrib.random - for random number generation
# - np.interp - for interpolation
# - np.fft - for fast fourier transform operations

# ## Other useful Python libraries and tools:
# There are a number of more detailed labs and tutorials from the BYU ACME program:
# - intro to Python - https://acme.byu.edu/00000181-448a-d778-a18f-dfcae22f0001/intro-to-python
# - intro to Numpy - https://acme.byu.edu/00000181-4478-d9e0-a789-7e7e0fe00001/numpy
# - intro to Matplotlib - https://acme.byu.edu/00000181-447a-d0f9-a7bd-fffa0f8d0001/matplotlib


# We can also use other libraries like "scipy" for more advanced operations, such as:
# - math.sqrt, math.exp, math.log - for basic math operations
# - scipy.optimize - for optimization
# - scipy.integrate - for numerical integration
# - scipy.signal - for signal processing
# - scipy.stats - for statistical analysis
# - scipy.ndimage - for image processing
# - scipy.fftpack - DFT and other functions - see https://acme.byu.edu/00000181-a758-d778-a18f-bf5abcb10001/dtf-pdf

# There are also libraries like "pandas" for data manipulation and analysis (see), OpenCV for computer vision,
# "scikit-learn" and "pytorch" for deep learning.
