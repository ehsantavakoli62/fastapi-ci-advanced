from typing import List

def decrypt(encrypted_message: str) -> str:
    """
    Decrypts a message based on a specific set of rules:
    - '.' after a character means keep the character, remove the dot.
    - '..' after a character means remove the previous character and both dots.
    The rules are applied sequentially from left to right.
    
    Args:
        encrypted_message (str): The encrypted string.
    
    Returns:
        str: The decrypted message. Can be an empty string.
    """
    decrypted_chars: List[str] = []
    i = 0
    while i < len(encrypted_message):
        char = encrypted_message[i]

        if char == '.':
            # Handle dots that might be at the beginning or after another dot
            # These dots should just be skipped as they don't follow a character
            if not decrypted_chars or decrypted_chars[-1] == '.':
                 i += 1
                 continue
            
            # Check for a double dot '..'
            if i + 1 < len(encrypted_message) and encrypted_message[i + 1] == '.':
                # Rule: '..' means remove previous character
                if decrypted_chars: # Ensure there is a character to remove
                    decrypted_chars.pop()
                i += 2 # Skip both dots
            else:
                # Rule: '.' means keep previous character (already kept), remove this dot
                i += 1 # Skip the single dot
        else:
            # Add normal character to the list
            decrypted_chars.append(char)
            i += 1
            
    return "".join(decrypted_chars)

if __name__ == '__main__':
    # This block is for direct execution and not strictly part of the test setup.
    # It can be used for manual testing of the decrypt function.
    pass
