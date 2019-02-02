Learned to start small.
Ignore the details and focus on a minimal implementation.
For example, I initially wanted to deal with quoted strings, with double and single quotes, with how
to identity the indentation,  etc - but that's all details that I can get to work later.
What I decided to do instead is focus on the mapping type - because it is fundamental. I have purposely not dealt with arrays yet.


Dealt with sequences and mappings.
What did I learn from this exercise?
Domain Driven Design FTW! Initially, I wrote this by trying to write a parse function, but it was all messy and had
all sorts of case statements to handle the different types. My next approach was to write a Node class and implement
parsing logic in the from_string method. This also had case statements everywhere.
Final iteration was to think about the domain, what were the fundamental types and code based on those.
And the code looks better but it's not perfect but it works as far as I want it too.

Next step, might be implement the reverse of parse. This is a simple exercise and it took too long I think. I plan
to improve on my implementation skills. TDD is also awesome! and I experimented with having the _test.py files side
by side with the code and integration tests in tests/. I think that worked well - probably means I need to figure out how to exclude test files from the library package.

Maybe I can extend this to support parsing json and retain the node as the central thing. Means I will remove the from_string method from the Node
and make it a standalone - this support the open close principle because I wont need to modify the Node anymore if I need to add a new way of parsing.
Will make it easy to convert from json to yaml and yaml to json, from json to string and string to json, from yaml to string and string to yaml and from yaml string to json string and vice-versa!
Nice Nice! And adding new types is just as easy.

Got it working. Yay! What next?
* Need to write a draft of a blogpost detailing what I have done here and why I took certain decisions
* Implement scalars to integers and other primitive types
* support quoted strings
* support flow types
* add more complex tests to make sure everything is working
* better error reporting


tried to keep my tests side by side with the code, but realized I couldnt come up with a way to exclude them from my packages - that's what happens when you go
against conventions

So I want to add support for arbitary indentation - initially I was going to do this by adding the indentSize as a parameter to the from_string methods
but I soon realized that I would be passing this variable everywhere - tramp data. I hit upon another approach, convert what I have to string with arbitary indentSize
into the currently supported indentSize. Viola! this meant I just need to replace the detected indent with the desired one.
Works right? Almost! So there is this condition - what happens when the line starts with `- `(a dash and three spaces?) this needs to become `-   `. Tricky.
My find replace no longer works. So what can I do? new idea - first replace - `- ` with `#`(or some other special character) (this requires I am ignoring the comments, I am not currently doing this)
and then replace the spaces at the begin of lines with `!`. and replace in order first. then replace `#` with the desired indent and `!` with `-` + ' '*desired indentSize


commenting doesnt work

key: value#valu - would be wrong


Finally have some insights, the code is going to be beautiful :D
I should probably add linting with flake8 or pylint (how do I decide which one?)
And also type hints with mypy - question is are they worth the hassle?
hated the mutual recursion between the parent class and the subclasses. I think it is a bad idea that the class knows about its subclasses.
Dependency should be one-way... but how does this apply to the observer pattern?


Refactoring now - this is a better design, I think, so far!

Refactoring is such a joy when you have integration tests
