===================
LED controller test
===================

Imagine we have two machines to build products.
The *./product_a_keywords.robot* file contains keywords to control machine A, which builds product A.
Similarly the *./product_b_keywords.robot* file contains keywords to control machine B, which builds product B.

We need to check whether these 2 machines do not interact with each other during work!


Usage
=====

Install dependencies:

`$ pip install -r requirements.txt`

Run test:

`robot -L TRACE -d logs test.robot`
