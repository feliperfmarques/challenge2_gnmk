# -*- coding: UTF-8 -*-

from django.shortcuts import render_to_response, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import StreamingHttpResponse
from django.core.servers.basehttp import FileWrapper
from painel.models import History
from django.utils.encoding import smart_str
from django.template import RequestContext
from challenge2_gnmk.settings import BASE_DIR
import os
import glob
import uuid
import mimetypes
import fileinput

def select(request):

    if request.user.is_authenticated():

        panels_list = []
        genes_list = []

        for panel in glob.glob(os.path.join(BASE_DIR, "painel/files/panels/*.txt")):
            genes = []
            for line in open(panel, "r"):
                genes.append(line.rstrip())
            panels_list.append({'name': panel.rsplit('/', 1)[1].split('.txt')[0], 'genes': ",".join(genes)})


        for line in open(os.path.join(BASE_DIR, "painel/files/references/Genes_NM.txt"), "r"):
            genes_list.append({'gene': line.split( )[0], 'refer': line.split( )[1]})


        if request.method == 'POST':

            references = request.POST.getlist('genes')
            panels = request.POST.getlist('panel')
            panels_list = []
            genes_list = []

            for panel in panels:
                panels_list.append(panel.split('_',1)[0])

            user_dir = os.path.join(BASE_DIR, "painel/files/history/") + request.user.username

            while 1:
                file_name = unicode(uuid.uuid4())
                try:
                    History.objects.get(filename=file_name)
                except History.DoesNotExist:
                    break

            file_path = user_dir + "/" + file_name + ".bed"

            if not os.path.exists(user_dir):
                os.makedirs(user_dir)
            file = open(file_path, "w")

            for reference in references:
                genes_list.append(reference.split('_',1)[0])
                for line in open(os.path.join(BASE_DIR, "painel/files/regions/genesGalaxy.bed"), "r"):
                    if(reference.split('_',1)[1] in line):
                        file.write(line)

            file.close()

            history = History(user=request.user, panels=(", ".join(panels_list)), genes=(", ".join(genes_list)), filename=file_name)
            history.save()

            wrapper = FileWrapper(open(file_path, "r"))
            content_type = mimetypes.guess_type(file_path)[0]
            response = StreamingHttpResponse(wrapper, content_type = content_type)
            response['Content-Length'] = os.path.getsize(file_path)
            response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name + ".bed")

            return response

        else:

            return render_to_response('painel/select.html', {'genes_list': genes_list, 'panels_list': panels_list}, context_instance=RequestContext(request))

    else:
        return HttpResponseRedirect('/painel/login/')


def references(request):

    if request.user.is_authenticated():

        success = ""
        genes_list = []
        for line in open(os.path.join(BASE_DIR, "painel/files/references/Genes_NM.txt"), "r"):
            genes_list.append({'gene': line.split( )[0], 'refer': line.split( )[1]})

        if request.method == 'POST':

            old = request.POST.getlist('old')
            new = request.POST.getlist('new')

            for line in fileinput.input(os.path.join(BASE_DIR, "painel/files/references/Genes_NM.txt"), inplace=True):
                print(line.replace(old[0], new[0]).rstrip())

            for line in fileinput.input(os.path.join(BASE_DIR, "painel/files/regions/genesGalaxy.bed"), inplace=True):
                print(line.replace(old[0], new[0]).rstrip())

            success = "Referência atualizada com sucesso!"

        return render_to_response('painel/references.html', {'genes_list': genes_list, 'success': success}, context_instance=RequestContext(request))

    else:
        return HttpResponseRedirect('/painel/login/')


def history(request):

    if request.user.is_authenticated():

        history_list = History.objects.all()

        paginator = Paginator(history_list, 20)

        page = request.GET.get('page')

        try:
            history_list = paginator.page(page)

        except PageNotAnInteger:
            history_list = paginator.page(1)

        except EmptyPage:
            history_list = paginator.page(paginator.num_pages)

        return render_to_response('painel/history.html', {"history_list": history_list}, context_instance=RequestContext(request))

    else:
        return HttpResponseRedirect('/painel/login/')


def download(request, filename):

    if request.user.is_authenticated():


        user_dir = os.path.join(BASE_DIR, "painel/files/history/") + request.user.username + "/"
        file_path = user_dir + filename + ".bed"

        wrapper = FileWrapper(open(file_path, "r"))
        content_type = mimetypes.guess_type(file_path)[0]
        response = StreamingHttpResponse(wrapper, content_type = content_type)
        response['Content-Length'] = os.path.getsize(file_path)
        response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(filename + ".bed")

        return response

    else:
        return HttpResponseRedirect('/painel/login/')


def delete(request, filename):

    if request.user.is_authenticated():


        user_dir = os.path.join(BASE_DIR, "painel/files/history/") + request.user.username + "/"
        file_path = user_dir + filename + ".bed"

        os.remove(file_path)
        History.objects.filter(filename=filename).delete()

        return HttpResponseRedirect('/painel/history/')

    else:
        return HttpResponseRedirect('/painel/login/')
