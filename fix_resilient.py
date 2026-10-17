# Fix the resilient_llm.py file
with open(r'M:\Cyber_Teacher\Cyber_Teacher\resilient_llm.py', 'rb') as f:
    content = f.read()
lines = content.split(b'\n')

# Fix the get_status method - lines 361-370 (0-indexed: 360-369)
# The structure should be:
#     return {          <- 8 spaces (inside method, inside for loop)
#         "providers": providers,
#         ...
#         }             <- 8 spaces
#     }                 <- 4 spaces (end of method)

# Current state has issues:
# Line 361 (index 360): '    return {' -> should be '        return {' (8 spaces)
# Line 362: duplicate '        return {' -> remove
# Line 368 (was 369): '    }' -> '        }' (8 spaces)
# Line 369 (was 370): '}' -> '    }' (4 spaces)
# Also line 367-368 had duplicate llm_call_count

# Fix lines
lines[360] = b'        return {'  # 8 spaces

# Remove duplicate 'return {' at line 362 (index 361 after first fix)
# But we need to be careful with indices shifting

# Let me just rebuild the section from line 360 onwards
# Find the start of the return dict
for i, line in enumerate(lines):
    if b'return {' in line and i > 350:
        start_return = i
        break

print(f"return at line {start_return}: {lines[start_return]}")

# Find the end of the method (line with '    def get_provider_name' or similar)
for i in range(start_return, len(lines)):
    if lines[i].strip().startswith(b'def get_provider_name') or lines[i].strip().startswith(b'@property'):
        end_return = i
        break

print(f"end at line {end_return}: {lines[end_return]}")

# Rebuild the section
new_section = [
    b'        return {',
    b'            "providers": providers,',
    b'            "active_provider": getattr(self._current_provider, "model", "unknown") if self._current_provider else "none",',
    b'            "timeout": self._timeout,',
    b'            "llm_call_count": self.llm_call_count,',
    b'            "llm_total_tokens": self.llm_total_tokens,',
    b'            "llm_prompt_tokens": self.llm_prompt_tokens,',
    b'            "llm_completion_tokens": self.llm_completion_tokens,',
    b'        }',
    b'    }',
    b'',
    b'    def get_provider_name(self, llm: Any) -> str:',
    b'        """Get the human-readable provider name for an LLM instance."""',
    b'        return self._provider_names.get(id(llm), "unknown")',
    b'',
    b'    @property',
    b'    def model(self) -> str:',
    b'        """Backward-compatible model attribute."""',
    b'        return getattr(self._primary, "model", "resilient")',
    b''
]

# Replace lines from start_return to end_return-1 with new_section
lines[start_return:end_return] = new_section

with open(r'M:\Cyber_Teacher\Cyber_Teacher\resilient_llm.py', 'wb') as f:
    f.write(b'\n'.join(lines))
print('Fixed!')
"