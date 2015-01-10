import sublime
import sublime_plugin

def get_indentation_on_line(view, point): 
    pt = view.line(point).begin()
    result = ''
    while True:
        c = view.substr(pt)
        if c == " " or c == "\t":
            pt += 1
            result += c
        else:
            break
    
    return result

class IndentAndBracesCommand(sublime_plugin.TextCommand):
    def run(self, edit, from_cursor = False):
        sel = self.view.sel()
        for r in tuple(reversed(sel)):
            if from_cursor:
                region = sublime.Region(r.begin(), self.view.line(r.end()).end())
            else:
                region = sublime.Region(self.view.line(r.begin()).begin(), self.view.line(r.end()).end())
            
            # sel.clear()
            # sel.add(region)
            
            indent = get_indentation_on_line(self.view, region.begin())
            if from_cursor:
                insert_start = "{"
            else:
                insert_start = indent + "{\n"
            insert_end = '\n' + indent + '}'
            
            self.view.insert(edit, region.begin(), insert_start)
            self.view.insert(edit, region.end() + len(insert_start), insert_end)
            
            indent_region = sublime.Region(region.begin() + len(insert_start) + 1, region.end() + len(insert_start))
            num_lines_indented = len(self.view.lines(indent_region))
            
            self.view.sel().clear()
            self.view.sel().add(indent_region)
            self.view.run_command('indent')
            
            # Move cursor to beyond last brace
            sel.clear()
            settings = self.view.settings()
            pt = region.end() + len(insert_start) + len(insert_end) + num_lines_indented * (settings.get('tab_size') if settings.get('translate_tabs_to_spaces') else 1)
            sel.add(sublime.Region(pt, pt))