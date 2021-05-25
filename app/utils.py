

def extractElement(domTree, selector, attribute=None):
    try:
        if attribute:
            if  isinstance(attribute, str):
                return domTree.select(selector).pop(0)[attribute].strip()
            else:
                return [x.get_text().strip() for x in domTree.select(selector)]
        else:
            return domTree.select(selector).pop(0).get_text().strip()
    except IndexError:
        return None