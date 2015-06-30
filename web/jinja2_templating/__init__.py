# -*- coding: utf-8 -*-
import os.path
import cherrypy


class Root(object):
  @cherrypy.expose
  def index(self):
    template = cherrypy.engine.publish('lookup-template', 'index.html').pop()
    print('Index', template)
    return {'msg': 'Hello world!'}

  @cherrypy.expose
  #@cherrypy.tools.jinja2tool(name='abc.html')
  def abc(self):
    return {'msg': 'msg'}


if __name__ == '__main__':
  cherrypy.config.update({'server.socket_port': 8090})
  # Register the Jinja2 plugin
  from jinja2 import Environment, FileSystemLoader
  from jinja2plugin import Jinja2TemplatePlugin

  env = Environment(loader=FileSystemLoader('templates'))
  Jinja2TemplatePlugin(cherrypy.engine, env=env).subscribe()

  # Register the Jinja2 tool
  from jinja2tool import Jinja2Tool

  cherrypy.tools.template = Jinja2Tool()

  # We must disable the encode tool because it
  # transforms our dictionary into a list which
  # won't be consumed by the jinja2 tool
  cherrypy.quickstart(Root(), '', {
    '/': {
      'tools.template.on': True,
      'tools.template.template': 'index.html',
      'tools.encode.on': False
    }
  })