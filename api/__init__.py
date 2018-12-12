# # -*- coding: utf-8 -*-
# import importlib
# import inspect
# import uuid

# from flask import Flask, render_template, session, g, request, jsonify, abort, url_for
# from flask_restful import Api, marshal, Resource
# from flask_admin import Admin
# from flask_admin.contrib.mongoengine import ModelView

# from mongoengine import connect

# from api.conf import *

# connect(DBNAME)

# app = Flask(
#     PROJECT_NAME,
#     static_folder=STATIC_FOLDER_PATH,
# )
# app.secret_key = SECRECT_KEY

# admin = Admin(
#     app,
#     name="%s" % PROJECT_NAME
# )

# api = Api(app)

# # Add public models
# model_file = importlib.import_module(
#     "%s.models" % MAIN_FOLDER
# )
# print("└────Adding public model views")
# _models = inspect.getmembers(model_file)
# models = []
# for name, obj in _models:
#     if inspect.isclass(obj) and \
#         '%s' % MAIN_FOLDER in str(obj) and \
#         'Model' in str(obj):
#         models.append((name, obj))
# for index, (name, obj) in enumerate(models):
#     if index == len(models) - 1:
#         print("     └────Creating public model view %s" % name)
#     elif not index:
#         print("     ├────Creating public model view %s" % name)
#     else:
#         print("     ├────Creating public model view %s" % name)
#     admin.add_view(
#         ModelView(
#             obj,
#             endpoint="%s" % name.lower()
#         )
#     )

# for package in INSTALLED_PACKAGES:
#     print("Installing package %s" % package)
#     resource_file = importlib.import_module(
#         "%s.%s.resource" % (MAIN_FOLDER, package)
#     )
#     model_file = importlib.import_module(
#         "%s.%s.model" % (MAIN_FOLDER, package)
#     )
#     print("├────Adding resources")
#     _resources = inspect.getmembers(resource_file)
#     resources = []
#     for name, obj in _resources:
#         if inspect.isclass(obj) and \
#                 '%s.%s' % (MAIN_FOLDER, package) in str(obj) and \
#                 'Resource' in str(obj):
#                 resources.append((name, obj))
#     for index, (name, obj) in enumerate(resources):
#                 if index == len(resources) - 1:
#                     print("│    └────Adding %s to resources" % name)
#                 elif not index:
#                     print("│    ├────Adding %s to resources" % name)
#                 else:
#                     print("│    ├────Adding %s to resources" % name)
#                 api.add_resource(
#                     obj,
#                     '/%s/%s' % (package, obj.url),
#                     endpoint='%s.%s' % (package, obj.__name__)
#                 )
#     print("└────Adding model views")
#     _models = inspect.getmembers(model_file)
#     models = []
#     for name, obj in _models:
#         if inspect.isclass(obj) and \
#                 '%s.%s' % (MAIN_FOLDER, package) in str(obj) and \
#                 'Model' in str(obj):
#                 models.append((name, obj))
#     for index, (name, obj) in enumerate(models):
#                 if index == len(models) - 1:
#                     print("     └────Creating model view %s" % name)
#                 elif not index:
#                     print("     ├────Creating model view %s" % name)
#                 else:
#                     print("     ├────Creating model view %s" % name)
#                 admin.add_view(
#                     ModelView(
#                         obj,
#                         endpoint="%s_%s" % (package, name.lower())
#                     )
#                 )
