def _ParseLine(line_num, line):
    insideQuote = False
    result = []
    word = ''
    
    i = 0
    while i < len(line):
        c = line[i]
        
        if not insideQuote:
            if c == '#':
                # Found start of comment
                line = line[:i].strip()
                break
            
            elif c == '"':
                if word == '':
                    # Found start of a quote
                    insideQuote = True
                else:
                    # Found quote inside word. Keep it there
                    word += c
                
            elif c.isspace():
                if word != '':
                    result.append(word)
                word = ''
                
            else:
                word += c
            
        else: # insideQuote
            if c == '\\' and line[i + 1] == '"':
                word += '"'
                i += 1
            
            elif c == '"':
                result.append(word)
                word = ''
                insideQuote = False
                
            else:
                word += c
        
        i += 1
    
    if word != '':
        result.append(word)
    
    if len(result) > 0:
        result.insert(0, line_num)
        result.insert(1, line)
        
    return result
    

def Parse(lines):
    rules = []
    
    line_num = 0
    for line in lines:
        line = line.strip('\r\n').strip()
        line_num += 1
        
        if line == '':
            continue
        
        rule = _ParseLine(line_num, line)
        if rule:
            rules.append(rule)
    
    return rules
