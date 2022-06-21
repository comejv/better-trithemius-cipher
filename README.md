# py-crypt
Simple encryption script based on the position of the char relatively to a juxtaposed alphabet (that can be shuffled with a given key), then transformed into a letter again. Similar to the Trithemius cipher.

Non alphanumeric characters are not encrypted (except space when using level 2 or 3).

Structure can be preserved or not.

The same algorithm is applied sepparately to numbers if users choses to do so.

## Example
Encrypting the string `Test 123 hello!` using level 3 encryption and key = 1234 gives this output : `togz95rv7k9sw7q!`
