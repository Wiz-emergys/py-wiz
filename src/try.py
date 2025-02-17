import re 

txt="Price of the product is 50.50 and discount is 25% you can also get it at 45"
pattern=r"\b\d{1,2}+(\.\d+)?\b"
print(re.findall(pattern,txt))