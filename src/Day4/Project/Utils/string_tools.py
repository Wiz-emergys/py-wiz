
def word_Count(text):
    return len(text)

def find_Most_Commom(text):
    maxi=0
    maxword=""
    try:
        for i in text.split():
            if text.count(i) > maxi:
                maxi=text.count(i)
                maxword=i
        return maxword
    except ValueError:
        return "Error in input"
    except Exception as e:
        return e
    
find_Most_Commom("hey demo demo demo im hey")

def reverse_words(text):
    try :
        return ' '.join(text.split()[::-1])
        # for i in text.split():
            #     print(i[::-1],end=" ")
    except ValueError:
        return "Error in input"
    except Exception as e:
        return e    
    
reverse_words("hey master demo im hey")

def check_palindrome(text):
    try:
        return text == text[::-1]
    except ValueError:
        return "Error in input"
    except Exception as e:  
        return e
print(check_palindrome("madam madam madam madam"))



