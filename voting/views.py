from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Election, CandidateApplication, Vote
from .forms import CandidateApplicationForm
from django.contrib import messages
from .forms import ElectionForm
from django.db.models import Count
from accounts.models import User
from django.utils import timezone


# -------------------------
# APPLY FOR ELECTION
# -------------------------
@login_required
def apply_candidate(request, election_id):
    user = request.user

    if user.role != "candidate":
        return render(request, "403.html")

    election = get_object_or_404(Election, id=election_id)

    if request.method == "POST":
        form = CandidateApplicationForm(request.POST)

        if form.is_valid():
            application = form.save(commit=False)
            application.user = user
            application.election = election
            application.save()

            return redirect("candidate_dashboard")

    else:
        form = CandidateApplicationForm()

    return render(request, "voting/apply.html", {"form": form, "election": election})
    


#==================================================
#   Voting Functionalities
#==================================================



@login_required
def vote(request, election_id, candidate_id):

    user = request.user

    # Only voters can vote
    if user.role != "voter":
        return render(request, "403.html")

    election = get_object_or_404(Election, id=election_id)

    candidate = get_object_or_404(User, id=candidate_id)

    # Election has not started
    if timezone.now() < election.start_date:

        messages.error(
            request,
            "This election has not started yet."
        )

        return redirect("voter_dashboard")

    # Election has ended
    if timezone.now() > election.end_date:

        messages.error(
            request,
            "This election has ended. Voting is closed."
        )

        return redirect("voter_dashboard")

    # Prevent voting for non-candidates
    if candidate.role != "candidate":

        messages.error(
            request,
            "Invalid candidate selected."
        )

        return redirect("voter_dashboard")

    # Prevent duplicate voting
    if Vote.objects.filter(
        voter=user,
        election=election
    ).exists():

        messages.error(
            request,
            "You have already voted in this election."
        )

        return redirect("voter_dashboard")

    Vote.objects.create(
        voter=user,
        candidate=candidate,
        election=election
    )

    messages.success(
        request,
        "Vote submitted successfully!"
    )

    return redirect("voter_dashboard")





#==================================================
#   Candidate List
#==================================================

@login_required
def candidate_list(request, election_id):

    election = get_object_or_404(Election, id=election_id)

    candidates = CandidateApplication.objects.filter(
        election=election,
        status="approved"
    )

    return render(
        request,
        "voting/candidate_list.html",
        {
            "election": election,
            "candidates": candidates
        }
    )








#==================================================
#   Admin Election Creation
#==================================================

@login_required
def create_election(request):
    if not request.user.is_superuser:
        return render(request, "403.html")

    if request.method == "POST":
        form = ElectionForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('admin_election_list')

    else:
        form = ElectionForm()

    return render(request, "admin/create_elections.html", {"form": form})


#==================================================
#   Admin Election Update
#==================================================

@login_required
def update_election(request, pk):
    if not request.user.is_superuser:
        return render(request, "403.html")

    election = get_object_or_404(Election, id=pk)
    form = ElectionForm(request.POST or None, instance=election)

    if form.is_valid():
        form.save()
        return redirect('admin_election_list')

    return render(request, "admin/update_election.html", {"form": form})


#==================================================
#   Admin Election Listings
#==================================================

@login_required
def admin_election_list(request):
    if not request.user.is_superuser:
        return render(request, "403.html")

    elections = Election.objects.all()

    return render(request, "admin/election_list.html", {
        "elections": elections
    })


#==================================================
#   Admin Election Deletion
#==================================================

@login_required
def delete_election(request, pk):
    if not request.user.is_superuser:
        return render(request, "403.html")

    election = get_object_or_404(Election, id=pk)

    if request.method == "POST":
        election.delete()
        return redirect('admin_election_list')

    return render(request, "admin/delete_election.html", {"election": election})

#==================================================
#   Candidate Management Listing
#==================================================

@login_required
def manage_candidates(request):
    if not request.user.is_superuser:
        return render(request, "403.html")

    applications = CandidateApplication.objects.all()

    return render(request, "admin/manage_candidates.html", {
        "applications": applications
    })


#==================================================
#   Candidate Approvement Functionality
#==================================================

@login_required
def approve_candidate(request, app_id):
    if not request.user.is_superuser:
        return render(request, "403.html")

    app = get_object_or_404(CandidateApplication, id=app_id)
    app.status = "approved"
    app.save()

    return redirect('manage_candidates')

#==================================================
#   Candidate Rejection Functionality
#==================================================


@login_required
def reject_candidate(request, app_id):
    if not request.user.is_superuser:
        return render(request, "403.html")

    app = get_object_or_404(CandidateApplication, id=app_id)
    app.status = "rejected"
    app.save()

    return redirect('manage_candidates')



#==================================================
#   Voting Result Fuctionalities
#==================================================


@login_required
def election_results(request, election_id):

    election = get_object_or_404(Election, id=election_id)

    # Prevent viewing results before election ends
    if timezone.now() < election.end_date:
        messages.error(
            request,
            "Election results are not available until the election has ended."
        )

        if request.user.role == "candidate":
            return redirect("candidate_dashboard")

        return redirect("voter_dashboard")

    votes = Vote.objects.filter(
        election=election
    )

    results = (
        votes
        .values('candidate')
        .annotate(total_votes=Count('id'))
        .order_by('-total_votes')
    )

    final_results = []

    for item in results:

        candidate = get_object_or_404(
            User,
            id=item['candidate']
        )

        final_results.append({
            "candidate": candidate,
            "votes": item['total_votes']
        })

    winner = final_results[0] if final_results else None

    return render(
        request,
        "voting/results.html",
        {
            "election": election,
            "results": final_results,
            "winner": winner
        }
    )


#==================================================
#   Admin vote page 
#==================================================


@login_required
def admin_vote_list(request):

    # ONLY ADMIN CAN ACCESS
    if not request.user.is_superuser:
        return redirect('login')

    votes = Vote.objects.select_related(
        'voter',
        'candidate',
        'election'
    ).order_by('-timestamp')

    context = {
        'votes': votes
    }

    return render(request, 'voting/vote_list.html', context
    )



#==================================================
#   Candidate Application list page 
#==================================================

@login_required
def my_applications(request):

    applications = CandidateApplication.objects.filter(
        user=request.user
    )

    return render(
        request,
        'voting/my_applications.html',
        {
            'applications': applications
        }
    )





#==================================================
#   Candidate vote page 
#==================================================

@login_required
def candidate_votes(request):

    results = (
        Vote.objects
        .filter(candidate=request.user)
        .values('election__title')
        .annotate(total_votes=Count('id'))
        .order_by('-total_votes')
    )

    return render(
        request,
        'voting/candidate_votes.html',
        {
            'results': results
        }
    )








