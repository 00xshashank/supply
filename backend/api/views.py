from django.shortcuts import render
from django.http import request, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from pydantic import BaseModel, EmailStr, ValidationError
import json

from api.agent.description_agent import DescriptionAgentCaller

from api.mongo import create_project, get_projects, get_project_id, get_all_messages, get_researched_content
from api.redis_ops import get_task_status
from api.neo4j_ops import get_all_nodes

class CreateUserRequest(BaseModel):
    name: str
    password: str
    email: EmailStr

description_agent = DescriptionAgentCaller()

SAMPLE_PROMPT = """
The company operates a small-to-medium-scale toy manufacturing business focused on the design and production of educational and play-oriented toys for children. Manufacturing activities are centralized at a single production facility, with an emphasis on safety compliance, cost efficiency, and scalable product lines. Core Activities: Design & Manufacturing: Operates one primary toy manufacturing facility responsible for: Product design finalization Molding, assembly, finishing, and packaging Produces a range of toys including: Plastic toys Wooden toys Simple mechanical and educational playsets Production processes combine automated machinery with manual assembly for quality-sensitive components. Raw Material Sourcing: Primary Materials: Plastic resins (e.g., ABS, polypropylene) sourced from Reliance Petrochemicals. Wood materials (e.g., rubberwood, plywood) sourced from domestic and nearby regional suppliers. Metal components (screws, springs, fasteners) sourced from local hardware manufacturers. Finishing & Safety Materials: Non-toxic paints, dyes, and coatings sourced from certified suppliers to meet child safety standards. Packaging materials such as printed boxes, inserts, and protective wraps sourced from domestic packaging manufacturers. Supplier Network: Majority of suppliers are located domestically to reduce lead times and ensure supply stability. Select specialty components (e.g., electronic modules for interactive toys or specialty finishes) are imported from international suppliers on Ebay. Logistics & Distribution: All inbound and outbound logistics are handled by DTDC. Sales & Distribution Channels: Products are sold through: Online marketplaces Customers: Primary customers include: Independent toy retailers Online consumers
"""

@csrf_exempt
def signupRoute(request):
    if request.method == 'POST':
        body_json = json.loads(request.body)
        try:
            user_validated = CreateUserRequest(
                name=body_json['name'],
                password=body_json['password'],
                email=body_json['email']
            )
        except KeyError as k:
            return JsonResponse({
                "status": "failure",
                "message": "Malformed request, please try again later"
            })
        
        # TODO: Show errors on frontend
        except ValidationError as v:
            print(v)
            error_list = v.errors(include_context=False)
            print(error_list)
            return JsonResponse({
                "status": "success",
                "message": error_list
            })

        user_save = User.objects.create_user(
            username=user_validated.name,
            email=user_validated.email,
            password=user_validated.password
        )
        user_save.save()

        return JsonResponse({
            "status": "success",
            "message": "created user successfully"
        })
    else:
        return JsonResponse({
            'status': 'success',
            'message': 'Method not allowed on this endpoint'
        })

@csrf_exempt
def loginRoute(request):
    if request.method == 'POST':
        body_json = json.loads(request.body)
        user = authenticate(
            username=body_json['username'],
            password=body_json['password']
        )
        if user is not None:
            login(request, user)
            return JsonResponse({
                "status": "success",
                "message": "User found"
            })
        else:
            return JsonResponse({
                "status": "failure",
                "message": "No such user"
            })
        
    else:
        return JsonResponse({
            'status': 'failure',
            'message': 'Method not allowed on this route'
        })

@csrf_exempt
def isUserAuthenticated(request):
    return JsonResponse({"status": request.user.is_authenticated})

@csrf_exempt
def createProject(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            json_body = json.loads(request.body)
            try:
                name = json_body['name']
                user_pk = request.user.pk
                project_id = create_project(user_pk, name)
                return JsonResponse({
                    "status": "success",
                    "projectId": project_id
                })
            except KeyError as E:
                return JsonResponse({
                    "status": "failure",
                    "message": "Malformed request"
                })
        else:
            return JsonResponse({
                "status": "failure",
                "message": "Please log in first"
            })
    else:
        return JsonResponse({
            "status": "failure",
            "message": "Method not allowed on this route"
        })

@csrf_exempt
def getProjects(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            user_pk = request.user.pk
            projects_list = get_projects(user_pk)
            return JsonResponse({
                "status": "success",
                "name": request.user.username,
                "message": projects_list
            })
        else:
            return JsonResponse({
                "status": "failure",
                "message": "User not logged in"
            })
    else:
        return JsonResponse({
            "status": "failure",
            "message": "Method not allowed on this route"
        })

@csrf_exempt
def selectProject(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            user_pk = request.user.pk
            body_json = json.loads(request.body)
            if "name" not in body_json:
                return JsonResponse({
                    "status": "failure",
                    "message": "Malformed request"
                })
            projects_list = get_projects(user_pk)
            if body_json['name'] not in projects_list:
                return JsonResponse({
                    "status": "failure",
                    "message": "no such project"
                })
            request.session['project'] = body_json['name']
            request.session.modified = True
            print(f"Set active project of user with pk: {user_pk} to {request.session['project']}")
            return JsonResponse({
                "status": "success",
                "message": body_json['name']
            })
        else:
            return JsonResponse({
                "status": "failure",
                "message": "Please log in first"
            })
    else:
        return JsonResponse({
            'status': 'failure',
            'message': 'Method not allowed on this route'
        })

@csrf_exempt
def indexChat(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            json_body = json.loads(request.body)
            msgs = request.session.get('messages', [])
            active_project = request.session.get('project', '')
            if active_project == '':
                return JsonResponse({
                    "status": "failure",
                    "message": "Set active project first."
                })
            
            user_msg = json_body['message']
            project_id = get_project_id(request.user.pk, active_project)
            agent_response = description_agent.call(project_id=project_id, message=user_msg, message_history=msgs)
            if not msgs:
                request.session['messages'] = [{"role": "user", "content": user_msg}, {"role": "assistant", "content": agent_response}]
            else:
                request.session['messages'].append({"role": "user", "content": user_msg})
                request.session['messages'].append({"role": "assistant", "content": agent_response})
            request.session.modified = True
            if agent_response == "completed":
                return JsonResponse({
                    "status": "completed",
                    "message": "Description found successfully"
                })
            return JsonResponse({
                "status": "success", 
                "message": agent_response
            })
        
        else:
            return JsonResponse({
                "status": "failure",
                "message": "not logged in"
            })
    
    else:
        return JsonResponse({
            "status": "failure",
            "message": "Method not allowed on this route."
        })

@csrf_exempt
def getAllMessages(request):
    if request.user.is_authenticated:
        active_project = request.session['project']
        if not active_project:
            return JsonResponse({
                "status": "failure",
                "message": "Please get an active project first."
            })
        proj_id = get_project_id(request.user.pk, active_project)
        messages = get_all_messages(proj_id)
        request.session['messages'] = messages
        request.session.modified = True
        return JsonResponse({
            "status": "success",
            "message": messages
        })

    else:
        return JsonResponse({
            "status": "failure",
            "message": "Please log in first."
        })

@csrf_exempt
def getStatus(request):
    if request.user.is_authenticated:
        active_project = request.session.get('project', None)
        if active_project is None:
            return JsonResponse({
                "status": "failure",
                "message": "No active project selected."
            })
        
        proj_id = get_project_id(user_pk=request.user.pk, name=active_project)
        return JsonResponse({
            "status": "success",
            "message": get_task_status(project_id=proj_id)
        })
    
    else:
        return JsonResponse({
            "status": "failure",
            "message": "Please log in first."
        })

@csrf_exempt
def logoutRoute(request):
    logout(request)
    return JsonResponse({
        "status": "success",
        "message": "logged out successsfully"
    })

@csrf_exempt
def nodeResearchInformation(request):
    if request.user.is_authenticated:
        proj_name = request.session['project']
        proj_id = get_project_id(user_pk=request.user.pk, name=proj_name)
        return JsonResponse(get_all_nodes(f"id_{proj_id}"))
    else:
        return JsonResponse({
            "status": "failure",
            "message": "please log in first."
        })

@csrf_exempt
def getResearch(request):
    if request.user.is_authenticated:
        proj_name = request.session['project']
        proj_id = get_project_id(user_pk=request.user.pk, name=proj_name)
        return JsonResponse({"content": get_researched_content(f"{proj_id}")})
    else:
        return JsonResponse({
            "status": "failure",
            "message": "please log in first."
        })