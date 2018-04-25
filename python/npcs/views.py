from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from npcs.forms import CreateNpcForm


@login_required
def create_npc(request):
    form = CreateNpcForm(request.POST or None)
    if request.POST and form.is_valid():
        npc = form.save()
        return redirect("npcs:create_npc")
    return render(request, "npcs/create_npc.html", {"form": form})
