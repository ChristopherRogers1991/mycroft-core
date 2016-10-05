from bottle import route
from bottle import redirect
from bottle import get
from bottle import run
from bottle import request
from os.path import dirname
from os.path import join
from mycroft.skills import core as skills
from subprocess import call


@route('/hello')
def hello():
    return "Hello World!"


@route('/config')
def config():
    html ="""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Mycroft Config</title>
    <script type="none_yet"></script>
</head>
<body>
    <form action='whitelist'>
        <ol>
            {checks}
        </ol>
        <input type="submit" value="Submit">
    </form>
</body>
</html>"""

    check_template = "<li><input type='checkbox' name='{skill}' value='on' {checked}>{skill}</input></li>"

    skill_list = skills.get_skills(skills.SKILLS_BASEDIR)

    with open(skills.USER_WHITELIST, mode='r') as f:
        enabled_skills = set(f.read().splitlines())

    checks = '\n'.join([
                           check_template.format(
                               skill=skill['name'],
                               checked='checked' if skill['name'] in enabled_skills
                                   else ''
                           ) for skill in skill_list
                       ])

    return html.format(checks=checks)


@get('/whitelist')
def whitelist():
    with open(skills.USER_WHITELIST, mode='w') as f:
        f.write('\n'.join(request.GET))
    script = join(dirname(dirname(dirname(__file__))), 'mycroft.sh')
    # restart does not work if it is not already running
    call([script, 'stop'])
    call([script, 'start'])
    redirect('/config')


if __name__ == '__main__':
    script = join(dirname(dirname(dirname(__file__))), 'mycroft.sh')
    run(host='0.0.0.0', port=8080, debug=True)