from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect
from  django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import UserForm
from .models import Album


class IndexView(generic.ListView):
    template_name = 'music/index.html'
    context_object_name = 'all_albums'

    def get_queryset(self):
        return Album.objects.all()


class DetailView(generic.DetailView):
    model = Album
    template_name = 'music/detail.html'


class AlbumCreate(CreateView):
    model = Album
    fields = ['artist', 'album_title', 'generex', 'album_logo']


class AlbumUpdate(UpdateView):
    model = Album
    fields = ['artist', 'album_title', 'generex', 'album_logo']


class AlbumDelete(DeleteView):
    model = Album
    success_url = reverse_lazy('music:index')


class UserFormView(View):
    form_class = UserForm
    template_name = 'music/registration_form.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # procces form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)
            # cleaned ( normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # return User Objects if credentials are correct

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('music:index')

        return render(request, self.template_name, {'form': form})

# ____________________
# def index(request):
#    all_albums = Album.objects.all()
#   ---  template = loader.get_template('music/index.html')
# ---- context = {
#    ---- 'all_albums': all_albums
# --- }
#    return render(request, 'music/index.html', {'all_albums': all_albums})
# ___________________
#    html = ''
#    for album in all_albums:
#        url = '/music/' + album.id + '/'
#        html += '<a href="' + url + '">' + album.album_title + '</a><br>'
#    return HttpResponse(template.render(context, request))
# ______________________
# def detail(request, album_id):
#    album = get_object_or_404(Album, pk=album_id)
#    return render(request, 'music/detail.html', {'album': album})
# __________________________
#    try:
#        album = Album.objects.get(pk=album_id)
#    except Album.DoesNotExist:
#        raise Http404("Album no existe")
#    return render(request, 'music/detail.html', {'album': album})
#    return HttpResponse("<h2> Detalle para el album id: " + str(album_id) + "</h2>")

# --------pra hacer el radio de favoritos.
# def favorite(request, album_id):
#    album = get_object_or_404(Album, pk=album_id)
#    try:
#        selected_song = album.song_set.get(pk=request.POST['song'])
#    except (KeyError, Song.DoesNotExist):
#        return render(request, 'music/detail.html', {
#            'album': album,
#            'error_message': "tu no tienes seleccionado un sonido valido"
#        })
#    else:
#        selected_song.is_favorite = True
#        selected_song.save()
#        return render(request, 'music/detail.html', {'album': album})
