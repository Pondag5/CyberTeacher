# Fix the resilient_llm.py indentation issues
with open(r'M:\Cyber_Teacher\Cyber_Teacher\resilient_llm.py', 'rb') as f:
    content = f.read()
lines = content.split(b'\n')

# The issue: return { is inside the for loop, should be after
# Line 361 (index 361) currently has 'return {' inside the loop
# It should close the loop first, then return

# Find the return statement in the loop
for i, line in enumerate(lines):
    if b'return {' in line and i > 350 and i < 370:
        print(f"Found return at line {i}: {line}")

# Fix: Move return outside the for loop
# Line 361 currently has 'return {' inside the loop
# Change line 361 to close the for loop: '    }' (4 spaces)
# Then insert the return dict after the loop

# Current structure around lines 350-370:
# 345: providers = []
# 346: for i, llm in ...:
# 352:     providers.append({...})
# 361: return {  <- WRONG - inside loop
# 362-368: dict contents
# 368: }  (closes dict)
# 369: }    (closes method)

# Should be:
# 345: providers = []
# 346: for i, llm in ...:
# 352:     providers.append({...})
# 361: }  (closes for loop)
# 362: return {
# 363-369: dict contents
# 370: }
# 371: }  (closes method)

# Fix line 361 (index 361) - change return { to }
lines[361] = b'    }'  # Close for loop with 4 spaces

# Insert return dict after line 361 (now at index 361 after modification)
return_dict = [
    b'        return {',
    b'            "providers": providers,',
    b'            "active_provider": getattr(self._current_provider, "model", "unknown") if self._current_provider else "none",',
    b'            "timeout": self._timeout,',
    b'            "llm_call_count": self.llm_call_count,',
    b'            "llm_total_tokens": self.llm_total_tokens,',
    b'            "llm_prompt_tokens": self.llm_prompt_tokens,',
    b'            "llm_completion_tokens": self.llm_completion_tokens,',
    b'        }',
    b'    }',  # close method
]

# Insert at index 362 (after the for loop close at index 361)
new_lines = lines[:362] + return_dict

with open(r'M:\Cyber_Teacher\Cyber_Teacher\resilient_llm.py', 'wb') as f:
    f.write(b'\n'.join(new_lines))

print('Fixed')