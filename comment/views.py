import json
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from react_render.django import render_component
from .models import Comment

comments = [
    dict(author=c.author, text=c.text)
    for c in Comment.objects.all()
]


def index(request):
    # Param flag to deactivate client-side Javascript
    no_js = 'no-js' in request.GET

    # Render the CommentBox component down to HTML
    comment_box = render_component(
        # The path to the component is resolved via Django's
        # static-file finders
        'js/main.server.js',
        # We can pass data along to the component which will be
        # accessible from the component via its `this.props` property
        props={
            'comments': comments,
            'url': reverse('comment:comment'),
        },
        # If we intend to use React on the client-side, React will
        # add extra attributes to the HTML so that the initial mount
        # is faster, however these extra attributes are unnecessary
        # if there is no JS on the client-side.
        to_static_markup=no_js
    )

    context = {
        'comment_box': comment_box,
        'no_js': no_js,
    }

    return render(request, 'core/index.html', context)


def comment(request):
    if request.POST:
        c = Comment.objects.create(
            author=request.POST.get('author', None),
            text=request.POST.get('text', None)
        )
        comments.append({
            'author': c.author,
            'text': c.text,
        })
        if not request.is_ajax():
            return redirect('index-no-js')
    return HttpResponse(
        json.dumps(comments),
        content_type='application/json'
    )
