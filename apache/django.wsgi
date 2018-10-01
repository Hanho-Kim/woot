import os,sys

apache_configuration = os.path.dirname(__file__)
project = os.path.dirname(apache_configuration)
workspace = os.path.dirname(project)
sys.path.append(workspace)
sys.path.append('/home/ec2-user/underbar/underbar')
sys.path.append('/home/ec2-user/underbar')
sys.path.append('/home/ec2-user')
#sys.path.append('/venv/lib/python2.7/site-packages')
#sys.path.append('/usr/lib/python2.7/site-packages')
sys.path.append('/opt/virtual-env-27/lib/python2.7/site-packages')
#print('/usr/lib/python2.7/site-packages')
#sys.path.append('/usr/local/lib/python2.7/site-packages')
#sys.path.append('/venv/bin/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'underbar.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()