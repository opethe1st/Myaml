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
by side with the code and integration tests in tests/. I think that worked well. 
