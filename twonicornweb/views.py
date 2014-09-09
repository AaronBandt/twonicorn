import TwonicornWebLib
from pyramid.view import view_config, forbidden_view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget
from pyramid_ldap import get_ldap_connector
import pprint


t_core = TwonicornWebLib.Core('/app/twonicorn_web/conf/twonicorn.conf')
t_facts = TwonicornWebLib.tFacter()

#@view_config(route_name='home', permission='view')
#def logged_in(request):
#    return Response('OK')

@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return Response('Logged out', headers=headers)

@view_config(route_name='login', renderer='templates/login.pt')
@forbidden_view_config(renderer='templates/login.pt')
def login(request):
    url = request.current_route_url()
    login = ''
    password = ''
    error = ''

    if 'form.submitted' in request.POST:
        print "trying to log in"
        login = request.POST['login']
        password = request.POST['password']
        connector = get_ldap_connector(request)
        data = connector.authenticate(login, password)
        pprint.pprint(connector)
        pprint.pprint(data)

        if data is not None:
            dn = data[0]
            headers = remember(request, dn)
            return HTTPFound('/', headers=headers)
        else:
            error = 'Invalid credentials'

    return dict(
        login_url=url,
        login=login,
        password=password,
        error=error,
        )

@view_config(route_name='home', permission='view', renderer='templates/home.pt')
def logged_in(request):
    return {'project': 'twonicorn-ui'}
#    return Response('OK')

@view_config(route_name='applications', renderer='templates/applications.pt')
def view_applications(request):

    try:
        applications = t_core.list_applications()
    except:
        raise
    return {'applications': applications, 'total': len(applications)}

@view_config(route_name='deploys', renderer='templates/deploys.pt')
def view_deploys(request):

    params = {'application_id': None,
              'nodegroup': None,
              'history': None,
              'deploy_id': None,
              'env': None}
    for p in params:
        try:
            params[p] = request.params[p]
        except:
            pass

    application_id = params['application_id']
    nodegroup = params['nodegroup']
    history = params['history']
    deploy_id = params['deploy_id']
    env = params['env']

    deploys_dev = None
    deploys_qat = None
    deploys_prd = None
    hist_list = None

    if application_id:
        try: 
            deploys_dev = t_core.list_deploys('dev',application_id,nodegroup)
            deploys_qat = t_core.list_deploys('qat',application_id,nodegroup)
            deploys_prd = t_core.list_deploys('prd',application_id,nodegroup)
        except:
            raise
    elif nodegroup:
        try:
            deploys_dev = t_core.list_deploys('dev',application_id,nodegroup)
            deploys_qat = t_core.list_deploys('qat',application_id,nodegroup)
            deploys_prd = t_core.list_deploys('prd',application_id,nodegroup)
        except:
            raise

    if history:
        try:
            hist_list = t_core.list_history(env,deploy_id)
        except:
            raise

    return {'deploys_dev': deploys_dev,
            'deploys_qat': deploys_qat,
            'deploys_prd': deploys_prd,
            'application_id': application_id,
            'nodegroup': nodegroup,
            'history': history,
            'hist_list': hist_list,
            'env': env,
            'deploy_id': deploy_id
           }

@view_config(route_name='promote', renderer='templates/promote.pt')
def view_promote(request):
    return {'project': 'twonicorn-ui'}

@view_config(route_name='help', renderer='templates/help.pt')
def view_help(request):
    return {'project': 'twonicorn-ui'}
