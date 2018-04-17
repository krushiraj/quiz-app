from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login
from django.contrib.auth.forms import AuthenticationForm
from forms_builder.forms.models import *
from django.contrib.auth import authenticate
from .models import *

# Create your views here.
def set_all_quizzes():
    all_forms = Form.objects.all()
    #fields = Field.objects.all()
    # username_field = Field(1, 'username', 'username', 1, True, True, '','{{request.user.username}}', None, '')
    for form in all_forms:
        form.redirect_url = '/'
        form.save()
        try:
            Field.objects.get(form_id = form.id, label = 'username')
            continue
        except:
            username_field = Field(
                                    label = 'username', 
                                    slug = 'username', 
                                    field_type = 1, 
                                    required = True, 
                                    visible = True, 
                                    choices = '', 
                                    default = '{{request.user.username}}{% if request.user.is_staff %}*staff*{% endif %}', 
                                    placeholder_text = None, 
                                    help_text = '', 
                                    form_id = form.id
                                )
            username_field.save()
            form.fields.add(username_field)

@login_required
def index(request):
    set_all_quizzes()
    if request.user.is_staff:
        drafts = [(form, form.get_absolute_url) for form in Form.objects.filter(status = 1)]
        published = [(form, form.get_absolute_url) for form in Form.objects.filter(status = 2)]
        return render(request, 'index.html', {'published': published, 'drafts':drafts, 'user': request.user})
    else:
        attempted, unattempted = {}, {}
        for field_entry in FieldEntry.objects.filter(value = request.user.username):
            form = Form.objects.get(id = field_entry.entry.form_id)
            attempted[form] = form.get_absolute_url
        temp = list(attempted.keys())
        for form in Form.objects.published():
            if form not in temp:
                unattempted[form] = form.get_absolute_url
        attempted = [(form, form.get_absolute_url) for form in attempted.keys()]
        unattempted = [(form, form.get_absolute_url) for form in unattempted.keys()]
        return render(request,'index.html',{'unattempted': unattempted, 'attempted': attempted, 'user': request.user})

@login_required
def marks(request, form_id):
    if request.user.is_staff:
        eval = Evaluated(id = form_id)
    else:
        return render(request, 'marks.html', {})
    labels = []
    for field in Form.objects.get(id = form_id).fields.all():
        labels.append(field.label)
    total_marks = len(labels) - 1
    labels += ['marks obtained', 'total marks']
    entries = Form.objects.get(id = form_id).entries.all()
    staff_entryfields = FieldEntry.objects.filter(value__contains = '*staff*')
    staff_entry = None
    for entryfield in staff_entryfields:
        if entryfield.entry.form_id == form_id:
            staff_entry = entryfield.entry
    ans_entry = [field.value for field in staff_entry.fields.all()]
    results = []
    rollno_index = labels.index('username') 
    for entry in entries:
        ans_temp = [field.value for field in entry.fields.all()]
        if '*staff*' in ans_temp[rollno_index]:
            continue        
        marks = len(set(ans_entry) & set(ans_temp))
        ans_temp += [marks, total_marks]
        results.append(ans_temp)
    results.sort(key = lambda x: x[rollno_index])
    return render(request, 'marks.html', {'form': Form.objects.get(id = form_id),
                                          'labels': labels, 
                                          'results' : results, 
                                          'total_marks': total_marks, 
                                          'user' : request.user,
                                          'eval' : eval,
                                        }
                )