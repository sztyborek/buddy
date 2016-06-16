from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from .models import Project
from users.models import Skill
from .forms import ProjectForm, SkillFormSet
from django.http import HttpResponseRedirect


class ProjectListView(ListView):
    model = Project

class ProjectDetailView(DetailView):
    model = Project

class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    subform_class = SkillFormSet

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.form_class(request.POST)
        subform = self.subform_class(request.POST)
        if form.is_valid() and subform.is_valid():
            this_project = form.save(commit=False)
            this_project.save()
            for a_form in subform:
                a_lang = a_form.cleaned_data.get('programming_lang')
                if a_lang:
                    a_lang = a_lang.lower()
                    skill, created = Skill.objects.get_or_create(programming_lang=a_lang)
                    this_project.skills.add(skill)
            this_project.save()
            self.object = Project.objects.get(slug=this_project.slug)
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(
                self.get_context_data(form=form, subform=subform))

    def get_context_data(self, **kwargs):
        context = super(ProjectCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['subform'] = self.subform_class(self.request.POST)
        else:
            context['subform'] = self.subform_class(queryset = Skill.objects.none())
        return context
        
    def get_success_url(self):
        return reverse_lazy('projects:detail', args=(self.object.slug,)) 

class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    subform_class = SkillFormSet

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.object)
        subform = self.subform_class(request.POST)
        if form.is_valid() and subform.is_valid():
            this_project = form.save(commit=False)
            this_project.skills.clear()
            for a_form in subform:
                a_lang = a_form.cleaned_data.get('programming_lang')
                if a_lang:
                    a_lang = a_lang.lower()
                    skill, created = Skill.objects.get_or_create(programming_lang=a_lang)
                    this_project.skills.add(skill)
            this_project.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(
                self.get_context_data(form=form, subform=subform))

    def get_context_data(self, **kwargs):
        context = super(ProjectUpdateView, self).get_context_data(**kwargs)
        context['subform'] = self.subform_class(queryset = self.get_object().skills.all())
        return context

    def get_success_url(self):
        return reverse_lazy('projects:detail', args=(self.object.slug,)) 

class ProjectDeleteView(DeleteView):
    model = Project
    success_url = reverse_lazy('projects:list')
