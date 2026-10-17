# Fix resilient_llm.py syntax error
with open(r'M:\Cyber_Teacher\Cyber_Teacher\resilient_llm.py', 'rb') as f:
    content = f.read()
lines = content.split(b'\n')

# Fix the get_status method - lines 361-371
# Current issues:
# Line 361: b'    }' -> should be b'                })' (close dict + providers.append)
# Line 362: '        return {' - stays but needs proper indent
# Line 371: '    }' - extra closing brace

# Let's fix by rebuilding lines 361-371
# Current state:
# 361: b'    }'  <- should be '                })' (8 spaces + })
# 362: b'        return {' - stays
# 363-370: dict content
# 370: '        }' -> should be '        }' (8 spaces) - closes the dict
# 371: '    }' - REMOVE (extra brace)

# Fix line 361
lines[361] = b'                })'

# The return dict is already correct at 362-370
# But line 370 has '        }' (8 spaces) - good
# Line 371 has '    }' - this is the extra one, remove it
del lines[371]  # Remove the extra '    }'

with open(r'M:\Cyber_Teacher\Cyber_Teacher\resilient_llm.py', 'wb') as f:
    f.write(b'\n'.join(lines))
print('Fixed!')