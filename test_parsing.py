from parsing import parse_coordinator_output

# Test case 1: a clear response
clear_example = """TOPIC: binary search trees
LEVEL: intermediate
NOTES: student knows basic data structures"""

print("Test 1:", parse_coordinator_output(clear_example))

# Test case 2: an unclear response
unclear_example = "CLARIFICATION_NEEDED: What aspect of recursion do you want to learn?"

print("Test 2:", parse_coordinator_output(unclear_example))

from parsing import parse_quiz_output

fake_quiz = """Q1: What is the time complexity of searching in a balanced BST?
ANSWER1: O(log n)

Q2: What happens if you insert values in sorted order into a BST?
ANSWER2: It degrades into a linked list with O(n) operations

Q3: Which child holds smaller values in a BST?
ANSWER3: The left child"""

print("Test 3:", parse_quiz_output(fake_quiz))