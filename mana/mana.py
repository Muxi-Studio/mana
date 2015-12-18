# coding: utf-8
"""
mana
~~~~
the missing startapp command for flask

Usage:

    mana init <project_name>

    mana sqlinit <project_name>

    mana blueprint <blueprint_name>

    mana deploy <project_name>
    \__ IP:
    \__ Port:

Options:

    --help:     help information
    --version:  show version
    --home:     link to the doc page

"""

import sys
import os

# project root path
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_path not in sys.path:
    sys.path.insert(0, project_path)

# operators
from operators import _mkdir_p
from operators import init_code

# templates
from templates.manage import _manage_basic_code, _manage_sql_code
from templates.requirement import _requirement_code
from templates.views import _views_basic_code, _views_blueprint_code
from templates.forms import _forms_basic_code
from templates.init import _init_basic_code, _init_code, _init_blueprint_code
from templates.config import _config_sql_code
from templates.models import _models_code

# logging
import logging
from logging import StreamHandler, DEBUG
# logger
logger = logging.getLogger(__name__)
logger.setLevel(DEBUG)
logger.addHandler(StreamHandler())


"""use click:)"""
import click

@click.group()
def cli():
    """the missing startapp command for Flask"""
    pass


@click.command()
@click.argument('project_name')
def init(project_name):
    """
    mana init <project_name>
    """

    # the destination path
    dst_path = os.path.join(os.getcwd(), project_name)

    # dst path exist
    if os.path.isdir(dst_path):
        logger.warning("path: %s exist,\nplease change the project name\n \
                and try again!" % dst_path)
        return

    # start init
    logger.info("start init your flask project!")

    # create dst path
    _mkdir_p(dst_path)

    # create project tree
    os.chdir(dst_path)

    # create files
    init_code('manage.py', _manage_basic_code)
    init_code('requirement.txt', _requirement_code)

    # create app/
    app_path = os.path.join(dst_path, 'app')
    _mkdir_p(app_path)

    os.chdir(app_path)
    # create files
    init_code('views.py', _views_basic_code)
    init_code('forms.py', _forms_basic_code)
    init_code('__init__.py', _init_basic_code)

    # create templates and static
    templates_path = os.path.join(app_path, 'templates')
    static_path = os.path.join(app_path, 'static')

    logger.info("init flask project <%s> done! " % project_name)


@click.command()
@click.argument('project_name')
def sqlinit(project_name):
    """
    mana sqlinit <project_name>
    """

    # the destination path
    dst_path = os.path.join(os.getcwd(), project_name)

    # dst path exist
    if os.path.isdir(dst_path):
        logger.warning("path: %s exist,\nplease change the project name\n \
                and try again!" % dst_path)
        return

    # start init
    logger.info("start init your flask project!")

    # create dst path
    _mkdir_p(dst_path)

    # create project tree
    os.chdir(dst_path)
    # create files
    init_code('manage.py', _manage_sql_code)
    init_code('requirement.txt', _requirement_code)
    init_code('config.py', _config_sql_code)

    # create app/
    app_path = os.path.join(dst_path, 'app')
    _mkdir_p(app_path)

    # create files
    os.chdir(app_path)
    init_code('models.py', _models_code)
    init_code('__init__.py', _init_code)

    # create main/
    main_path = os.path.join(app_path, 'main')
    _mkdir_p(main_path)

    os.chdir(main_path)
    # create files
    init_code('views.py', _views_blueprint_code % ('main', 'main'))
    init_code('forms.py', _forms_basic_code)
    init_code('__init__.py', _init_blueprint_code % ('main', 'main'))

    # create templates and static
    templates_path = os.path.join(main_path, 'templates')
    static_path = os.path.join(main_path, 'static')

    logger.info("init flask project <%s> done! " % project_name)


@click.command()
@click.argument('blueprint_name')
def blueprint(blueprint_name):
    """
    mana blueprint <blueprint_name>
    """

    # destination path
    dst_path = os.path.join(os.getcwd(), blueprint_name)

    # dst path exist
    if os.path.isdir(dst_path):
        logger.warning("path: %s exist,\nplease change the project name\n \
                and try again!" % dst_path)
        return

    # create dst_path
    _mkdir_p(dst_path)

    # change dir
    os.chdir(dst_path)
    # create files
    init_code('__init__.py', _init_blueprint_code % (blueprint_name, blueprint_name))
    init_code('views.py', _views_blueprint_code % (blueprint_name, blueprint_name))
    init_code('forms.py', _forms_basic_code)

    # create templates
    templates_path = os.path.join(dst_path, 'templates')
    _mkdir_p(templates_path)
    # create static
    static_path = os.path.join(dst_path, 'static')
    _mkdir_p(static_path)

    # register auth in app
    os.chdir(os.path.join(dst_path, '..'))
    with open('__init__.py', 'r+') as f:
        prev = pos = 0
        while f.readline():
            prev, pos = pos, f.tell()
        f.seek(prev)
        f.write(
            '    from %s import %s\n    app.register_blueprint(%s, url_prefix="/%s")\n\n    return app'
            % (
                blueprint_name, blueprint_name,
                blueprint_name, blueprint_name
            )
        )

    logger.info("init flask blueprint <%s> done! " % blueprint_name)


# """:version 2.1"""
# @click.command()
# @click.argument('project_name')
# @click.option('--host')
# @click.option('--port', type=int)
# def deploy(project_name, host, port):
#     """deploy your flask application"""
#     click.echo("create wsgi file")
#     os.system("cd %s && touch wsgi.py" % project_name)
#     fill_file_w(project_name, 'wsgi.py', _wsgi_py % (host, port))
# 
#     click.echo("deploy wsgi...done!🍺 ")
# 
# 
# """:version 2.3"""
# @click.command()
# def version():
#     """show the mana version you installed"""
#     click.echo("mana version: 2.6 🍺 ")
# 
# 
# @click.command()
# def home():
#     """go to the homepage of mana"""
#     os.system('python -m webbrowser -t "http://121.43.230.104:520/mana"')


###########################
# mana command set
cli.add_command(init)
cli.add_command(sqlinit)
cli.add_command(blueprint)
# cli.add_command(deploy)
# cli.add_command(version)
# cli.add_command(home)
###########################
