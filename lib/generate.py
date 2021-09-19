def generate(key, url):
    output = ('command -v curl >/dev/null && X=' + key + ' bash -c "$(curl -fsSL ' + url +')" || X=' + key + ' bash -c "$(wget -qO- ' + url +')"')
    return(output)
