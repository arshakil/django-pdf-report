# Make sure you added STATIC URL, Media URL and Templates



# PDF Download and Save Individually
from io import BytesIO
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.template.loader import get_template

def render_to_pdf1(template, context):
   template = get_template(template)
   html  = template.render(context)
   result = BytesIO()
   pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
   if not pdf.err:
       return HttpResponse(result.getvalue(), content_type='application/pdf')
   return None

def generate_obj_pdf1(request):
    '''
    if you want to save pdf in model
    '''
    obj = Calculation.objects.get(id=2)
    context = {'obj': obj}
    pdf = render_to_pdf1('pdf.html', context)  # pdf.htm is yourtemplates name, where your tamplates is located
    filename = "File name is {fname}{ext}".format(fname=obj.name, ext=".pdf")
    obj.pdf.save(str(filename), File(BytesIO(pdf.content)))
    # return JsonResponse({'result': "t"})

    '''
    if you want to direct download
    '''
    # Create a Django response object, and specify content_type as pdf
    template_path = 'pdf.html' # your templates path, where your tamplates is located
    obj = Calculation.objects.get(id=2)
    context = {'obj': obj}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
    # return pdf



def my_view(request):
    obj = Calculation.objects.get(id=1)
    context = {
        "obj":obj
    }
    return render(request, 'pdf.html', context)


#################################################################################################################
# PDF Download and Save at a time
from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.http import HttpResponse
def render_to_pdf(template, context, is_direct_download_or_create):
   template = get_template(template)
   html  = template.render(context)
   result = BytesIO()
   pdf=""
   if is_direct_download_or_create==1:
       pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
   else:
       response = HttpResponse(content_type='application/pdf')
       response['Content-Disposition'] = 'attachment; filename="report.pdf"'
       pdf = pisa.CreatePDF(
           html, dest=response)
       return response
   if not pdf.err:
       return HttpResponse(result.getvalue(), content_type='application/pdf')
   return None

def generate_obj_pdf(request):
    '''
    if you want to save pdf in model
    '''
    is_direct_download_or_create=0  # checking pdf will directly will download or just create in DB, if download=1, create=0
    template_path = 'pdf.html' # your templates path, where your tamplates is located
    obj = Calculation.objects.get(id=2)
    context = {'obj': obj}
    pdf = render_to_pdf(template_path, context, is_direct_download_or_create)
    filename = "File name is {fname}{ext}".format(fname=obj.name, ext=".pdf")
    obj.pdf.save(str(filename), File(BytesIO(pdf.content)))
    return pdf

