import random
import string


length = 1024*1024 * 100
# choose from all lowercase letter
letters = string.ascii_lowercase
result_str = ''.join(random.choice(letters) for i in range(length))
print(result_str)